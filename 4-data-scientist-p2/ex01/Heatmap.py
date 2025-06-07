import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../Train_knight.csv")
df["knight"] = df["knight"].map({"Jedi": 0, "Sith": 1})
corr_matrix = df.corr(numeric_only=True)

plt.figure(figsize=(10, 10))
sns.heatmap(
    corr_matrix,
    cmap="magma",
    center=0,
    annot=False,
    square=True,
    linewidths=0,
    cbar_kws={"shrink": 0.8}
)

plt.tight_layout()
plt.savefig("heatmap.png")