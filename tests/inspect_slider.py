from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:8501", wait_until="networkidle")
    page.wait_for_selector("[data-testid='stAppViewContainer']")
    
    # Check all elements with slider or input
    slider_elements = page.locator("[data-testid='stSlider']").all()
    print(f"Count of stSlider: {len(slider_elements)}")
    if slider_elements:
        first = slider_elements[0]
        print("HTML of first slider:", first.inner_html())

    browser.close()
