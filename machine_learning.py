import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "student_dataset_v3.csv")

X = df.drop(
    columns=[
        "student_id",
        "placement_status",
        "company_track"
    ]
)

y = df["company_track"]

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

y = le.fit_transform(y)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

import joblib

joblib.dump(model, BASE_DIR / "placement_model.pkl")
joblib.dump(le, BASE_DIR / "label_encoder.pkl")

print("Model saved successfully!")

y_pred = model.predict(X_test)

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))

import pandas as pd
import matplotlib.pyplot as plt

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print(feature_importance.head(15))

plt.figure(figsize=(10,6))
plt.barh(
    feature_importance["feature"][:15],
    feature_importance["importance"][:15]
)
plt.title("Top Feature Importances")
plt.tight_layout()
plt.savefig(BASE_DIR / "feature_importance_training.png", dpi=150)
plt.close()

df["placement_readiness_score"] = (
    0.20 * df["technical_score"] +
    0.15 * df["communication_score"] +
    0.15 * df["aptitude_score"] +
    0.10 * df["core_cs_score"] +
    0.15 * df["resume_strength"] +
    0.15 * (df["cgpa"] * 10) -
    0.10 * (df["active_backlogs"] * 10)
)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

df["placement_readiness_score"] = scaler.fit_transform(
    df[["placement_readiness_score"]]
) * 100

import joblib

# joblib.dump(model, "placement_model.pkl")
#
# print("Model Saved!")

joblib.dump(le, "label_encoder.pkl")

print(X.columns.tolist())