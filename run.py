#!/usr/bin/env python3
"""
Universal Cross-Platform CLI Runner for Placement Readiness & Analytics Portal.
Compatible with Windows (cmd/PowerShell), Linux, and macOS.

Usage:
    python run.py [command]

Commands:
    app         Launch the Streamlit Portal & Dashboard (default)
    data        Generate/enrich student analytics dataset (generate_analytics_data.py)
    train       Train Random Forest ML model and evaluate (machine_learning.py)
    eda         Run Exploratory Data Analysis and generate heatmap (eda.py)
    importance  Calculate and plot feature importances (feature_importance.py)
    process     Run dataset preprocessing pipeline (processing.py)
    test        Execute Playwright E2E automation tests (test_analytics_playwright.py)
    test-all    Execute both Streamlit & Analytics Playwright test suites
    pdf         Compile and regenerate technical documentation PDF
    install     Install Python package dependencies from requirements.txt
    status      Verify environment, model files, and datasets
    help        Display this help message
"""

import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable

def run_cmd(cmd, description=""):
    if description:
        print(f"\n>>> {description}...")
    print(f"[CMD] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(BASE_DIR))
    if result.returncode != 0:
        print(f"[ERROR] Command exited with code {result.returncode}")
        sys.exit(result.returncode)
    return result.returncode

def cmd_app():
    port = os.environ.get("PORT", "8501")
    cmd = [PYTHON, "-m", "streamlit", "run", "app.py", "--server.port", str(port)]
    run_cmd(cmd, f"Starting Streamlit Portal on port {port}")

def cmd_data():
    cmd = [PYTHON, "generate_analytics_data.py"]
    run_cmd(cmd, "Generating Enriched Placement Analytics Dataset")

def cmd_train():
    cmd = [PYTHON, "machine_learning.py"]
    run_cmd(cmd, "Training Random Forest Classifier (200 trees)")

def cmd_eda():
    cmd = [PYTHON, "eda.py"]
    run_cmd(cmd, "Running Exploratory Data Analysis")

def cmd_importance():
    cmd = [PYTHON, "feature_importance.py"]
    run_cmd(cmd, "Computing Feature Importances")

def cmd_process():
    cmd = [PYTHON, "processing.py"]
    run_cmd(cmd, "Running Feature Engineering Preprocessing")

def cmd_test():
    cmd = [PYTHON, "test_analytics_playwright.py"]
    run_cmd(cmd, "Executing Playwright Automated Tests")

def cmd_test_all():
    cmd1 = [PYTHON, "test_analytics_playwright.py"]
    run_cmd(cmd1, "Running Playwright Analytics Dashboard Test")
    cmd2 = [PYTHON, "test_streamlit_playwright.py"]
    run_cmd(cmd2, "Running Playwright Digital Twin Predictor Test")

def cmd_pdf():
    script = BASE_DIR / "scratch" / "generate_pdf_docs.py"
    if not script.exists():
        # Fallback path if in antigravity brain
        brain_script = Path("C:/Users/hp/.gemini/antigravity/brain/3ca3903b-2b83-43a9-923e-a5b90bd7713e/scratch/generate_pdf_docs.py")
        if brain_script.exists():
            script = brain_script
    if script.exists():
        run_cmd([PYTHON, str(script)], "Compiling Documentation PDF")
    else:
        print("[WARN] generate_pdf_docs.py not found in scratch folder.")

def cmd_install():
    req_file = BASE_DIR / "requirements.txt"
    cmd = [PYTHON, "-m", "pip", "install", "-r", str(req_file)]
    run_cmd(cmd, "Installing Dependencies from requirements.txt")

def cmd_status():
    print("\n=======================================================")
    print("Placement Readiness & Analytics Portal - Status Check")
    print("=======================================================")
    print(f"Python Executable : {PYTHON} ({sys.version.split()[0]})")
    print(f"Platform / OS     : {sys.platform}")
    print(f"Base Directory    : {BASE_DIR}")
    print("-------------------------------------------------------")
    
    files_to_check = [
        ("app.py", "Main Portal Application"),
        ("analytics_dashboard.py", "Analytics Dashboard Module"),
        ("placement_model.pkl", "Trained ML Model"),
        ("label_encoder.pkl", "Target Label Encoder"),
        ("student_placement_analytics.csv", "Analytics Dataset (5,000 records)"),
        ("student_dataset_v3.csv", "Baseline Training Dataset"),
        ("student_dataset_v2.csv", "Raw Feature Dataset"),
        ("Placement_Readiness_and_Analytics_Full_Documentation.pdf", "Technical Docs PDF")
    ]
    
    all_ok = True
    for fname, desc in files_to_check:
        p = BASE_DIR / fname
        if p.exists():
            size_kb = p.stat().st_size / 1024
            print(f" [OK] {fname:<45} ({size_kb:>8.1f} KB) - {desc}")
        else:
            print(f" [MISSING] {fname:<45} - {desc}")
            all_ok = False
            
    print("-------------------------------------------------------")
    if all_ok:
        print("[STATUS] All core components are present and verified!")
    else:
        print("[STATUS] Some files are missing. Run 'python run.py data' or 'python run.py train' to regenerate.")
    print("=======================================================\n")

def cmd_help():
    print(__doc__)

def main():
    if len(sys.argv) < 2:
        cmd_app()
        return
        
    arg = sys.argv[1].lower().strip("-")
    commands = {
        "app": cmd_app,
        "run": cmd_app,
        "start": cmd_app,
        "data": cmd_data,
        "train": cmd_train,
        "eda": cmd_eda,
        "importance": cmd_importance,
        "process": cmd_process,
        "test": cmd_test,
        "test-all": cmd_test_all,
        "pdf": cmd_pdf,
        "install": cmd_install,
        "status": cmd_status,
        "help": cmd_help,
        "h": cmd_help
    }
    
    if arg in commands:
        commands[arg]()
    else:
        print(f"Unknown command: '{sys.argv[1]}'")
        cmd_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
