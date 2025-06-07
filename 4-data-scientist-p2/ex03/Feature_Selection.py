from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv("../Train_knight.csv")
X = df.drop(columns=["knight"]) 
X_scaled = StandardScaler().fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

vif_data = pd.DataFrame()
vif_data["Feature"] = X_scaled_df.columns
vif_data["VIF"] = [variance_inflation_factor(X_scaled_df.values, i) for i in range(X_scaled_df.shape[1])]
vif_data["Tolerance"] = 1 / vif_data["VIF"]

print(vif_data.to_string(index=False))

vif_under_5 = vif_data[vif_data["VIF"] < 5]
print(vif_under_5.to_string(index=False))