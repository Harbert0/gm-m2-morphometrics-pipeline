"""
Step 06b: Learning curves for machine learning models

Models:
- Random Forest
- k-Nearest Neighbors
- Gradient Boosting

Input:
- SuperImposed_GM_M2_4.csv

Output:
- Displays learning curve plots (not saved automatically)

Notes:
- Notebook-style implementation 
- StandardScaler + PCA(n_components=0.95) applied before learning curves
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import learning_curve, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("__file_name__.csv")
df.columns = df.columns.str.replace(r"\s+", "", regex=True)

# -----------------------------
# Encode target variable
# -----------------------------
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Column1"].astype(str))

# -----------------------------
# Features (Procrustes coordinates)
# -----------------------------
X = df.iloc[:, 8:].apply(pd.to_numeric, errors="coerce").fillna(0).values

# -----------------------------
# Standardize + PCA (95% variance)
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

print(f"PCA components retained: {X_pca.shape[1]} (95% variance)")

# -----------------------------
# Learning curve plotting function
# -----------------------------
def plot_learning_curve(estimator, X, y, title, cv=None, n_jobs=None, train_sizes=np.linspace(0.1, 1.0, 10)):
    plt.figure()
    plt.title(title)
    plt.xlabel("Training examples")
    plt.ylabel("Score")

    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes
    )

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid(True)

    plt.fill_between(
        train_sizes,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.15,
        label="Training score ± SD"
    )
    plt.fill_between(
        train_sizes,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.15,
        label="CV score ± SD"
    )

    plt.plot(train_sizes, train_scores_mean, marker="o", label="Training score")
    plt.plot(train_sizes, test_scores_mean, marker="o", label="Cross-validation score")

    plt.legend(loc="best")
    plt.show()


# -----------------------------
# Models (use defaults here, like your notebook)
# -----------------------------
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
}

# Cross-validation scheme
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Plot learning curves
for name, model in models.items():
    plot_learning_curve(model, X_pca, y, f"{name} Learning Curve (PCA features)", cv=cv, n_jobs=-1)
