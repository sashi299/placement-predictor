import time
from playwright.sync_api import sync_playwright

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
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/analytics_kpi_overview.png")
        
        # Tab 1: Branch-wise Trends
        print("[4] Testing Branch-wise Trends tab...")
        page.locator("button:has-text('Branch-wise Trends')").click()
        page.wait_for_timeout(1500)
        assert page.locator("text=Placement Rate by Branch (%)").first.is_visible()
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/tab1_branch_trends.png")
        
        # Tab 2: Salary Statistics
        print("[5] Testing Salary Statistics tab...")
        page.locator("button:has-text('Salary Statistics')").click()
        page.wait_for_timeout(1500)
        assert page.locator("text=Salary Distribution for Placed Students").first.is_visible()
        assert page.locator("text=Offers by Salary Tier").first.is_visible()
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/tab2_salary_stats.png")
        
        # Tab 3: Skills Analysis
        print("[6] Testing Skills Analysis tab...")
        page.locator("button:has-text('Skills Analysis')").click()
        page.wait_for_timeout(1500)
        assert page.locator("text=Placement Rate by Primary Skill Domain").first.is_visible()
        assert page.locator("text=Skill Benchmark: Placed vs Unplaced").first.is_visible()
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/tab3_skills_analysis.png")
        
        # Tab 4: Companies & Recruiters
        print("[7] Testing Companies & Recruiters tab...")
        page.locator("button:has-text('Companies & Recruiters')").click()
        page.wait_for_timeout(1500)
        assert page.locator("text=Total Student Hires by Company").first.is_visible()
        assert page.locator("text=Average CTC Offered per Company").first.is_visible()
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/tab4_companies.png")
        
        # Tab 5: Data Explorer & Export
        print("[8] Testing Data Explorer & Export tab...")
        page.locator("button:has-text('Data Explorer & Export')").click()
        page.wait_for_timeout(1500)
        assert page.locator("text=Download Filtered Data as CSV").first.is_visible()
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/tab5_explorer.png")

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
        page.screenshot(path="C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/twin_prediction_verified.png")
        print("[10] Digital Twin prediction verified successfully!")
        
        browser.close()
        print("\n>>> ALL PLAYWRIGHT AUTOMATION TESTS PASSED! <<<")

if __name__ == "__main__":
    test_app()
