"""
train_classifier.py

Trains a lightweight, explainable Random Forest classifier on the
electrical feature dataset. Evaluates with accuracy, precision,
recall, F1, and confusion matrix. Saves the trained model and a
plotted confusion matrix.

Framed as: anomaly/cause classification for decision support, NOT
proof of electricity theft.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import json
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report, ConfusionMatrixDisplay
)

from signal_processing.src.feature_extraction import FEATURE_NAMES

RANDOM_SEED = 42
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "classifier.joblib")
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "evaluation_results.json")
CM_PLOT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "confusion_matrix.png")


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_NAMES].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=RANDOM_SEED,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )
    labels_sorted = sorted(df["label"].unique())
    per_class_report = classification_report(
        y_test, y_pred, labels=labels_sorted, zero_division=0, output_dict=True
    )
    cm = confusion_matrix(y_test, y_pred, labels=labels_sorted)

    results = {
        "test_size": len(y_test),
        "train_size": len(y_train),
        "accuracy": accuracy,
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "per_class_report": per_class_report,
        "confusion_matrix_labels": labels_sorted,
        "confusion_matrix": cm.tolist(),
        "feature_names": FEATURE_NAMES,
        "feature_importances": dict(zip(FEATURE_NAMES, clf.feature_importances_.tolist())),
    }

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels_sorted)
    fig, ax = plt.subplots(figsize=(7, 6))
    disp.plot(ax=ax, xticks_rotation=45, cmap="Blues", colorbar=False)
    plt.tight_layout()
    plt.savefig(CM_PLOT_PATH, dpi=120)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro Precision: {precision:.4f}")
    print(f"Macro Recall: {recall:.4f}")
    print(f"Macro F1: {f1:.4f}")
    print("\nPer-class report:")
    print(classification_report(y_test, y_pred, labels=labels_sorted, zero_division=0))
    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Results saved to {RESULTS_PATH}")
    print(f"Confusion matrix plot saved to {CM_PLOT_PATH}")


if __name__ == "__main__":
    main()
