import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_file(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
    # [<expression> for <item> in <iterable> if <condition>]
    # loop over every line, only include non-empty lines, remove extra whitespaces

try:
    if len(sys.argv) != 3:
        print("Usage: python Confusion_Matrix.py predictions.txt truth.txt")
        exit(1)
    
    y_pred = load_file(sys.argv[1])
    y_true = load_file(sys.argv[2])

    if len(y_true) != len(y_pred):
        raise ValueError("Length mismatch between truth and prediction files.")

    classes = sorted(set(y_true + y_pred))
    label_to_index = {label: idx for idx, label in enumerate(classes)} # Map string to number
    n_classes = len(classes)

    # Manually create confusion matrix
    cm = np.zeros((n_classes, n_classes), dtype=int)
    for true_label, pred_label in zip(y_true, y_pred):
        i = label_to_index[true_label]
        j = label_to_index[pred_label]
        cm[i][j] += 1

    # Compute metrics manually
    print(f"{'':<8}{'precision':>10}{'recall':>10}{'f1-score':>10}{'total':>8}\n")
    total_correct = 0
    for i, label in enumerate(classes):
        TP = cm[i][i]
        FP = cm[:, i].sum() - TP
        FN = cm[i, :].sum() - TP
        support = cm[i, :].sum()
        total_correct += TP

        precision = TP / (TP + FP) if (TP + FP) else 0.0
        recall = TP / (TP + FN) if (TP + FN) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        print(f"{label:<8}{precision:10.2f}{recall:10.2f}{f1:10.2f}{support:8d}")

    accuracy = total_correct / len(y_true)
    print(f"\n{'accuracy':<8}{'':>20}{accuracy:10.2f}{len(y_true):8d}\n")
    print(np.array2string(cm, separator=' '))

    # Plot the graph
    plt.figure(figsize=(8, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='viridis', xticklabels=[0, 1], yticklabels=[0, 1])
    # plt.xlabel("Prediction")
    # plt.ylabel("Truth")

    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.close()

except Exception as e:
    print(f"Error: {e}")
    exit(1)