"""Run against the app on port 8501: python tests/browser_smoke.py."""
from pathlib import Path
from io import BytesIO
from docx import Document
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    page.goto('http://127.0.0.1:8501')
    page.get_by_role('button', name='Build evidence-based draft').click()
    editor = page.get_by_role('textbox', name='Edit resume Markdown')
    editor.wait_for()
    assert 'Alex Morgan' in editor.input_value()
    assert 'PMP' not in editor.input_value()
    page.get_by_text('I reviewed this draft for factual accuracy and approve it for download.', exact=True).click()
    with page.expect_download() as download:
        page.get_by_role('button', name='Download Word resume').click()
    doc = Document(BytesIO(Path(download.value.path()).read_bytes()))
    assert doc.paragraphs[0].text == 'Alex Morgan'
    page.get_by_role('tab', name='Evidence & gaps').click()
    page.get_by_text('JD evidence candidates', exact=True).wait_for()
    page.get_by_role('tab', name='Resume editor', exact=True).click()
    Path('outputs').mkdir(exist_ok=True)
    page.screenshot(path='outputs/demo.png', full_page=True)
    page.get_by_role('button', name='Clear session', exact=True).click()
    page.get_by_role('button', name='Build evidence-based draft').wait_for()
    expect(page.get_by_role('textbox', name='Edit resume Markdown')).to_have_count(0)
    browser.close()
    print('Browser smoke passed: generate, evidence, review, DOCX download, clear session.')
