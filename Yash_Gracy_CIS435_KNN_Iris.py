# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W6tVf4UGaUkF0PkcVgq6I9ml0zV34XkC
"""

import pandas as pd
import numpy as np

def knn_classifier(X_train, y_train, X_test, k=1):
    X_train_array = np.array(X_train, dtype=float)
    X_test_array = np.array(X_test, dtype=float)
    y_train_array = np.array(y_train)

    predictions = []

    for test_instance in X_test_array:
        distances = [
            (np.linalg.norm(test_instance - train_instance), y_train_array[idx])
            for idx, train_instance in enumerate(X_train_array)
        ]

        # Sort distances to get the nearest neighbors
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:k]

        # Count votes for classes
        class_votes = {}
        for _, label in k_nearest:
            class_votes[label] = class_votes.get(label, 0) + 1

        # Get the majority vote
        predicted_class = max(class_votes, key=class_votes.get)
        predictions.append(predicted_class)

    return predictions

def calculate_accuracy(y_true, y_pred):
    correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return correct / len(y_true)

def main():
    try:
        # Corrected file paths and separator
        train_data = pd.read_csv("/content/iris_train.txt", header=None, sep=",")
        test_data = pd.read_csv("/content/iris_test.txt", header=None, sep=",")
        print("✅ Datasets loaded successfully!")
    except FileNotFoundError:
        print("❌ Error: One or both of the files were not found. Please check the file path.")
        return
    except pd.errors.EmptyDataError:
        print("❌ Error: One of the files is empty or has invalid content.")
        return

    # Assign column names
    train_data.columns = [f"feature_{i}" for i in range(train_data.shape[1] - 1)] + [
        "class"
    ]
    test_data.columns = [f"feature_{i}" for i in range(test_data.shape[1] - 1)] + [
        "class"
    ]

    # Split into features and labels
    X_train = train_data.iloc[:, :-1].astype(float)
    y_train = train_data.iloc[:, -1]
    X_test = test_data.iloc[:, :-1].astype(float)
    y_test = test_data.iloc[:, -1]

    # Set value of K
    k = 1

    print(f"\n🔍 Running custom KNN Classification with K={k}")
    predictions = knn_classifier(X_train, y_train, X_test, k)

    # Calculate accuracy
    accuracy = calculate_accuracy(y_test, predictions)

    print(f"✅ Correct Predictions: {int(accuracy * len(y_test))}/{len(y_test)}")
    print(f"📊 Accuracy: {accuracy * 100:.2f}%")

    return predictions, accuracy

if __name__ == "__main__":
    main()