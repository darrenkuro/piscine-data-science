import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

FILE_TRAIN = "../Train_knight.csv"
FILE_TEST = "../Test_knight.csv"

try:
    df_train = pd.read_csv(FILE_TRAIN)
    df_test = pd.read_csv(FILE_TEST)

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

    # Separate features and target
    features = df_train.drop(columns=["knight"])
    target = df_train["knight"]

    # Standardize features
    scaler = StandardScaler()
    standardized = scaler.fit_transform(features)

    df_std = pd.DataFrame(standardized, columns=features.columns)
    df_std["knight"] = target
    # df_test_std = pd.DataFrame(standardized, columns=df_test.columns)

    print(df_std)

    df_jedi = df_std[df_std["knight"] == "Jedi"]
    df_sith = df_std[df_std["knight"] == "Sith"]
    # df_test = df_test_std

    x_col = "Empowered"
    y_col = "Stims"

    plt.figure(figsize=(6, 5))
    ax1 = axes[0, 0]
    ax1.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    ax1.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")
    ax1.xlabel(x_col)
    ax1.ylabel(y_col)
    ax1.legend()

    # ax2 = axes[1, 0]
    # ax2.scatter(df_test_std[x_col], df_test_std[y_col], color='green', alpha=0.5, label='Knight')
    # ax2.xlabel(x_col)
    # ax2.ylabel(y_col)
    # ax2.legend()

    plt.tight_layout()
    plt.savefig("standardized.png")

except Exception as e:
    print(f"Error: {e}")