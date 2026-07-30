import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("student_dataset_v3.csv")

numeric_df = df.select_dtypes(include=["int64", "float64"])

plt.figure(figsize=(15,10))

sns.heatmap(
    numeric_df.corr(),
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.show()