import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_FILE = "Train_knight.csv"
TRAIN_OUTPUT = "Training_knight.csv"
VALID_OUTPUT = "Validation_knight.csv"

df = pd.read_csv(INPUT_FILE)

train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

train_df.to_csv(TRAIN_OUTPUT, index=False)
val_df.to_csv(VALID_OUTPUT, index=False)