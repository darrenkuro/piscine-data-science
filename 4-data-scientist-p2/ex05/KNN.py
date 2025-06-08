import sys
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, accuracy_score
import matplotlib.pyplot as plt

FILE_VALIDATION = "../Validation_knight.csv"

try:
    if len(sys.argv) != 3:
        print("Usage: python KNN.py Training_knight.csv Test_knight.csv")
        exit(1)
    
    train_df = pd.read_csv(sys.argv[1])  # Training
    test_df = pd.read_csv(sys.argv[2])   # Test
    val_df = pd.read_csv(FILE_VALIDATION)  # Validationg for tweaking k

    X_train = train_df.drop(columns=["knight"])
    y_train = train_df["knight"]
    X_val = val_df.drop(columns=["knight"])
    y_val = val_df["knight"]
    X_test = test_df.drop(columns=["knight"], errors='ignore')

    encoder = LabelEncoder()
    y_train_enc = encoder.fit_transform(y_train)
    y_val_enc = encoder.transform(y_val)

    # Try different k values and track precision
    k_values = range(1, 21)
    accuracy_scores = []
    f1_scores = []

    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train_enc)
        y_pred_val = knn.predict(X_val)
        
        accuracy = accuracy_score(y_val_enc, y_pred_val)
        f1 = f1_score(y_val_enc, y_pred_val, average='weighted')
        
        accuracy_scores.append(accuracy)
        f1_scores.append(f1)

    # Plot
    plt.plot(k_values, accuracy_scores)
    plt.xlabel('k values')
    plt.ylabel('accuracy')
    plt.tight_layout()
    plt.savefig("knn_accuracy_scores.png")
    plt.close()

    # Choose best k
    best_k = k_values[f1_scores.index(max(f1_scores))]
    print(f"Best k: {best_k} with F1 = {max(f1_scores):.4f}")

    # Train on full training data using best_k
    final_knn = KNeighborsClassifier(n_neighbors=best_k)
    final_knn.fit(X_train, y_train_enc)

    # Predict on test set
    y_pred_test = final_knn.predict(X_test)
    y_pred_labels = encoder.inverse_transform(y_pred_test)

    # Write predictions
    with open("KNN.txt", "w") as f:
        f.write("\n".join(y_pred_labels))

except Exception as e:
    print(f"Error: {e}")
    exit(1)