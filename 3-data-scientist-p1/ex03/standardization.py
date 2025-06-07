import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

FILE_TRAIN = "../Train_knight.csv"
FILE_TEST = "../Test_knight.csv"

try:
    df_train = pd.read_csv(FILE_TRAIN)
    df_test = pd.read_csv(FILE_TEST)

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(5, 8))

    features_train = df_train.drop(columns=["knight"])
    target_train = df_train["knight"]

    print(features_train)

    scaler = StandardScaler()
    standardized_train = scaler.fit_transform(features_train)
    standardized_test = scaler.transform(df_test)

    df_std = pd.DataFrame(standardized_train, columns=features_train.columns)
    print(df_std)

    df_std["knight"] = target_train
    df_test_std = pd.DataFrame(standardized_test, columns=df_test.columns)

    df_jedi = df_std[df_std["knight"] == "Jedi"]
    df_sith = df_std[df_std["knight"] == "Sith"]

    x_col = "Empowered"
    y_col = "Stims"

    # Plot 1: train
    ax1 = axes[0]
    ax1.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    ax1.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(y_col)
    ax1.legend()

    # Plot 2: test
    ax2 = axes[1]
    ax2.scatter(df_test_std[x_col], df_test_std[y_col], color='green', alpha=0.5, label="Knight")
    ax2.set_xlabel(x_col)
    ax2.set_ylabel(y_col)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("standardized.png")

except Exception as e:
    print(f"Error: {e}")