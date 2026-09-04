import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("student_placement_analytics.csv")
    return df

def render_analytics_dashboard():
    st.title("📊 Placement Analytics Dashboard")
    st.markdown("Comprehensive insights into **branch-wise placement trends**, **skills analytics**, **recruiting companies**, and **salary distributions**.")
    
    df = load_data()
    
    # ------------------- SIDEBAR FILTERS -------------------
    st.sidebar.markdown("### 🔍 Dashboard Filters")
    
    all_branches = sorted(df["branch"].unique().tolist())
    selected_branches = st.sidebar.multiselect(
        "Select Branch(es):",
        options=all_branches,
        default=all_branches
    )
    
    track_options = ["All Tracks"] + sorted(df["company_track"].unique().tolist())
    selected_track = st.sidebar.selectbox("Filter by Track:", options=track_options)
    
    max_salary_val = float(df["salary_lpa"].max())
    salary_range = st.sidebar.slider(
        "Salary Range (LPA):",
        min_value=0.0,
        max_value=max_salary_val,
        value=(0.0, max_salary_val),
        step=0.5
    )
    
    # Apply filters
    filtered_df = df[df["branch"].isin(selected_branches)].copy()
    if selected_track != "All Tracks":
        filtered_df = filtered_df[filtered_df["company_track"] == selected_track]
        
    filtered_df = filtered_df[
        (filtered_df["salary_lpa"] >= salary_range[0]) & 
        (filtered_df["salary_lpa"] <= salary_range[1])
    ]
    
    placed_filtered = filtered_df[filtered_df["placement_status"] == 1]
    
    if filtered_df.empty:
        st.warning("No student records match the selected filters. Please adjust the filters in the sidebar.")
        return
        
    # ------------------- TOP KPI METRICS -------------------
    total_students = len(filtered_df)
    total_placed = len(placed_filtered)
    placement_rate = (total_placed / total_students * 100) if total_students > 0 else 0
    avg_salary = placed_filtered["salary_lpa"].mean() if not placed_filtered.empty else 0.0
    highest_salary = placed_filtered["salary_lpa"].max() if not placed_filtered.empty else 0.0
    median_salary = placed_filtered["salary_lpa"].median() if not placed_filtered.empty else 0.0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🎓 Total Students", f"{total_students:,}")
    with col2:
        st.metric("✅ Total Placed", f"{total_placed:,}", f"{placement_rate:.1f}% Rate")
    with col3:
        st.metric("💵 Average CTC", f"{avg_salary:.2f} LPA" if avg_salary > 0 else "N/A")
    with col4:
        st.metric("🏆 Highest CTC", f"{highest_salary:.2f} LPA" if highest_salary > 0 else "N/A")
    with col5:
        st.metric("📈 Median CTC", f"{median_salary:.2f} LPA" if median_salary > 0 else "N/A")
        
    st.markdown("---")
    
    # ------------------- TABS -------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏛️ Branch-wise Trends", 
        "💰 Salary Statistics", 
        "💡 Skills Analysis", 
        "🏢 Companies & Recruiters",
        "📋 Data Explorer & Export"
    ])
    
    # ------------------- TAB 1: BRANCH TRENDS -------------------
    with tab1:
        st.subheader("Branch-wise Placement Performance")
        
        branch_stats = filtered_df.groupby("branch").agg(
            Total_Students=("student_id", "count"),
            Placed_Students=("placement_status", lambda x: (x == 1).sum()),
            Unplaced_Students=("placement_status", lambda x: (x == 0).sum())
        ).reset_index()
        branch_stats["Placement_Rate_%"] = (branch_stats["Placed_Students"] / branch_stats["Total_Students"] * 100).round(1)
        
        # Placed branch salaries
        placed_branch = placed_filtered.groupby("branch")["salary_lpa"].agg(
            Avg_CTC_LPA="mean",
            Max_CTC_LPA="max",
            Median_CTC_LPA="median"
        ).round(2).reset_index()
        
        branch_summary = pd.merge(branch_stats, placed_branch, on="branch", how="left").fillna(0)
        branch_summary = branch_summary.sort_values(by="Placement_Rate_%", ascending=False)
        
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            fig_rate = px.bar(
                branch_summary,
                x="branch",
                y="Placement_Rate_%",
                text="Placement_Rate_%",
                title="Placement Rate by Branch (%)",
                color="Placement_Rate_%",
                color_continuous_scale="Blues",
                labels={"Placement_Rate_%": "Placement Rate (%)", "branch": "Branch"}
            )
            fig_rate.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_rate.update_layout(xaxis_tickangle=-30, yaxis_range=[0, 100], height=400)
            st.plotly_chart(fig_rate, use_container_width=True)
            
        with row1_col2:
            fig_headcount = px.bar(
                branch_summary,
                x="branch",
                y=["Placed_Students", "Unplaced_Students"],
                barmode="stack",
                title="Student Distribution: Placed vs Unplaced",
                color_discrete_map={"Placed_Students": "#2ecc71", "Unplaced_Students": "#e74c3c"},
                labels={"value": "Headcount", "branch": "Branch", "variable": "Status"}
            )
            fig_headcount.update_layout(xaxis_tickangle=-30, height=400)
            st.plotly_chart(fig_headcount, use_container_width=True)
            
        st.subheader("Branch Compensation Summary")
        fig_salary_branch = px.bar(
            branch_summary[branch_summary["Avg_CTC_LPA"] > 0],
            x="branch",
            y=["Avg_CTC_LPA", "Median_CTC_LPA"],
            barmode="group",
            title="Average vs Median Package across Branches (LPA)",
            color_discrete_map={"Avg_CTC_LPA": "#3498db", "Median_CTC_LPA": "#9b59b6"},
            labels={"value": "CTC (LPA)", "branch": "Branch", "variable": "Metric"}
        )
        fig_salary_branch.update_layout(xaxis_tickangle=-25, height=380)
        st.plotly_chart(fig_salary_branch, use_container_width=True)
        
        st.dataframe(
            branch_summary.rename(columns={
                "branch": "Branch",
                "Total_Students": "Total Students",
                "Placed_Students": "Placed Count",
                "Unplaced_Students": "Unplaced Count",
                "Placement_Rate_%": "Placement Rate (%)",
                "Avg_CTC_LPA": "Avg CTC (LPA)",
                "Median_CTC_LPA": "Median CTC (LPA)",
                "Max_CTC_LPA": "Highest CTC (LPA)"
            }),
            use_container_width=True,
            hide_index=True
        )

    # ------------------- TAB 2: SALARY STATISTICS -------------------
    with tab2:
        st.subheader("Salary & Compensation Analytics")
        if placed_filtered.empty:
            st.info("No placed students in the current filter selection.")
        else:
            sal_col1, sal_col2 = st.columns(2)
            with sal_col1:
                fig_hist = px.histogram(
                    placed_filtered,
                    x="salary_lpa",
                    nbins=25,
                    title="Salary Distribution for Placed Students (LPA)",
                    color="company_track",
                    marginal="box",
                    color_discrete_map={"Product_Ready": "#f39c12", "Service_Ready": "#2980b9"},
                    labels={"salary_lpa": "Salary (LPA)", "company_track": "Track"}
                )
                fig_hist.update_layout(height=420)
                st.plotly_chart(fig_hist, use_container_width=True)
                
            with sal_col2:
                tier_counts = placed_filtered["salary_tier"].value_counts().reset_index()
                tier_counts.columns = ["Tier", "Count"]
                fig_tier = px.pie(
                    tier_counts,
                    names="Tier",
                    values="Count",
                    title="Offers by Salary Tier",
                    hole=0.45,
                    color="Tier",
                    color_discrete_map={
                        "Super Dream (> 20 LPA)": "#8e44ad",
                        "Dream (10 - 20 LPA)": "#2980b9",
                        "Core / Growth (6 - 10 LPA)": "#27ae60",
                        "Standard / Mass (3.5 - 6 LPA)": "#f39c12"
                    }
                )
                fig_tier.update_layout(height=420)
                st.plotly_chart(fig_tier, use_container_width=True)
                
            st.subheader("Salary Package vs Academic Performance (CGPA)")
            fig_scatter = px.scatter(
                placed_filtered,
                x="cgpa",
                y="salary_lpa",
                color="company_track",
                size="technical_score",
                hover_data=["student_id", "branch", "hiring_company", "primary_skill"],
                title="Salary Package (LPA) vs CGPA (Bubble Size = Technical Score)",
                color_discrete_map={"Product_Ready": "#e67e22", "Service_Ready": "#3498db"},
                labels={"cgpa": "CGPA", "salary_lpa": "Package (LPA)"}
            )
            fig_scatter.update_layout(height=420)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.subheader("🌟 Top Highest Package Offers")
            top_offers = placed_filtered.sort_values(by="salary_lpa", ascending=False).head(10)
            st.dataframe(
                top_offers[["student_id", "branch", "hiring_company", "salary_lpa", "salary_tier", "primary_skill", "cgpa", "coding_score", "dsa_score"]].rename(columns={
                    "student_id": "Student ID",
                    "branch": "Branch",
                    "hiring_company": "Company",
                    "salary_lpa": "CTC (LPA)",
                    "salary_tier": "Tier",
                    "primary_skill": "Primary Skill",
                    "cgpa": "CGPA",
                    "coding_score": "Coding Score",
                    "dsa_score": "DSA Score"
                }),
                use_container_width=True,
                hide_index=True
            )

    # ------------------- TAB 3: SKILLS ANALYSIS -------------------
    with tab3:
        st.subheader("Skills Analytics & Impact on Placement")
        
        skill_col1, skill_col2 = st.columns(2)
        with skill_col1:
            skill_placement = filtered_df.groupby("primary_skill").agg(
                Total=("student_id", "count"),
                Placed=("placement_status", lambda x: (x == 1).sum())
            ).reset_index()
            skill_placement["Placement_Rate_%"] = (skill_placement["Placed"] / skill_placement["Total"] * 100).round(1)
            skill_placement = skill_placement.sort_values(by="Placement_Rate_%", ascending=True)
            
            fig_skill_rate = px.bar(
                skill_placement,
                y="primary_skill",
                x="Placement_Rate_%",
                orientation="h",
                text="Placement_Rate_%",
                title="Placement Rate by Primary Skill Domain (%)",
                color="Placement_Rate_%",
                color_continuous_scale="Greens",
                labels={"Placement_Rate_%": "Placement Rate (%)", "primary_skill": "Skill Domain"}
            )
            fig_skill_rate.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_skill_rate.update_layout(xaxis_range=[0, 100], height=400)
            st.plotly_chart(fig_skill_rate, use_container_width=True)
            
        with skill_col2:
            skill_salaries = placed_filtered.groupby("primary_skill")["salary_lpa"].mean().round(2).reset_index()
            skill_salaries = skill_salaries.sort_values(by="salary_lpa", ascending=False)
            
            fig_skill_sal = px.bar(
                skill_salaries,
                x="primary_skill",
                y="salary_lpa",
                text="salary_lpa",
                title="Average Salary by Primary Skill (LPA)",
                color="salary_lpa",
                color_continuous_scale="Purples",
                labels={"salary_lpa": "Avg CTC (LPA)", "primary_skill": "Skill Domain"}
            )
            fig_skill_sal.update_traces(texttemplate="%{text:.1f} LPA", textposition="outside")
            fig_skill_sal.update_layout(xaxis_tickangle=-25, height=400)
            st.plotly_chart(fig_skill_sal, use_container_width=True)
            
        st.subheader("Skill Benchmark: Placed vs Unplaced Students")
        skill_cols = ["coding_score", "dsa_score", "sql_score", "python_score", "dbms_score", "os_score", "communication_score", "aptitude_score"]
        labels_map = {
            "coding_score": "Coding", "dsa_score": "DSA", "sql_score": "SQL", "python_score": "Python",
            "dbms_score": "DBMS", "os_score": "OS", "communication_score": "Communication", "aptitude_score": "Aptitude"
        }
        
        placed_means = filtered_df[filtered_df["placement_status"] == 1][skill_cols].mean().round(1)
        unplaced_means = filtered_df[filtered_df["placement_status"] == 0][skill_cols].mean().round(1)
        
        radar_df = pd.DataFrame({
            "Skill": [labels_map[c] for c in skill_cols],
            "Placed Students": placed_means.values,
            "Unplaced Students": unplaced_means.values
        })
        
        fig_comparison = px.bar(
            radar_df,
            x="Skill",
            y=["Placed Students", "Unplaced Students"],
            barmode="group",
            title="Average Skill Scores Comparison (Out of 100)",
            color_discrete_map={"Placed Students": "#2ecc71", "Unplaced Students": "#95a5a6"},
            labels={"value": "Mean Score", "variable": "Cohort"}
        )
        fig_comparison.update_layout(height=400)
        st.plotly_chart(fig_comparison, use_container_width=True)

    # ------------------- TAB 4: COMPANIES & RECRUITERS -------------------
    with tab4:
        st.subheader("Recruiter Insights & Company Trends")
        if placed_filtered.empty:
            st.info("No placed students in the current selection.")
        else:
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                company_counts = placed_filtered["hiring_company"].value_counts().reset_index()
                company_counts.columns = ["Company", "Offers"]
                fig_company = px.bar(
                    company_counts,
                    x="Offers",
                    y="Company",
                    orientation="h",
                    title="Total Student Hires by Company",
                    color="Offers",
                    color_continuous_scale="Viridis",
                    labels={"Offers": "Number of Placed Students", "Company": "Company"}
                )
                fig_company.update_layout(yaxis={'categoryorder':'total ascending'}, height=420)
                st.plotly_chart(fig_company, use_container_width=True)
                
            with comp_col2:
                company_salaries = placed_filtered.groupby("hiring_company")["salary_lpa"].mean().round(2).reset_index()
                company_salaries.columns = ["Company", "Avg_CTC_LPA"]
                fig_comp_sal = px.bar(
                    company_salaries.sort_values(by="Avg_CTC_LPA", ascending=True),
                    x="Avg_CTC_LPA",
                    y="Company",
                    orientation="h",
                    title="Average CTC Offered per Company (LPA)",
                    color="Avg_CTC_LPA",
                    color_continuous_scale="Plasma",
                    labels={"Avg_CTC_LPA": "Average CTC (LPA)", "Company": "Company"}
                )
                fig_comp_sal.update_layout(yaxis={'categoryorder':'total ascending'}, height=420)
                st.plotly_chart(fig_comp_sal, use_container_width=True)
                
            st.subheader("Company vs Branch Hiring Heatmap")
            comp_branch_crosstab = pd.crosstab(placed_filtered["hiring_company"], placed_filtered["branch"])
            fig_heatmap = px.imshow(
                comp_branch_crosstab,
                labels=dict(x="Branch", y="Recruiting Company", color="Hires Count"),
                x=comp_branch_crosstab.columns,
                y=comp_branch_crosstab.index,
                color_continuous_scale="YlGnBu",
                title="Recruiting Company Hiring Volume Across Branches"
            )
            fig_heatmap.update_layout(height=450)
            st.plotly_chart(fig_heatmap, use_container_width=True)

    # ------------------- TAB 5: DATA EXPLORER & EXPORT -------------------
    with tab5:
        st.subheader("Student Placement Records Explorer")
        st.markdown(f"Showing **{len(filtered_df):,}** student records matching current filters.")
        
        display_columns = [
            "student_id", "branch", "placement_status", "company_track", 
            "hiring_company", "salary_lpa", "salary_tier", "primary_skill", 
            "cgpa", "technical_score", "communication_score", "projects_count"
        ]
        
        st.dataframe(
            filtered_df[display_columns].rename(columns={
                "student_id": "Student ID",
                "branch": "Branch",
                "placement_status": "Placed (1/0)",
                "company_track": "Track",
                "hiring_company": "Hiring Company",
                "salary_lpa": "CTC (LPA)",
                "salary_tier": "Salary Tier",
                "primary_skill": "Primary Skill",
                "cgpa": "CGPA",
                "technical_score": "Technical Score",
                "communication_score": "Comm Score",
                "projects_count": "Projects"
            }),
            use_container_width=True,
            hide_index=True
        )
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="placement_analytics_filtered.csv",
            mime="text/csv"
        )
