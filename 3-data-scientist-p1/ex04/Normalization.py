import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

TRAIN_PATH = "../Train_knight.csv"
FILE_TEST = "../Test_knight.csv"

try:
    df_train = pd.read_csv(TRAIN_PATH)
    df_test = pd.read_csv(FILE_TEST)

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(5, 8))

    features = df_train.drop(columns=["knight"])
    target = df_train["knight"]

    print(features)
    scaler = MinMaxScaler()
    normalized_values = scaler.fit_transform(features)
    normalized_test = scaler.transform(df_test)

    df_norm = pd.DataFrame(normalized_values, columns=features.columns)
    print(df_norm)

    df_norm["knight"] = target
    df_test_norm = pd.DataFrame(normalized_test, columns=df_test.columns)

    df_jedi = df_norm[df_norm["knight"] == "Jedi"]
    df_sith = df_norm[df_norm["knight"] == "Sith"]

    x_col = "Push"
    y_col = "Deflection"

    # Plot 1: train
    ax1 = axes[0]
    ax1.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    ax1.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(y_col)
    ax1.legend()

    # Plot 2: test
    ax2 = axes[1]
    ax2.scatter(df_test_norm[x_col], df_test_norm[y_col], color='green', alpha=0.5, label="Knight")
    ax2.set_xlabel(x_col)
    ax2.set_ylabel(y_col)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("normalized.png")

except Exception as e:
    print(f"Error: {e}")