"""Check final local Book/landing/gallery routes and a narrow gallery viewport."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'validation'/'runs'/'browser'
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    for slug in ['', 'book/', 'book/notebooks/browser-laboratory/', 'book/notebooks/reactive-maps-with-shiny/']:
        response=page.goto('http://127.0.0.1:8000/'+slug,wait_until='networkidle',timeout=60000)
        assert response.status==200,(slug,response.status)
        assert page.locator('h1').count()>0,slug
        missing=page.evaluate("Array.from(document.images).filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)")
        assert not missing,missing
        page.screenshot(path=str(OUT/('site-'+(slug.replace('/','-') or 'home')+'.png')),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    page.goto('http://127.0.0.1:8000/gallery/',wait_until='networkidle',timeout=60000)
    page.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')")
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    page.screenshot(path=str(OUT/'gallery-mobile.png'),full_page=True)
    (OUT/'site-report.json').write_text(json.dumps({'javascript_errors':errors,'routes':'landing, Book home, chapters 1 and 10','mobile_gallery_width':390},indent=2),encoding='utf-8')
    print('PASS: Book routes/images, landing page, 390px gallery; errors:',errors,flush=True)
    browser.close()
