import sys
import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("[1] Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", timeout=30000)
        
        # Wait for Streamlit app to load
        page.wait_for_selector("text=Placement Readiness Digital Twin", timeout=20000)
        print("[2] Page loaded successfully with title 'Placement Readiness Digital Twin'")
        
        # Take initial screenshot
        page.screenshot(path="tests/initial_state.png", full_page=True)
        print("[3] Captured initial state screenshot: tests/initial_state.png")
        
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
        page.screenshot(path="tests/prediction_result.png", full_page=True)
        print("[8] Captured final prediction results screenshot: tests/prediction_result.png")
        
        browser.close()
        print("ALL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test()
