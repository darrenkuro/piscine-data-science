import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_FILE = "../Train_knight.csv"
TRAIN_OUTPUT = "Training_knight.csv"
VALID_OUTPUT = "Validation_knight.csv"

try:
    df = pd.read_csv(INPUT_FILE)
    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42, shuffle=True)

    train_df.to_csv(TRAIN_OUTPUT, index=False)
    val_df.to_csv(VALID_OUTPUT, index=False)

    print(f"Total rows: {len(df)}")
    print(f"Training set: {len(train_df)} rows")
    print(f"Validation set: {len(val_df)} rows")

except Exception as e:
    print(f"Error: {e}")