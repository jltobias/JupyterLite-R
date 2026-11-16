"""Check exported R Shinylive app controls and downloads in system Chrome.

Requires tools/serve.py on port 8000 serving the combined site. Publishes nothing.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'validation'/'runs'/'browser'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(channel='chrome',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},accept_downloads=True)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/shiny/',wait_until='domcontentloaded',timeout=120000)
    # The exported runtime hosts the Shiny interface in an iframe.
    page.wait_for_selector('iframe',timeout=120000)
    app=page.frame_locator('iframe').first
    app.locator('#summary').wait_for(timeout=180000)
    app.locator('#summary').filter(has_text='sites selected').wait_for(timeout=180000)
    initial=app.locator('#summary').inner_text()
    print('Shinylive initial:',initial,flush=True)
    page.screenshot(path=str(OUT/'shiny-initial.png'),full_page=True)
    app.locator('#seed').fill('2027')
    app.locator('#seed').press('Tab')
    page.wait_for_timeout(1500)
    changed=app.locator('#summary').inner_text()
    assert changed!=initial,'Seed input did not change the summary'
    app.locator('#seed').fill('2026')
    app.locator('#seed').press('Tab')
    page.wait_for_timeout(1500)
    assert app.locator('#summary').inner_text()==initial,'Restoring seed did not reproduce observations'
    # Keyboard control of the slider: move from 48 toward its upper limit.
    app.locator('.irs-handle').click()
    for _ in range(7):page.keyboard.press('ArrowRight')
    page.wait_for_timeout(1500)
    after_threshold=app.locator('#summary').inner_text()
    assert after_threshold!=initial,'Keyboard threshold control did not update selection'
    app.locator('.selectize-input').click()
    app.locator('.selectize-dropdown .option[data-value="Blues 3"]').click()
    page.wait_for_timeout(1000)
    assert app.locator('#summary').inner_text()==after_threshold,'Palette changed the data'
    print('Frame:',page.locator('iframe').first.get_attribute('sandbox'),flush=True)
    print('Download href:',app.locator('#download').get_attribute('href'),flush=True)
    with page.expect_download(timeout=30000) as download_info:
        app.locator('#download').click()
    download=download_info.value
    try:
        download.save_as(str(OUT/'shiny-download.csv'))
    except Exception:
        print('Download failure:',download.failure(),flush=True)
        print('Download URL:',download.url,flush=True)
        print('Browser errors:',errors,flush=True)
        raise
    rows=(OUT/'shiny-download.csv').read_text(encoding='utf-8').splitlines()
    assert len(rows)==101,'CSV must contain 100 observations and one header'
    assert 'selected' in rows[0]
    assert app.locator('.shiny-output-error').count()==0
    page.screenshot(path=str(OUT/'shiny-controls.png'),full_page=True)
    report={'initial':initial,'changed_seed':changed,'after_threshold':after_threshold,
            'csv_rows':100,'javascript_errors':errors,'browser':browser.version}
    (OUT/'shiny-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: Shinylive load, seed changes, restored seed, controls, 100-row CSV download',flush=True)
    browser.close()
