"""Local browser diagnostics; requires playwright and an installed Chrome browser."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validation' / 'runs' / 'browser'
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page(viewport={'width':1440,'height':1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/gallery/', wait_until='networkidle', timeout=120000)
    page.wait_for_function("document.querySelector('#status').textContent.startsWith('Ready')", timeout=90000)
    page.screenshot(path=str(OUT/'gallery-map.png'), full_page=True)
    for name in ['terrain','scene','globe','evidence']:
        page.locator(f'[data-view="{name}"]').click()
        page.wait_for_timeout(1200)
        assert page.locator(f'[data-view="{name}"]').get_attribute('aria-pressed') == 'true'
        page.screenshot(path=str(OUT/f'gallery-{name}.png'), full_page=True)
    print('Gallery views:', errors, flush=True)
    page.goto('http://127.0.0.1:8000/lite/lab/index.html?path=01-browser-laboratory.ipynb', wait_until='domcontentloaded', timeout=120000)
    page.wait_for_timeout(30000)
    page.screenshot(path=str(OUT/'lab-start.png'), full_page=True)
    print('Isolated:', page.evaluate('crossOriginIsolated'), flush=True)
    print(page.locator('body').inner_text()[-12000:], flush=True)
    (OUT/'probe-errors.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    browser.close()
