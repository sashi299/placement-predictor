import os
import json
import time
from playwright.sync_api import sync_playwright

def run_extended_test():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=15000)

        # Let's adjust sliders:
        # Sliders order in app.py:
        # 0: CGPA (5.0 to 10.0, step 0.1/default 7.0)
        # 1: Aptitude Score (0 to 100, default 50)
        # 2: Coding Score (0 to 100, default 50)
        # 3: DSA Score (0 to 100, default 50)
        # 4: Communication Score (0 to 100, default 50)
        # 5: Projects Count (0 to 10, default 2)
        # 6: Internships (0 to 5, default 0)
        # 7: Active Backlogs (0 to 5, default 0)

        sliders = page.locator("[role='slider']").all()
        print(f"Found {len(sliders)} slider thumbs.")

        # Adjust Coding Score (index 2) and DSA Score (index 3) to higher values
        if len(sliders) >= 4:
            # Click on slider thumb and use keyboard to increase
            coding_slider = sliders[2]
            coding_slider.focus()
            for _ in range(40):
                coding_slider.press("ArrowRight")
            
            dsa_slider = sliders[3]
            dsa_slider.focus()
            for _ in range(40):
                dsa_slider.press("ArrowRight")

        time.sleep(1)

        # Click Predict Placement Readiness
        predict_btn = page.locator("button:has-text('Predict Placement Readiness')")
        predict_btn.click()

        page.wait_for_selector("text=Prediction Result", timeout=15000)
        time.sleep(2)

        page.screenshot(path="tests/prediction_high_scores.png", full_page=True)
        
        artifact_dir = r"C:\Users\hp\.gemini\antigravity\brain\b252461a-8155-40c0-af00-bdd70fac1134"
        if os.path.exists(artifact_dir):
            import shutil
            shutil.copy("tests/prediction_high_scores.png", os.path.join(artifact_dir, "prediction_high_scores.png"))

        main_text = page.locator("[data-testid='stAppViewContainer']").inner_text()
        with open("tests/test_results_interactive.json", "w", encoding="utf-8") as f:
            json.dump({"main_text": main_text}, f, indent=2)

        print("Interactive test finished successfully.")
        browser.close()

if __name__ == "__main__":
    run_extended_test()
