import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, classification_report
from sklearn.preprocessing import StandardScaler

FILE_VALIDATION = "../Validation_knight.csv"

try:
    if len(sys.argv) != 3:
        print("Usage: python Voting.py Training_knight.csv Test_knight.csv")
        exit(1)

    train_df = pd.read_csv(sys.argv[1])
    test_df = pd.read_csv(sys.argv[2])
    val_df = pd.read_csv(FILE_VALIDATION)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_df.drop(columns=["knight"]))
    y_train = train_df["knight"]
    X_val = scaler.transform(val_df.drop(columns=["knight"]))
    y_val = val_df["knight"]
    X_test = scaler.transform(test_df.drop(columns=["knight"], errors="ignore"))

    encoder = LabelEncoder()
    all_labels = pd.concat([y_train, y_val], ignore_index=True)
    encoder.fit(all_labels)

    y_train_enc = encoder.transform(y_train)
    y_val_enc = encoder.transform(y_val)

    # Find best k for KNN
    f1_scores = []
    for k in range(1, 21):
        knn_try = KNeighborsClassifier(n_neighbors=k)
        knn_try.fit(X_train, y_train_enc)
        pred_val = knn_try.predict(X_val)
        score = f1_score(y_val_enc, pred_val, average="weighted")
        f1_scores.append(score)

    best_k = list(range(1, 21))[f1_scores.index(max(f1_scores))]
    print(f"Best k for KNN: {best_k} with F1 = {max(f1_scores):.4f}")

    dt = DecisionTreeClassifier(random_state=42)
    knn = KNeighborsClassifier(n_neighbors=best_k)
    lr = LogisticRegression(max_iter=2000)
    voting = VotingClassifier(
        estimators=[("dt", dt), ("knn", knn), ("lr", lr)],
        voting="hard"
    )
    voting.fit(X_train, y_train_enc)

    # Evaluate on validation set
    val_pred = voting.predict(X_val)
    f1 = f1_score(y_val_enc, val_pred, average="weighted")
    print("Voting Classifier Evaluation on Validation Set:")
    print(classification_report(y_val_enc, val_pred, target_names=encoder.classes_))
    print(f"Weighted F1 Score: {f1:.4f}")

    # Predict on test set
    test_pred = voting.predict(X_test)
    test_labels = encoder.inverse_transform(test_pred)

    # Write to file
    with open("Voting.txt", "w") as f:
        f.write("\n".join(test_labels))

except Exception as e:
    print(f"Error: {e}")
    exit(1)