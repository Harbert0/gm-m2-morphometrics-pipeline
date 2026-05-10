"""
Step 05b: Learning curves for machine learning models

Models:
- Random Forest
- k-Nearest Neighbors
- Gradient Boosting

Input:
- CSV file containing specimen metadata and Procrustes-aligned landmark coordinates

Output:
- Displays learning curve plots (not saved automatically)

Notes:
- Notebook-style implementation 
- StandardScaler + PCA(n_components=0.95) applied before learning curves
"""

import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve, StratifiedKFold
 
def plot_learning_curve(estimator, X, y, title, cv=None, n_jobs=None, train_sizes=np.linspace(0.1, 1.0, 10)):
    plt.figure()
    plt.title(title)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
 
    train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
 
    plt.grid()
 
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
 
    plt.legend(loc="best")
    plt.show()
 
# Plot learning curves for each classifier
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
 
for name, (clf, param_grid) in classifiers.items():
    plot_learning_curve(clf, X_train_pca, y_train, f"{name} Learning Curve for Principal Components", cv=cv, n_jobs=-1)
 
 

