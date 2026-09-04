import os
import json
import time
from playwright.sync_api import sync_playwright

def run_slider_interaction_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_selector("[data-testid='stAppViewContainer']")
        time.sleep(2)

        # Let's find range inputs
        range_inputs = page.locator("input[type='range']").all()
        print(f"Found {len(range_inputs)} range inputs.")

        # Let's adjust sliders:
        # 0: CGPA (5.0 to 10.0) -> let's press ArrowRight multiple times
        # 1: Aptitude (0 to 100) -> press ArrowRight
        # 2: Coding (0 to 100)
        # 3: DSA (0 to 100)
        # 4: Communication (0 to 100)
        # 5: Projects Count (0 to 10)
        # 6: Internships (0 to 5)
        # 7: Active Backlogs (0 to 5)

        if len(range_inputs) >= 8:
            print("Adjusting CGPA slider...")
            range_inputs[0].focus()
            for _ in range(20):
                page.keyboard.press("ArrowRight")
            time.sleep(0.5)

            print("Adjusting Coding Score slider...")
            range_inputs[2].focus()
            for _ in range(35):
                page.keyboard.press("ArrowRight")
            time.sleep(0.5)

            print("Adjusting DSA Score slider...")
            range_inputs[3].focus()
            for _ in range(40):
                page.keyboard.press("ArrowRight")
            time.sleep(0.5)

            print("Adjusting Internships slider...")
            range_inputs[6].focus()
            for _ in range(2):
                page.keyboard.press("ArrowRight")
            time.sleep(0.5)

        # Click Predict Placement Readiness
        predict_btn = page.locator("button:has-text('Predict Placement Readiness')")
        print("Clicking Predict button with modified slider values...")
        predict_btn.click()

        page.wait_for_selector("text=Prediction Result", timeout=15000)
        time.sleep(2)

        # Take screenshot
        screenshot_path = "tests/prediction_modified_sliders.png"
        page.screenshot(path=screenshot_path, full_page=True)

        artifact_dir = r"C:\Users\hp\.gemini\antigravity\brain\b252461a-8155-40c0-af00-bdd70fac1134"
        if os.path.exists(artifact_dir):
            import shutil
            shutil.copy(screenshot_path, os.path.join(artifact_dir, "prediction_modified_sliders.png"))

        # Extract results
        main_text = page.locator("[data-testid='stAppViewContainer']").inner_text()
        with open("tests/modified_sliders_result.json", "w", encoding="utf-8") as f:
            json.dump({"main_text": main_text}, f, indent=2)

        print("Modified slider test complete! Results saved.")
        browser.close()

if __name__ == "__main__":
    run_slider_interaction_test()
