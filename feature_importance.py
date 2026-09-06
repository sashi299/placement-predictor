import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load model and dataset features
model = joblib.load(BASE_DIR / "placement_model.pkl")
df = pd.read_csv(BASE_DIR / "student_dataset_v3.csv")
feature_cols = [c for c in df.columns if c not in ["student_id", "placement_status", "company_track"]]

feature_importance = pd.DataFrame({
    "feature": feature_cols,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("Top 15 Feature Importances:")
print(feature_importance.head(15).to_string(index=False))

plt.figure(figsize=(10,6))
plt.barh(
    feature_importance["feature"][:15],
    feature_importance["importance"][:15]
)
plt.title("Top Feature Importances")
plt.tight_layout()
output_chart = BASE_DIR / "feature_importance.png"
plt.savefig(output_chart, dpi=150)
plt.close()
print(f"Feature importance chart saved to: {output_chart}")