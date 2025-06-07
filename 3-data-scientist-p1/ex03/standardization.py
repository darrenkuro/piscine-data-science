import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

TRAIN_PATH = "Train_knight.csv"

try:
    df_train = pd.read_csv(TRAIN_PATH)

    # Separate features and target
    features = df_train.drop(columns=["knight"])
    target = df_train["knight"]

    # Standardize features
    scaler = StandardScaler()
    standardized = scaler.fit_transform(features)

    df_std = pd.DataFrame(standardized, columns=features.columns)
    df_std["knight"] = target

    print(df_std)

    df_jedi = df_std[df_std["knight"] == "Jedi"]
    df_sith = df_std[df_std["knight"] == "Sith"]

    x_col = "Empowered"
    y_col = "Stims"

    plt.figure(figsize=(6, 5))
    plt.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    plt.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.tight_layout()
    plt.savefig("plot.png")

except Exception as e:
    print(f"Error: {e}")