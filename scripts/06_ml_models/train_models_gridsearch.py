"""
Step 06: Machine learning classification with GridSearchCV

Models:
- Random Forest
- k-Nearest Neighbors
- Gradient Boosting

Input:
- SuperImposed_GM_M2_4.csv

Outputs:
- Prints summary of best params and performance for each model
- Saves misclassified instances for each model as CSV:
  - misclassified_random_forest.csv
  - misclassified_k_nearest_neighbors.csv
  - misclassified_gradient_boosting.csv

Notes:
- Notebook-style implementation
- StandardScaler + PCA(n_components=0.95) applied before model training
"""


import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, LabelBinarizer
from sklearn.decomposition import PCA

from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("__file_name__.csv")
df.columns = df.columns.str.replace(r"\s+", "", regex=True)

# -----------------------------
# Encode target variable (diet)
# -----------------------------
label_encoder = LabelEncoder()
df["y_encoded"] = label_encoder.fit_transform(df["Column1"])

# -----------------------------
# Split into features and target
# -----------------------------
X = df.iloc[:, 8:].apply(pd.to_numeric, errors="coerce").fillna(0)
y = df["y_encoded"]

# Keep metadata for misclassification tables
has_species = "Species" in df.columns
has_tribe = "Tribe" in df.columns
has_filename = "File_Name" in df.columns

# -----------------------------
# Train-test split (stratified)
# -----------------------------
X_train, X_test, y_train, y_test, train_index, test_index = train_test_split(
    X,
    y,
    df.index,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# -----------------------------
# Standardize features
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# PCA (retain 95% variance)
# -----------------------------
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# -----------------------------
# Model evaluation function (GridSearchCV + metrics + misclassified)
# -----------------------------
def evaluate_model_gs(clf, param_grid, Xtr, ytr, Xte, yte, original_df, test_indices, model_name):
    grid_search = GridSearchCV(clf, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
    grid_search.fit(Xtr, ytr)

    best_clf = grid_search.best_estimator_
    best_params = grid_search.best_params_

    cv_scores = cross_val_score(best_clf, Xtr, ytr, cv=5, scoring="accuracy")

    y_train_pred = best_clf.predict(Xtr)
    y_test_pred = best_clf.predict(Xte)

    train_accuracy = accuracy_score(ytr, y_train_pred)
    test_accuracy = accuracy_score(yte, y_test_pred)
    precision = precision_score(yte, y_test_pred, average="weighted", zero_division=0)
    recall = recall_score(yte, y_test_pred, average="weighted", zero_division=0)
    f1 = f1_score(yte, y_test_pred, average="weighted", zero_division=0)

    # ROC-AUC (multiclass) if predict_proba is available
    roc_auc = None
    try:
        lb = LabelBinarizer()
        y_test_binarized = lb.fit_transform(yte)
        y_test_prob = best_clf.predict_proba(Xte)
        roc_auc = roc_auc_score(y_test_binarized, y_test_prob, average="macro", multi_class="ovr")
    except Exception:
        roc_auc = None

    # Classification report
    target_names = label_encoder.inverse_transform(np.unique(yte))
    report = classification_report(yte, y_test_pred, target_names=target_names, zero_division=0)

    # Misclassified instances
    mis_idx = np.where(yte.values != y_test_pred)[0]
    mis_rows = []
    for i in mis_idx:
        row_i = test_indices[i]
        mis_rows.append({
            "Species": original_df.loc[row_i, "Species"] if "Species" in original_df.columns else None,
            "Tribe": original_df.loc[row_i, "Tribe"] if "Tribe" in original_df.columns else None,
            "File_Name": original_df.loc[row_i, "File_Name"] if "File_Name" in original_df.columns else None,
            "True_Label": label_encoder.inverse_transform([yte.iloc[i]])[0],
            "Predicted_Label": label_encoder.inverse_transform([y_test_pred[i]])[0],
        })

    mis_df = pd.DataFrame(mis_rows)
    out_name = model_name.lower().replace(" ", "_").replace("-", "_")
    mis_df.to_csv(f"misclassified_{out_name}.csv", index=False)

    return {
        "best_model": best_clf,
        "best_params": best_params,
        "cv_mean": float(cv_scores.mean()),
        "cv_std": float(cv_scores.std()),
        "train_accuracy": float(train_accuracy),
        "test_accuracy": float(test_accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": None if roc_auc is None else float(roc_auc),
        "report": report,
        "misclassified_csv": f"misclassified_{out_name}.csv",
    }

# -----------------------------
# Define classifiers + grids (same spirit as your notebook)
# -----------------------------
classifiers = {
    "Random Forest": (
        RandomForestClassifier(random_state=42),
        {
            "n_estimators": [100, 200],
            "max_depth": [10, 20],
            "min_samples_split": [2, 10],
            "min_samples_leaf": [1, 2],
            "max_features": ["sqrt", "log2"],
        },
    ),
    "K-Nearest Neighbors": (
        KNeighborsClassifier(),
        {
            "n_neighbors": [3, 5, 7],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan"],
        },
    ),
    "Gradient Boosting": (
        GradientBoostingClassifier(random_state=42),
        {
            "n_estimators": [100, 200],
            "learning_rate": [0.01, 0.1],
            "max_depth": [3, 5],
            "min_samples_split": [2, 10],
            "min_samples_leaf": [1, 2],
        },
    ),
}

# -----------------------------
# Run evaluations
# -----------------------------
results = {}

for name, (clf, grid) in classifiers.items():
    print(f"\nEvaluating {name} with GridSearchCV...")
    res = evaluate_model_gs(
        clf,
        grid,
        X_train_pca,
        y_train,
        X_test_pca,
        y_test,
        df,
        test_index,
        name
    )

    results[name] = res

    print("Best Params:", res["best_params"])
    print(f"CV Mean Accuracy: {res['cv_mean']:.3f} ± {res['cv_std']:.3f}")
    print(f"Training Accuracy: {res['train_accuracy']:.3f}")
    print(f"Test Accuracy: {res['test_accuracy']:.3f}")
    print(f"Precision: {res['precision']:.3f}")
    print(f"Recall: {res['recall']:.3f}")
    print(f"F1 Score: {res['f1']:.3f}")
    print(f"ROC AUC: {res['roc_auc']}")
    print("Saved misclassified table:", res["misclassified_csv"])
    print("Classification Report:\n", res["report"])
    print("=" * 80)

# -----------------------------
# Print summary
# -----------------------------
print("\nSummary:")
for name, res in results.items():
    print(
        f"{name} | "
        f"CV: {res['cv_mean']:.2f} ± {res['cv_std']:.2f} | "
        f"Train: {res['train_accuracy']:.2f} | "
        f"Test: {res['test_accuracy']:.2f} | "
        f"F1: {res['f1']:.2f} | "
        f"ROC AUC: {res['roc_auc']}"
    )
