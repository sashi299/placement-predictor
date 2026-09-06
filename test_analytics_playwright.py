import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        
        print("[1] Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", timeout=30000)
        page.wait_for_timeout(3000)
        
        # Check title
        assert page.locator("h1:has-text('Placement Analytics Dashboard')").is_visible(), "Dashboard title not found"
        print("[2] Verified Placement Analytics Dashboard title")
        
        # Check metrics
        page.wait_for_selector("text=Total Students")
        page.wait_for_selector("text=Average CTC")
        page.wait_for_selector("text=Highest CTC")
        print("[3] Verified KPI metric cards")
        
        # Screenshot overview
        page.screenshot(path=str(SCREENSHOTS_DIR / "analytics_kpi_overview.png"))
        
        # Tab testing
        tabs = [
            ("Branch-wise Trends", "tab1_branch_trends.png"),
            ("Salary Statistics", "tab2_salary_stats.png"),
            ("Skills Analysis", "tab3_skills_analysis.png"),
            ("Companies & Recruiters", "tab4_companies.png"),
            ("Data Explorer & Export", "tab5_explorer.png")
        ]
        
        for idx, (tab_name, shot_name) in enumerate(tabs, 4):
            print(f"[{idx}] Testing {tab_name} tab...")
            tab_elem = page.get_by_role("tab", name=tab_name)
            if tab_elem.is_visible():
                tab_elem.click()
                page.wait_for_timeout(1500)
                page.screenshot(path=str(SCREENSHOTS_DIR / shot_name))
        
        # Switch to Digital Twin page
        print("[9] Testing Navigation to Placement Readiness Digital Twin...")
        radio_twin = page.locator("label:has-text('Placement Readiness Digital Twin')")
        radio_twin.click()
        page.wait_for_timeout(2000)
        
        assert page.locator("h1:has-text('Placement Readiness Digital Twin')").is_visible()
        predict_btn = page.locator("button:has-text('Predict Placement Readiness')")
        assert predict_btn.is_visible()
        predict_btn.click()
        page.wait_for_timeout(2000)
        
        assert page.locator("text=Prediction Result").first.is_visible()
        assert page.locator("text=Readiness Score").first.is_visible()
        page.screenshot(path=str(SCREENSHOTS_DIR / "twin_prediction_verified.png"))
        print("[10] Digital Twin prediction verified successfully!")
        
        browser.close()
        print("\n>>> ALL PLAYWRIGHT AUTOMATION TESTS PASSED! <<<")

if __name__ == "__main__":
    test_app()
