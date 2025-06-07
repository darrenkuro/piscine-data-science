import pandas as pd
import matplotlib.pyplot as plt

FILE_TRAIN = "Train_knight.csv"
FILE_TEST = "Test_knight.csv"

try:
    df_train = pd.read_csv(FILE_TRAIN)
    df_test  = pd.read_csv(FILE_TEST)
    df_jedi = df_train[df_train["knight"] == "Jedi"]
    df_sith = df_train[df_train["knight"] == "Sith"]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

    # Plot #1: clusters separated, clear separation (high corr)
    ax1 = axes[0, 0]

    x_col = "Empowered"
    y_col = "Stims"

    ax1.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    ax1.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")

    ax1.set_xlabel(x_col)
    ax1.set_ylabel(y_col)
    ax1.legend()

    # Plot #2: clusters mixed, clear separation
    ax2 = axes[1, 0]
    ax2.scatter(df_test[x_col], df_test[y_col], color='green', alpha=0.5, label='Knight')
    ax2.set_xlabel(x_col)
    ax2.set_ylabel(y_col)
    ax2.legend()

    # Plot #3: clusters separated, no separation (low corr)
    x_col = "Push"
    y_col = "Grasping"
    ax3 = axes[0, 1]

    ax3.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    ax3.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")

    ax3.set_xlabel(x_col)
    ax3.set_ylabel(y_col)
    ax3.legend()

    # Plot #4: clusters mixed, no separation
    ax4 = axes[1, 1]
    ax4.scatter(df_test[x_col], df_test[y_col], color='green', alpha=0.5, label='Knight')
    ax4.set_xlabel(x_col)
    ax4.set_ylabel(y_col)
    ax4.legend()

    # Save
    plt.tight_layout()
    plt.savefig("plot.png")

    # Check Plot #1, subject reversed?

except Exception as e:
    print(f"Error: {e}")