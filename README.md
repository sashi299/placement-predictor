# Placement Readiness Digital Twin & Analytics Dashboard

An AI-powered student placement portal featuring interactive Machine Learning predictions and an executive **Placement Analytics Dashboard** built with Streamlit and Plotly.

## 🚀 Key Modules

### 1. 📊 Placement Analytics Dashboard
- **Branch-wise Placement Trends**: Track placement rates (%), headcount distribution (Placed vs Unplaced), and average/median CTC across engineering branches (CSE, IT, ECE, AI/DS, EEE, ME).
- **Salary Statistics**: Comprehensive CTC distributions (LPA), salary tier categorization (Super Dream >20 LPA, Dream 10-20 LPA, Core 6-10 LPA, Mass/Standard 3.5-6 LPA), and CGPA-to-package correlation.
- **Skills Analytics**: Primary skill domain impact on placement rates and compensation, plus skill benchmark comparisons between placed and unplaced cohorts.
- **Recruiter & Company Insights**: Total hires and average CTC per company (Product leaders like Google, Microsoft, Amazon, Adobe vs Service leaders like TCS, Infosys, Wipro, Accenture), plus branch-to-company hiring heatmaps.
- **Interactive Multi-filtering & Data Export**: Dynamic branch, track, and salary range filters with full dataset CSV export.

### 2. 🎯 Placement Readiness Digital Twin
- Individual student readiness prediction using a trained Random Forest model.
- Readiness score (0-100) and confidence breakdown.
- Multi-company fit analysis (Product & Service company match percentages).

## 🛠️ Technologies Used

- **Python** 3.10+
- **Streamlit** (Interactive web application)
- **Plotly Express & Graph Objects** (Interactive data visualizations)
- **Pandas & NumPy** (Data processing and analytics)
- **Scikit-Learn** (Random Forest classifier & Label Encoder)
- **Joblib** (Model serialization)
- **Playwright** (Automated end-to-end testing)

## 🏃 Run Locally

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```