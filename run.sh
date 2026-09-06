#!/usr/bin/env bash
# =======================================================
# Placement Readiness & Analytics Portal - Linux/macOS Runner
# =======================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Auto-detect python3 / python
if command -v python3 &>/dev/null; then
    PY="python3"
elif command -v python &>/dev/null; then
    PY="python"
else
    echo "[ERROR] Python 3 was not found. Please install Python."
    exit 1
fi

TARGET="${1:-app}"

case "$TARGET" in
    app|run|start)
        echo "[INFO] Starting Placement Portal & Analytics Dashboard..."
        $PY -m streamlit run app.py
        ;;
    data)
        echo "[INFO] Generating Analytics Dataset..."
        $PY generate_analytics_data.py
        ;;
    train)
        echo "[INFO] Training Random Forest Machine Learning Model..."
        $PY machine_learning.py
        ;;
    eda)
        echo "[INFO] Running Exploratory Data Analysis..."
        $PY eda.py
        ;;
    importance)
        echo "[INFO] Calculating Feature Importances..."
        $PY feature_importance.py
        ;;
    process)
        echo "[INFO] Running Data Preprocessing Pipeline..."
        $PY processing.py
        ;;
    test)
        echo "[INFO] Executing Playwright Automated Tests..."
        $PY test_analytics_playwright.py
        ;;
    test-all)
        echo "[INFO] Executing All Playwright Automated Tests..."
        $PY test_analytics_playwright.py
        $PY test_streamlit_playwright.py
        ;;
    install)
        echo "[INFO] Installing Dependencies..."
        $PY -m pip install -r requirements.txt
        ;;
    status)
        $PY run.py status
        ;;
    help|--help|-h)
        echo "======================================================="
        echo "Placement Readiness Portal - Bash Runner (Linux/macOS)"
        echo "======================================================="
        echo "  ./run.sh            - Start the Streamlit Portal (default)"
        echo "  ./run.sh app        - Start the Streamlit Portal"
        echo "  ./run.sh data       - Generate analytics dataset"
        echo "  ./run.sh train      - Train ML model"
        echo "  ./run.sh eda        - Run Exploratory Data Analysis"
        echo "  ./run.sh importance - Calculate feature importances"
        echo "  ./run.sh process    - Run dataset preprocessing"
        echo "  ./run.sh test       - Run Playwright automated tests"
        echo "  ./run.sh install    - Install requirements"
        echo "  ./run.sh status     - Check component status"
        echo "======================================================="
        ;;
    *)
        echo "Unknown command: $TARGET"
        $PY run.py help
        exit 1
        ;;
esac
