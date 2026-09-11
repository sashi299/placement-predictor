# 🎓 Placement Readiness Digital Twin & Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Plotly Visualizations](https://img.shields.io/badge/Visualizations-Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
[![Scikit-Learn ML](https://img.shields.io/badge/ML-Random%20Forest-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

An AI-driven student placement intelligence platform combining a **Machine Learning Digital Twin predictor** with an executive **7-Tab Analytics Dashboard** built with Streamlit, Plotly, Pandas, and Scikit-Learn.

---

## ⚡ Quick Understanding: The 3 Datasets at a Glance

### 1. Student Placement Dataset (`student_placement_analytics.csv` — 5,000 records)
Tracks student academic performance, technical scores across 8 skill dimensions, and placement results.

| Student ID | Branch | Placement Status | Company Track | Hiring Company | CTC (LPA) | Primary Skill | CGPA | Technical Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S00001** | Computer Science (CSE) | Placed (1) | Product_Ready | Amazon | 43.05 LPA | Data Structures & Algorithms | 6.33 | 70.25 |
| **S00002** | Electrical Engg (EEE) | Placed (1) | Service_Ready | Cognizant | 8.39 LPA | Full Stack Web Development | 8.25 | 71.00 |
| **S00003** | Electrical Engg (EEE) | Unplaced (0) | Not_Placed | Not Placed | 0.00 LPA | Full Stack Web Development | 5.79 | 53.50 |

---

### 2. Recruiter Benchmarks (`recruiter_requirements.csv` — 14 top employers)
Defines minimum score thresholds and CGPA cutoffs for top product & IT services recruiters.

| Company | Min CGPA | Coding Benchmark | DSA Benchmark | SQL Benchmark | Python Benchmark | Aptitude Benchmark | Comm Benchmark |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Google** | 8.0 | 85 | 85 | 70 | 75 | 80 | 75 |
| **Microsoft** | 7.5 | 80 | 85 | 70 | 70 | 75 | 75 |
| **Amazon** | 7.5 | 80 | 80 | 70 | 70 | 75 | 70 |
| **TCS** | 6.5 | 55 | 50 | 50 | 50 | 65 | 60 |
| **Accenture** | 6.5 | 55 | 50 | 55 | 50 | 65 | 65 |

---

### 3. Alumni Career Outcomes (`alumni_outcomes.csv` — 1,400 alumni)
Tracks 1–5 year post-placement career trajectory, promotions, salary compounding, and company switches.

| Student ID | Experience | Initial Company | Current Company | Starting CTC | Current CTC | Promotions | Switched Company |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S00687** | 2 Years | Microsoft | Microsoft | 44.50 LPA | 63.84 LPA | 1 | No |
| **S04418** | 1 Year | Amazon | Uber | 41.20 LPA | 67.30 LPA | 1 | Yes |
| **S04086** | 5 Years | TCS | TCS | 7.20 LPA | 26.00 LPA | 4 | Yes |
| **S03483** | 2 Years | Infosys | Infosys | 6.80 LPA | 13.24 LPA | 1 | No |

---

## 🧭 Dashboard Modules & Tabs Overview

```
Placement Portal (app.py)
 ├── 🎯 Placement Readiness Digital Twin
 │    └── ML Random Forest predictor (Readiness Score 0-100, Confidence, Product/Service company fit)
 │
 └── 📊 Placement Analytics Dashboard (analytics_dashboard.py)
      ├── Tab 1: 🏛️ Branch-wise Trends (Placement rate %, CTC comparison by branch)
      ├── Tab 2: 💰 Salary Statistics (CTC distributions, Tier breakdown, CGPA correlation)
      ├── Tab 3: 💡 Skills Analysis (High-impact skills, placed vs unplaced score comparison)
      ├── Tab 4: 🏢 Companies & Recruiters (Hiring volume, average CTC, branch-company heatmap)
      ├── Tab 5: 🎯 Skill-Gap Recommender (Individual student vs company benchmark gap & fit)
      ├── Tab 6: 🎓 Alumni Outcome Tracker (1-5 yr career trajectory, salary growth curves, switches)
      └── Tab 7: 📋 Data Explorer & Export (Live filtered dataset table & 1-click CSV download)
```

---

## 🛠️ Technologies Used

- **Python** 3.10+
- **Streamlit** (Interactive web application)
- **Plotly Express & Graph Objects** (Interactive data visualizations)
- **Pandas & NumPy** (Data processing and analytics)
- **Scikit-Learn** (Random Forest classifier & Label Encoder)
- **Joblib** (Model serialization)
- **Playwright** (Automated end-to-end testing)

## 🏃 Run Anywhere (Cross-Platform)

This project is fully platform-independent and provides native, 1-click runners for **Windows Command Prompt**, **Windows PowerShell**, **Linux**, **macOS**, and **Python CLI**:

### 1. Windows Command Prompt (`cmd.exe`)
```cmd
:: Start Streamlit Portal & Dashboard (Default)
run.bat

:: Or run specific tasks:
run.bat test        :: Run Playwright automated tests
run.bat train       :: Train Random Forest ML model
run.bat data        :: Generate analytics dataset
run.bat eda         :: Run Exploratory Data Analysis
run.bat importance  :: Calculate feature importances
run.bat status      :: Check file health & environment
```

### 2. Windows PowerShell
```powershell
# Start Streamlit Portal & Dashboard (Default)
.\run.ps1

# Or run specific tasks:
.\run.ps1 -Target test
.\run.ps1 -Target train
.\run.ps1 -Target data
.\run.ps1 -Target eda
.\run.ps1 -Target importance
.\run.ps1 -Target status
```

### 3. Universal Python CLI (Windows, Linux, macOS)
```bash
# Start Streamlit Portal (Default)
python run.py

# Task commands:
python run.py test        # Playwright E2E tests
python run.py train       # Retrain Random Forest model
python run.py data        # Generate analytics dataset
python run.py eda         # Run EDA heatmap analysis
python run.py importance  # Calculate feature importances
python run.py status      # Check component health
```

### 4. Linux & macOS (`bash`)
```bash
chmod +x run.sh
./run.sh                  # Start Portal
./run.sh test             # Run automated tests
./run.sh train            # Train ML model
```
