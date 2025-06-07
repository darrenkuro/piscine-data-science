import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

TRAIN_PATH = "Train_knight.csv"

try:
    df_train = pd.read_csv(TRAIN_PATH)

    # Separate features and target
    features = df_train.drop(columns=["knight"])
    target = df_train["knight"]

    scaler = MinMaxScaler()
    normalized_values = scaler.fit_transform(features)

    # Create DataFrame from normalized values
    df_norm = pd.DataFrame(normalized_values, columns=features.columns)
    df_norm["knight"] = target

    print(df_norm)

    # Plot: one of the graphs from before (e.g., Empowered vs Stims)
    x_col = "Push"
    y_col = "Grasping"

    df_jedi = df_norm[df_norm["knight"] == "Jedi"]
    df_sith = df_norm[df_norm["knight"] == "Sith"]

    plt.figure(figsize=(6, 5))
    plt.scatter(df_jedi[x_col], df_jedi[y_col], color='blue', alpha=0.5, label="Jedi")
    plt.scatter(df_sith[x_col], df_sith[y_col], color='red', alpha=0.5, label="Sith")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error: {e}")