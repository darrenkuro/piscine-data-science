import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load train and test data
df_train = pd.read_csv(sys.argv[1])
df_test = pd.read_csv(sys.argv[2])

# Separate features and labels
X_train = df_train.drop(columns=["knight"])
y_train = df_train["knight"]

X_test = df_test.drop(columns=["knight"], errors='ignore')

# Encode labels
encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train)

# Train Decision Tree
dtc = DecisionTreeClassifier(random_state=42)
dtc.fit(X_train, y_train_encoded)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train_encoded)

# Predict
y_pred_encoded_rf = rf.predict(X_test)
y_pred_rf = encoder.inverse_transform(y_pred_encoded_rf)

# Predict on test set
y_pred_encoded_dtc = dtc.predict(X_test)
y_pred_dtc = encoder.inverse_transform(y_pred_encoded_dtc)

# Write predictions to Tree.txt
with open("Tree.txt", "w") as f:
    for label in y_pred_dtc: # Use decision tree 
        f.write(label + "\n")

# Plot one of the trees in the forest
plt.figure(figsize=(20, 10))
plot_tree(rf.estimators_[0], feature_names=X_train.columns,
          class_names=encoder.classes_, filled=True)
plt.savefig("random_forest.png")

# Plot and show the decision tree
plt.figure(figsize=(20, 10))
plot_tree(dtc, feature_names=X_train.columns, class_names=encoder.classes_, filled=True)
plt.savefig("decision_tree.png")