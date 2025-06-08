import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FILE_TRAIN = "../Train_knight.csv"

try:
    df = pd.read_csv(FILE_TRAIN)
    df["knight"] = df["knight"].map({"Jedi": 0, "Sith": 1})

    plt.figure(figsize=(10, 10))
    sns.heatmap(
        df.corr(),
        cmap="magma",
        center=0,
        annot=False,
        square=True,
        linewidths=0,
        cbar_kws={"shrink": 0.8}
    )

    plt.tight_layout()
    plt.savefig("heatmap.png")
    plt.close()
except Exception as e:
    print(f"Error: {e}")
    exit(1)