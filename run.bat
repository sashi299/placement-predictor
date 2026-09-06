@echo off
setlocal enabledelayedexpansion

REM =======================================================
REM Placement Readiness & Analytics Portal - Windows CMD Runner
REM =======================================================

cd /d "%~dp0"

REM Find python executable
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY=python"
    goto :EXEC
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY=py"
    goto :EXEC
)

echo [ERROR] Python not found in PATH. Please install Python or add it to PATH.
exit /b 1

:EXEC
if "%~1"=="" goto :DEFAULT
if /i "%~1"=="app" goto :APP
if /i "%~1"=="data" goto :DATA
if /i "%~1"=="train" goto :TRAIN
if /i "%~1"=="eda" goto :EDA
if /i "%~1"=="importance" goto :IMPORTANCE
if /i "%~1"=="process" goto :PROCESS
if /i "%~1"=="test" goto :TEST
if /i "%~1"=="install" goto :INSTALL
if /i "%~1"=="status" goto :STATUS
if /i "%~1"=="help" goto :HELP

echo Unknown command: %~1
goto :HELP

:DEFAULT
:APP
echo [INFO] Starting Placement Portal & Analytics Dashboard...
%PY% -m streamlit run app.py
goto :EOF

:DATA
echo [INFO] Generating Analytics Dataset...
%PY% generate_analytics_data.py
goto :EOF

:TRAIN
echo [INFO] Training Random Forest Machine Learning Model...
%PY% machine_learning.py
goto :EOF

:EDA
echo [INFO] Running Exploratory Data Analysis...
%PY% eda.py
goto :EOF

:IMPORTANCE
echo [INFO] Calculating Feature Importances...
%PY% feature_importance.py
goto :EOF

:PROCESS
echo [INFO] Running Preprocessing Feature Engineering...
%PY% processing.py
goto :EOF

:TEST
echo [INFO] Executing Playwright E2E Automation Tests...
%PY% test_analytics_playwright.py
goto :EOF

:INSTALL
echo [INFO] Installing Dependencies from requirements.txt...
%PY% -m pip install -r requirements.txt
goto :EOF

:STATUS
%PY% run.py status
goto :EOF

:HELP
echo =======================================================
echo Placement Readiness Portal - Commands Reference (CMD)
echo =======================================================
echo   run.bat            - Start the Streamlit Portal (default)
echo   run.bat app        - Start the Streamlit Portal
echo   run.bat data       - Generate analytics dataset
echo   run.bat train      - Train Random Forest ML model
echo   run.bat eda        - Run Exploratory Data Analysis
echo   run.bat importance - Calculate Feature Importances
echo   run.bat process    - Run dataset preprocessing
echo   run.bat test       - Execute Playwright automated tests
echo   run.bat install    - Install requirements.txt packages
echo   run.bat status     - Verify project file health
echo   run.bat help       - Display this help message
echo =======================================================
goto :EOF
