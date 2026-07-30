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
plt.show()