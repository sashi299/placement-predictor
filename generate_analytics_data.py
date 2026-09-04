import pandas as pd
import numpy as np

np.random.seed(42)

df = pd.read_csv("student_dataset_v3.csv")

branches = ["Computer Science (CSE)", "Information Technology (IT)", "Electronics & Comm (ECE)", 
            "Data Science & AI (AI/DS)", "Electrical Engg (EEE)", "Mechanical Engg (ME)"]

# Branch assignment correlated with CS interest/scores
def assign_branch(row):
    tech_affinity = (row["coding_score"] + row["dsa_score"] + row["python_score"]) / 3.0
    if tech_affinity >= 65:
        probs = [0.40, 0.25, 0.15, 0.15, 0.03, 0.02]
    elif tech_affinity >= 45:
        probs = [0.25, 0.25, 0.20, 0.15, 0.08, 0.07]
    else:
        probs = [0.15, 0.15, 0.25, 0.10, 0.20, 0.15]
    return np.random.choice(branches, p=probs)

df["branch"] = df.apply(assign_branch, axis=1)

product_companies = ["Google", "Microsoft", "Amazon", "Adobe", "Atlassian", "Uber", "Cisco"]
service_companies = ["TCS", "Infosys", "Wipro", "Accenture", "Cognizant", "Capgemini", "LTI Mindtree"]

def assign_company_and_salary(row):
    track = row["company_track"]
    status = row["placement_status"]
    
    if status == 0 or track == "Not_Placed":
        return pd.Series(["Not Placed", 0.0, "Unplaced"])
    
    if track == "Product_Ready":
        company = np.random.choice(product_companies, p=[0.18, 0.20, 0.22, 0.14, 0.10, 0.08, 0.08])
        # Base salary between 12 and 45 LPA based on dsa, coding, and cgpa
        base = 12.0 + (row["dsa_score"] * 0.15) + (row["coding_score"] * 0.12) + (row["cgpa"] * 0.8)
        # add slight variance
        salary = base + np.random.uniform(-2.0, 3.5)
        salary = round(min(45.0, max(11.0, salary)), 2)
    else:
        company = np.random.choice(service_companies, p=[0.24, 0.22, 0.18, 0.16, 0.10, 0.05, 0.05])
        # Base salary between 3.6 and 9.0 LPA
        base = 3.6 + (row["aptitude_score"] * 0.02) + (row["communication_score"] * 0.02) + (row["cgpa"] * 0.2)
        salary = base + np.random.uniform(-0.5, 1.2)
        salary = round(min(9.5, max(3.5, salary)), 2)
        
    if salary >= 20.0:
        tier = "Super Dream (> 20 LPA)"
    elif salary >= 10.0:
        tier = "Dream (10 - 20 LPA)"
    elif salary >= 6.0:
        tier = "Core / Growth (6 - 10 LPA)"
    else:
        tier = "Standard / Mass (3.5 - 6 LPA)"
        
    return pd.Series([company, salary, tier])

df[["hiring_company", "salary_lpa", "salary_tier"]] = df.apply(assign_company_and_salary, axis=1)

# Primary skill assignment based on relative profile strengths
def assign_primary_skill(row):
    skills = {
        "Data Structures & Algorithms": row["dsa_score"] * 1.1,
        "Full Stack Web Development": (row["coding_score"] + row["sql_score"]) / 2.0 + row["projects_count"] * 3,
        "Machine Learning & Data Science": (row["python_score"] + row["sql_score"]) / 2.0,
        "Cloud & DevOps": (row["os_score"] + row["core_cs_score"]) / 2.0,
        "Systems & Core CS": row["core_cs_score"] * 1.05,
        "Tech Consulting & Analytics": (row["aptitude_score"] + row["communication_score"]) / 2.0
    }
    return max(skills, key=skills.get)

df["primary_skill"] = df.apply(assign_primary_skill, axis=1)

output_file = "student_placement_analytics.csv"
df.to_csv(output_file, index=False)
print(f"Enriched analytics dataset saved to {output_file} with shape {df.shape}")
print("Sample summary:")
print(df[["student_id", "branch", "placement_status", "company_track", "hiring_company", "salary_lpa", "salary_tier", "primary_skill"]].head())
