"""Exercise the actual JupyterLite UI with Chrome; save runtime/browser evidence locally."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'validation'/'runs'/'browser'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/lite/lab/index.html?path=01-browser-laboratory.ipynb',wait_until='domcontentloaded',timeout=120000)
    page.wait_for_selector('.jp-Notebook',timeout=120000)
    page.wait_for_function("document.body.innerText.includes('R (webR) | Idle')",timeout=120000)
    print('Globals:',page.evaluate("({app:typeof window.jupyterapp,lite:typeof window.jupyterlite})"),flush=True)
    page.get_by_text('Run',exact=True).click()
    print('Menu:',page.locator('.lm-Menu').inner_text(),flush=True)
    page.get_by_text('Run All Cells',exact=True).click()
    page.wait_for_timeout(20000)
    print(page.locator('body').inner_text()[-14000:],flush=True)
    print('Errors',errors,flush=True)
    page.screenshot(path=str(OUT/'lab-executed.png'),full_page=True)
    (OUT/'lab-console.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    browser.close()
