import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Config
FILE_TEST = "Test_knight.csv"
FILE_TRAIN = "Train_knight.csv"

# Main
try:
    COLS = 5
    ROWS = 6
    plt.figure(figsize=(COLS * 5, ROWS * 4))

    # Histogram 1: test
    test_df = pd.read_csv(FILE_TEST)

    for i, column in enumerate(test_df.columns, start=1):
        plt.subplot(ROWS, COLS, i)
        sns.histplot(data=test_df, x=column, kde=False, bins=40, color="green", edgecolor=None, label="knight")
        plt.xlabel("")
        plt.ylabel("")
        plt.legend(title="")
        plt.title(column)

    plt.tight_layout()
    plt.savefig("histogram1.png")
    plt.clf()

    # Histogram 2: train
    train_df = pd.read_csv(FILE_TRAIN)
    features = train_df.drop(columns=["knight"])

    for i, column in enumerate(features.columns, start=1):
        plt.subplot(ROWS, COLS, i)
        sns.histplot(data=train_df, x=column, hue="knight", kde=False, palette="pastel", bins=20)
        plt.xlabel("")
        plt.ylabel("")
        plt.title(column)

    plt.tight_layout()
    plt.savefig("histogram2.png")
    plt.clf()

except Exception as e:
    print(f"Error: {e}")