import sys
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(cm, labels, title="Confusion Matrix", filename="confusion_matrix.png"):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='viridis', xticklabels=labels, yticklabels=labels)
    plt.xlabel("Prediction")
    plt.ylabel("Truth")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def load_file(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def main(pred_file, truth_file):
    y_pred = load_file(pred_file)
    y_true = load_file(truth_file)

    labels = sorted(list(set(y_true + y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
    acc = accuracy_score(y_true, y_pred)

    # Print per-class metrics
    print(f"{'Class':<8}{'Precision':>10}{'Recall':>10}{'F1-score':>10}{'Total':>8}\n")
    for label in labels:
        precision = report[label]["precision"]
        recall = report[label]["recall"]
        f1 = report[label]["f1-score"]
        support = int(report[label]["support"])
        print(f"{label:<8}{precision:10.2f}{recall:10.2f}{f1:10.2f}{support:8d}")

    print(f"\n{'Accuracy':<8}{acc:10.2f}{'':>20}{len(y_true):8d}\n")
    print(np.array2string(cm, separator=' '))
    plot_confusion_matrix(cm, labels)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Confusion_Matrix.py predictions.txt truth.txt")
    else:
        main(sys.argv[1], sys.argv[2])