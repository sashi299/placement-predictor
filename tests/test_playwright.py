import os
import json
import time
from playwright.sync_api import sync_playwright

def run_test():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("1. Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        
        # Wait for Streamlit app container to be ready
        page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=20000)
        time.sleep(2)  # Allow Streamlit to finish rendering components

        # Check page title and headings
        html_title = page.title()
        print(f"HTML Title: {html_title}")
        results["html_title"] = html_title

        # Headings check
        title_element = page.locator("h1").first
        title_text = title_element.inner_text() if title_element.count() > 0 else ""
        print(f"H1 Title: {title_text}")
        results["h1_title"] = title_text

        sub_text = page.locator("text='Predict placement readiness and company fit.'").first
        results["subtitle_present"] = sub_text.is_visible()
        print(f"Subtitle visible: {results['subtitle_present']}")

        # Sliders verification and interaction
        # Find sliders
        sliders = page.locator("[data-testid='stSlider']")
        slider_count = sliders.count()
        print(f"Found {slider_count} sliders.")
        results["slider_count"] = slider_count

        # Adjust a slider (e.g. CGPA or Coding Score) by keyboard arrow or slider track click
        if slider_count > 0:
            first_slider_thumb = sliders.first.locator("[role='slider']")
            if first_slider_thumb.count() > 0:
                print("Interacting with first slider (CGPA)...")
                first_slider_thumb.focus()
                first_slider_thumb.press("ArrowRight")
                first_slider_thumb.press("ArrowRight")
                time.sleep(1)

        # Take initial screenshot
        os.makedirs("tests", exist_ok=True)
        page.screenshot(path="tests/initial_state.png", full_page=True)
        print("Captured initial_state.png")

        # Locate 'Predict Placement Readiness' button
        predict_btn = page.locator("button:has-text('Predict Placement Readiness')")
        btn_visible = predict_btn.is_visible()
        print(f"Predict button visible: {btn_visible}")
        results["button_visible"] = btn_visible

        # Click the button
        print("Clicking 'Predict Placement Readiness' button...")
        predict_btn.click()

        # Wait for results to appear
        print("Waiting for Prediction Result...")
        page.wait_for_selector("text=Prediction Result", timeout=15000)
        time.sleep(2)

        # Extract Predicted Track
        alert_success = page.locator("[data-testid='stAlert']").first
        track_text = alert_success.inner_text() if alert_success.count() > 0 else ""
        print(f"Track Result: {track_text}")
        results["track_result"] = track_text

        # Extract Readiness Score
        metric_value = page.locator("[data-testid='stMetricValue']").first
        readiness_score = metric_value.inner_text() if metric_value.count() > 0 else ""
        print(f"Readiness Score: {readiness_score}")
        results["readiness_score"] = readiness_score

        # Status text (Needs Improvement / Good / Excellent)
        status_alerts = page.locator("[data-testid='stAlert']").all_inner_texts()
        print(f"Status Alerts: {status_alerts}")
        results["status_alerts"] = status_alerts

        # Extract Prediction Confidence
        confidence_header = page.locator("text=Prediction Confidence")
        results["confidence_header_visible"] = confidence_header.is_visible()

        # Extract Top Company Matches
        company_header = page.locator("text=Top Company Matches")
        results["company_header_visible"] = company_header.is_visible()

        # Get all text from main container
        main_content = page.locator("[data-testid='stAppViewContainer']").inner_text()
        
        # Save screenshot after prediction
        page.screenshot(path="tests/prediction_result.png", full_page=True)
        print("Captured prediction_result.png")

        # Copy to artifact directory if it exists
        artifact_dir = r"C:\Users\hp\.gemini\antigravity\brain\b252461a-8155-40c0-af00-bdd70fac1134"
        if os.path.exists(artifact_dir):
            import shutil
            shutil.copy("tests/initial_state.png", os.path.join(artifact_dir, "initial_state.png"))
            shutil.copy("tests/prediction_result.png", os.path.join(artifact_dir, "prediction_result.png"))
            print(f"Copied screenshots to artifact directory: {artifact_dir}")

        results["main_text"] = main_content
        with open("tests/test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print("TEST COMPLETED SUCCESSFULLY!")
        browser.close()

if __name__ == "__main__":
    run_test()
