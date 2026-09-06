import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("[1] Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", timeout=30000)
        
        # Navigate to Digital Twin in sidebar if needed
        radio_twin = page.locator("label:has-text('Placement Readiness Digital Twin')")
        if radio_twin.is_visible():
            radio_twin.click()
            page.wait_for_timeout(1500)

        # Wait for Streamlit app to load
        page.wait_for_selector("text=Placement Readiness Digital Twin", timeout=20000)
        print("[2] Page loaded successfully with title 'Placement Readiness Digital Twin'")
        
        # Take initial screenshot
        page.screenshot(path=str(SCREENSHOTS_DIR / "initial_state.png"), full_page=True)
        print(f"[3] Captured initial state screenshot: {SCREENSHOTS_DIR / 'initial_state.png'}")
        
        # Click the "Predict Placement Readiness" button
        predict_button = page.locator("button:has-text('Predict Placement Readiness')")
        print("[4] Clicking 'Predict Placement Readiness' button...")
        predict_button.click()
        
        # Wait for results to appear
        page.wait_for_selector("text=Prediction Result", timeout=15000)
        print("[5] Prediction Result section appeared!")
        
        # Extract text elements
        track_text = page.locator("div[data-testid='stAlert']").all_inner_texts()
        print(f"[6] Alert outputs: {track_text}")
        
        metric_val = page.locator("div[data-testid='stMetricValue']").all_inner_texts()
        print(f"[7] Readiness Score: {metric_val}")
        
        # Wait a moment for chart/progress bars to finish animation
        time.sleep(1)
        
        # Take final screenshot
        page.screenshot(path=str(SCREENSHOTS_DIR / "prediction_result.png"), full_page=True)
        print(f"[8] Captured final prediction results screenshot: {SCREENSHOTS_DIR / 'prediction_result.png'}")
        
        browser.close()
        print("ALL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test()
