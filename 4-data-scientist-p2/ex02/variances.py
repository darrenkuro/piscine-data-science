from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FILE_TRAIN = "../Train_knight.csv"

try:
    df = pd.read_csv(FILE_TRAIN)
    df["knight"] = df["knight"].map({"Jedi": 0, "Sith": 1})
    X_scaled = StandardScaler().fit_transform(df)

    pca = PCA()
    pca.fit(X_scaled)

    explained_var = pca.explained_variance_ratio_ * 100 # To percentage
    cumulative_var = explained_var.cumsum()

    print("Variances (Percentage):")
    print(explained_var)
    print("\n")

    print("Cumulative Variance (Percentage):")
    print(cumulative_var)
    print("\n")

    n_components_90 = (cumulative_var < 90).sum() + 1
    print(f"Components needed to reach 90% variance: {n_components_90}")

    plt.figure(figsize=(8, 5))
    plt.plot(np.arange(1, len(cumulative_var) + 1), cumulative_var)
    plt.xlabel('Number of components')
    plt.ylabel('Explained variance (%)')

    plt.tight_layout()
    plt.savefig("variance.png")
    plt.close()

except Exception as e:
    print(f"Error: {e}")
    exit(1)