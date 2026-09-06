import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from analytics_dashboard import render_analytics_dashboard

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Placement Portal & Digital Twin",
    page_icon="🎓",
    layout="wide"
)

# ------------------- SIDEBAR NAVIGATION -------------------
st.sidebar.title("🎓 Placement Portal")
page = st.sidebar.radio(
    "Navigate To:",
    ["📊 Placement Analytics Dashboard", "🎯 Placement Readiness Digital Twin"],
    index=0
)

st.sidebar.markdown("---")

if page == "📊 Placement Analytics Dashboard":
    render_analytics_dashboard()

else:
    # ------------------- DIGITAL TWIN PREDICTOR -------------------
    model = joblib.load(BASE_DIR / "placement_model.pkl")
    le = joblib.load(BASE_DIR / "label_encoder.pkl")
    
    st.title("Placement Readiness Digital Twin")
    st.write("Predict student placement readiness and company fit.")

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        cgpa = st.slider("CGPA", 5.0, 10.0, 7.0)
        aptitude_score = st.slider("Aptitude Score", 0, 100, 50)
        coding_score = st.slider("Coding Score", 0, 100, 50)
        dsa_score = st.slider("DSA Score", 0, 100, 50)
    with col_input2:
        communication_score = st.slider("Communication Score", 0, 100, 50)
        projects_count = st.slider("Projects Count", 0, 10, 2)
        internship_count = st.slider("Internships", 0, 5, 0)
        active_backlogs = st.slider("Active Backlogs", 0, 5, 0)

    if st.button("Predict Placement Readiness"):
        # Temporary values for missing features
        tenth_percentage = 75
        twelfth_percentage = 75

        dbms_score = 50
        os_score = 50
        oops_score = 50
        sql_score = 50
        python_score = 50

        project_quality_score = 50
        certifications_count = 2
        hackathon_count = 0

        mock_interview_score = 50
        learning_hours_per_week = 10

        technical_score = (
            coding_score +
            dsa_score +
            sql_score +
            python_score
        ) / 4

        core_cs_score = (
            dbms_score +
            os_score +
            oops_score
        ) / 3

        resume_strength = (
            projects_count * 2 +
            certifications_count +
            internship_count * 3 +
            hackathon_count
        )

        input_data = pd.DataFrame([{
            "tenth_percentage": tenth_percentage,
            "twelfth_percentage": twelfth_percentage,
            "cgpa": cgpa,
            "active_backlogs": active_backlogs,
            "aptitude_score": aptitude_score,
            "coding_score": coding_score,
            "dsa_score": dsa_score,
            "dbms_score": dbms_score,
            "os_score": os_score,
            "oops_score": oops_score,
            "sql_score": sql_score,
            "python_score": python_score,
            "communication_score": communication_score,
            "projects_count": projects_count,
            "project_quality_score": project_quality_score,
            "certifications_count": certifications_count,
            "internship_count": internship_count,
            "hackathon_count": hackathon_count,
            "mock_interview_score": mock_interview_score,
            "learning_hours_per_week": learning_hours_per_week,
            "technical_score": technical_score,
            "core_cs_score": core_cs_score,
            "resume_strength": resume_strength
        }])

        prediction = model.predict(input_data)
        track = le.inverse_transform(prediction)[0]
        readiness_score = (
            aptitude_score * 0.20 +
            coding_score * 0.15 +
            dsa_score * 0.15 +
            communication_score * 0.20 +
            cgpa * 5 +
            internship_count * 5 -
            active_backlogs * 10
        )

        readiness_score = max(0, min(100, readiness_score))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Prediction Result")
            st.success(f"Predicted Track: {track}")
        with col2:
            st.metric("Readiness Score", f"{readiness_score:.1f}/100")

        if readiness_score >= 80:
            st.success("Excellent Placement Readiness")
        elif readiness_score >= 60:
            st.warning("Good Placement Readiness")
        else:
            st.error("Needs Improvement")

        probabilities = model.predict_proba(input_data)[0]

        st.subheader("Prediction Confidence")
        for cls, prob in zip(le.classes_, probabilities):
            st.write(f"{cls}: {prob * 100:.2f}%")
            st.progress(float(prob))

        st.subheader("Top Company Matches")
        companies = {}

        # Service Companies
        companies["TCS"] = (
            aptitude_score * 0.4 +
            communication_score * 0.4 +
            cgpa * 2
        )

        companies["Infosys"] = (
            aptitude_score * 0.35 +
            communication_score * 0.35 +
            coding_score * 0.2
        )

        companies["Wipro"] = (
            aptitude_score * 0.4 +
            communication_score * 0.3 +
            coding_score * 0.2
        )

        companies["Accenture"] = (
            aptitude_score * 0.3 +
            communication_score * 0.3 +
            coding_score * 0.2 +
            cgpa * 2
        )

        # Product Companies
        companies["Amazon"] = (
            dsa_score * 0.45 +
            coding_score * 0.35 +
            projects_count * 2
        )

        companies["Google"] = (
            dsa_score * 0.50 +
            coding_score * 0.40 +
            projects_count * 2
        )

        companies["Microsoft"] = (
            dsa_score * 0.40 +
            coding_score * 0.40 +
            communication_score * 0.10
        )

        companies["Adobe"] = (
            dsa_score * 0.40 +
            coding_score * 0.35 +
            project_quality_score * 0.15
        )

        for company in companies:
            companies[company] = round(min(100, companies[company]), 2)
            
        sorted_companies = sorted(
            companies.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for company, score in sorted_companies:
            st.write(f"{company}: {score:.1f}%")
            st.progress(score / 100)
