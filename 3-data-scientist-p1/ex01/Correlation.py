import pandas as pd

# Config
FILE_TRAIN = "Train_knight.csv"

# Main
try:
    df = pd.read_csv(FILE_TRAIN)
    df["knight"] = df["knight"].map({'Sith': 0, 'Jedi': 1})
    df_numeric = df.select_dtypes(include='number')

    corr_matrix = df_numeric.corr() # Default: Pearson
    corr_sorted = corr_matrix["knight"].abs().sort_values(ascending=False)
    print(corr_sorted)

except Exception as e:
    print(f"Error: {e}")