import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
import matplotlib.pyplot as plt

FILE_VALIDATION = "../Validation_knight.csv"

try:
    if len(sys.argv) != 3:
        print("Usage: python Tree.py Training_knight.csv Test_knight.csv")
        exit(1)
    
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])

    X_train = df_train.drop(columns=["knight"])
    y_train = df_train["knight"]

    X_test = df_test.drop(columns=["knight"], errors='ignore')

    encoder = LabelEncoder()
    y_train_encoded = encoder.fit_transform(y_train)

    # Train Decision Tree
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train_encoded)

    y_pred_encoded_dt = dt.predict(X_test)
    y_pred_dt = encoder.inverse_transform(y_pred_encoded_dt)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train_encoded)

    y_pred_encoded_rf = rf.predict(X_test)
    y_pred_rf = encoder.inverse_transform(y_pred_encoded_rf)

    # Write predictions
    with open("Tree.txt", "w") as f:
        f.write("\n".join(y_pred_dt)) # Use decision tree 

    # Check f1 score of decision tree with validation set
    df_val = pd.read_csv("../Validation_knight.csv")
    X_val = df_val.drop(columns=["knight"])
    y_val = encoder.transform(df_val["knight"])

    y_val_pred = dt.predict(X_val)
    print("Decision Tree Evaluation on Validation Set:")
    print(classification_report(y_val, y_val_pred, target_names=encoder.classes_))

    f1 = f1_score(y_val, y_val_pred, average="weighted")
    print(f"Weighted F1 Score: {f1:.4f}")

    # Plot random forest
    plt.figure(figsize=(20, 10))
    plot_tree(rf.estimators_[0], feature_names=X_train.columns,
            class_names=encoder.classes_, filled=True)
    plt.savefig("random_forest.png")

    # Plot decision tree
    plt.figure(figsize=(20, 10))
    plot_tree(dt, feature_names=X_train.columns, class_names=encoder.classes_, filled=True)
    plt.savefig("decision_tree.png")

except Exception as e:
    print(f"Error: {e}")
    exit(1)