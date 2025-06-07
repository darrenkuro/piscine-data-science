from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Train_knight.csv")
X = df.drop(columns=["knight"]) 
X_scaled = StandardScaler().fit_transform(X)

pca = PCA()
pca.fit(X_scaled)

explained_var = pca.explained_variance_ratio_ * 100 # To percentage
cumulative_var = explained_var.cumsum()

print("Variances (Percentage):")
print(explained_var)

print("\nCumulative Variance (Percentage):")
print(cumulative_var)

# How many components to reach 90%?
n_components_90 = (cumulative_var < 90).sum() + 1
print(f"\nComponents needed to reach 90% variance: {n_components_90}")