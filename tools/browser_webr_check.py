"""Execute notebook core cells in the pinned webR runtime inside Chrome.

Uses the built Lab origin (and its isolation worker), with a separate webR evaluator.
This complements, rather than replaces, the actual notebook UI smoke test.
Requires the optional playwright test dependency and system Chrome.
"""
from pathlib import Path
import json
import argparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'validation'/'runs'/'browser'
OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--extensions',action='store_true')
args=parser.parse_args()
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page()
    page.goto('http://127.0.0.1:8000/lite/lab/index.html',wait_until='domcontentloaded',timeout=120000)
    page.wait_for_function('crossOriginIsolated',timeout=120000)
    page.evaluate("""async () => {
      const {WebR}=await import('https://webr.r-wasm.org/v0.5.1/webr.mjs');
      window.validationR=new WebR({baseUrl:'https://webr.r-wasm.org/v0.5.1/'});
      await validationR.init();
      window.validationShelter=await new validationR.Shelter();
      const cwd=await validationR.evalRString('getwd()');
      await validationR.FS.mkdir(cwd+'/data');
      const border=await fetch('/lite/files/data/FictionalBG.rda');
      if(border.ok)await validationR.FS.writeFile(cwd+'/data/FictionalBG.rda',new Uint8Array(await border.arrayBuffer()));
    }""")
    runtime=page.evaluate("async()=>await validationR.evalRString('R.version.string')")
    results={'runtime':runtime,'webR':'0.5.1','browser':browser.version,'core':[],'extensions':[]}
    for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
        nb=json.loads(path.read_text(encoding='utf-8'))
        page.evaluate("async()=>{window.chapterEnv=await validationR.evalR('new.env(parent=globalenv())');}")
        codes=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code' and 'optional-package' not in c.get('metadata',{}).get('tags',[])]
        for code in codes:
            answer=page.evaluate("""async(code)=>{
              const captured=await validationShelter.captureR(code,{env:chapterEnv,captureGraphics:true});
              const errors=captured.output.filter(x=>x.type==='error');
              if(errors.length)throw new Error(await errors[0].data.toString());
              const imageCount=captured.images.length;
              await validationShelter.purge();
              return imageCount;
            }""",code)
        results['core'].append({'notebook':path.name,'cells':len(codes),'status':'pass'})
        print('webR core PASS:',path.name,flush=True)
    # One explicitly selected, small package integration check.
    page.evaluate("async()=>{await validationR.installPackages(['RColorBrewer']);}")
    page.evaluate("async()=>{await validationR.evalRVoid(\"stopifnot(length(RColorBrewer::brewer.pal(5, 'YlGnBu')) == 5)\");}")
    results['extensions'].append({'package':'RColorBrewer','status':'installed and palette assertion passed'})
    if args.extensions:
        for package in ['sf','spdep','ggplot2','micromapST']:
            try:
                page.evaluate("async(name)=>{await validationR.installPackages([name]);}",package)
                installed=page.evaluate("async(name)=>await validationR.evalRBoolean(`requireNamespace('${name}',quietly=TRUE)`)",package)
                results['extensions'].append({'package':package,'installed':installed})
                print('webR package:',package,installed,flush=True)
            except Exception as error:
                results['extensions'].append({'package':package,'installed':False,'error':str(error)[:600]})
                print('webR package unavailable:',package,flush=True)
        results['optional_cells']=[]
        for path in sorted((ROOT/'notebooks').glob('*.ipynb')):
            nb=json.loads(path.read_text(encoding='utf-8'))
            if not any('optional-package' in c.get('metadata',{}).get('tags',[]) for c in nb['cells']):continue
            page.evaluate("async()=>{window.chapterEnv=await validationR.evalR('new.env(parent=globalenv())');}")
            try:
                for c in nb['cells']:
                    if c['cell_type']!='code':continue
                    page.evaluate("""async(code)=>{
                      const captured=await validationShelter.captureR(code,{env:chapterEnv,captureGraphics:true});
                      const errors=captured.output.filter(x=>x.type==='error');
                      if(errors.length)throw new Error(await errors[0].data.toString());
                      await validationShelter.purge();
                    }""",''.join(c['source']))
                results['optional_cells'].append({'notebook':path.name,'status':'completed; package availability recorded separately'})
            except Exception as error:
                results['optional_cells'].append({'notebook':path.name,'status':'failed','error':str(error)[:600]})
    results['session']=page.evaluate("async()=>await validationR.evalRString(\"paste(capture.output(sessionInfo()),collapse='\\n')\")")
    (OUT/'webr-report.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(results['session'],flush=True)
    browser.close()
    if any(item.get('installed') is False for item in results['extensions']) or any(item.get('status')=='failed' for item in results.get('optional_cells',[])):
        raise SystemExit('A required browser extension check failed; inspect webr-report.json')
