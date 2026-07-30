
import pandas as pd

df = pd.read_csv("student_dataset_v2.csv")


df["technical_score"] = (
    df["coding_score"] +
    df["dsa_score"] +
    df["sql_score"] +
    df["python_score"]
) / 4

df["core_cs_score"] = (
    df["dbms_score"] +
    df["os_score"] +
    df["oops_score"]
) / 3

df["resume_strength"] = (
    df["projects_count"] * 2 +
    df["certifications_count"] +
    df["internship_count"] * 3 +
    df["hackathon_count"]
)

df["resume_strength"] = (
    df["projects_count"] * 2 +
    df["certifications_count"] +
    df["internship_count"] * 3 +
    df["hackathon_count"]
)

print(df[[
    "technical_score",
    "core_cs_score",
    "resume_strength"
]].head(20))

df.to_csv("student_dataset_v3.csv", index=False)