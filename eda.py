import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(BASE_DIR / "student_dataset_v3.csv")
numeric_df = df.select_dtypes(include=["int64", "float64"])

plt.figure(figsize=(15,10))
sns.heatmap(
    numeric_df.corr(),
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
output_chart = BASE_DIR / "eda_correlation_heatmap.png"
plt.savefig(output_chart, dpi=150)
plt.close()
print(f"EDA Correlation Heatmap saved to: {output_chart}")