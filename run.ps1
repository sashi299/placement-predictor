<#
.SYNOPSIS
    Turnkey PowerShell Runner for Placement Readiness & Analytics Portal.
.DESCRIPTION
    Launches, trains, tests, and manages the project from Windows PowerShell.
.PARAMETER Target
    The action to execute: app (default), data, train, eda, importance, process, test, install, status, help.
.EXAMPLE
    .\run.ps1
    .\run.ps1 -Target train
    .\run.ps1 -Target test
#>
[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [ValidateSet("app","data","train","eda","importance","process","test","test-all","install","status","help","run","start")]
    [string]$Target = "app"
)

Set-StrictMode -Off
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Auto-detect Python
$PythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $PythonCmd) {
    $PythonCmd = (Get-Command py -ErrorAction SilentlyContinue).Source
}

if (-not $PythonCmd) {
    Write-Error "[ERROR] Python was not found on your system PATH. Please ensure Python is installed."
    exit 1
}

Write-Host ">>> Placement Portal Runner [PowerShell] Target: $Target" -ForegroundColor Cyan

switch ($Target) {
    { $_ -in @("app", "run", "start") } {
        Write-Host "[1/1] Launching Streamlit Portal & Analytics Dashboard..." -ForegroundColor Green
        & $PythonCmd -m streamlit run app.py
    }
    "data" {
        Write-Host "[1/1] Generating Enriched Placement Analytics Dataset..." -ForegroundColor Green
        & $PythonCmd generate_analytics_data.py
    }
    "train" {
        Write-Host "[1/1] Training Random Forest Machine Learning Model..." -ForegroundColor Green
        & $PythonCmd machine_learning.py
    }
    "eda" {
        Write-Host "[1/1] Running Exploratory Data Analysis..." -ForegroundColor Green
        & $PythonCmd eda.py
    }
    "importance" {
        Write-Host "[1/1] Calculating Feature Importances..." -ForegroundColor Green
        & $PythonCmd feature_importance.py
    }
    "process" {
        Write-Host "[1/1] Running Data Preprocessing Pipeline..." -ForegroundColor Green
        & $PythonCmd processing.py
    }
    "test" {
        Write-Host "[1/1] Executing Playwright E2E Automated Tests..." -ForegroundColor Green
        & $PythonCmd test_analytics_playwright.py
    }
    "test-all" {
        Write-Host "[1/2] Running Analytics Dashboard Tests..." -ForegroundColor Green
        & $PythonCmd test_analytics_playwright.py
        Write-Host "[2/2] Running Digital Twin Predictor Tests..." -ForegroundColor Green
        & $PythonCmd test_streamlit_playwright.py
    }
    "install" {
        Write-Host "[1/1] Installing Dependencies from requirements.txt..." -ForegroundColor Green
        & $PythonCmd -m pip install -r requirements.txt
    }
    "status" {
        & $PythonCmd run.py status
    }
    "help" {
        Write-Host @"
===========================================================
 Placement Readiness Portal - PowerShell Usage
===========================================================
  .\run.ps1                     Start the Streamlit Portal (default)
  .\run.ps1 -Target app         Start the Streamlit Portal
  .\run.ps1 -Target data        Generate analytics dataset
  .\run.ps1 -Target train       Train ML model (Random Forest)
  .\run.ps1 -Target eda         Run Exploratory Data Analysis
  .\run.ps1 -Target importance  Calculate feature importances
  .\run.ps1 -Target process     Run preprocessing feature engineering
  .\run.ps1 -Target test        Run Playwright automated tests
  .\run.ps1 -Target test-all    Run all Playwright test suites
  .\run.ps1 -Target install     Install requirements.txt packages
  .\run.ps1 -Target status      Verify component health
  .\run.ps1 -Target help        Display this help message
===========================================================
"@ -ForegroundColor Yellow
    }
}
