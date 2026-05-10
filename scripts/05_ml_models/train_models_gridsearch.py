"""
Step 05: Machine learning classification (GridSearchCV) on Procrustes-aligned shape data

Input:
- CSV file containing specimen metadata and Procrustes-aligned landmark coordinates.

Output:
- Printed model evaluation results for each classifier:
  - best hyperparameters (GridSearchCV)
  - cross-validated accuracy (mean ± SD) on the training set
  - train/test accuracy, weighted precision/recall/F1, multiclass ROC-AUC
  - test-set classification report
- Printed tables of test-set misclassified specimens (Species, Tribe, File_Name, true vs predicted label)

Notes:
- Features are standardized (fit on training set) and reduced using PCA (95% variance)
  prior to model fitting.
- Models evaluated: Random Forest, k-Nearest Neighbors, Gradient Boosting.
- This script does not save outputs to disk unless explicitly added (e.g., to_csv()).
- Notebook-style implementation
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from scikeras.wrappers import KerasClassifier
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.utils import to_categorical
 
# Load the dataset
data = pd.read_csv('__file_name__.csv')
data.columns = data.columns.str.replace(r'\s+', '', regex=True)
 
# Encode the target variable
label_encoder = LabelEncoder()
data['y_encoded'] = label_encoder.fit_transform(data['Column1'])
 
# Split into features and target
procrustes_coordinates = data.iloc[:, 8:].apply(pd.to_numeric, errors='coerce').fillna(0)
target = data['y_encoded']
 
# Standardize the features
scaler = StandardScaler()
 
# Split the data into training and testing sets
X_train, X_test, y_train, y_test, train_index, test_index = train_test_split(procrustes_coordinates, target, data.index, test_size=0.3, random_state=42, stratify=target)
 
# Fit the scaler on the training data and transform the training and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
 
# Apply PCA transformation on the training set only
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)
 
# Function to evaluate traditional machine learning models using GridSearchCV
def evaluate_model_gs(clf, param_grid, X, y, X_test, y_test, original_data, test_indices):
    grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X, y)
    best_clf = grid_search.best_estimator_
    best_params = grid_search.best_params_
    cv_scores = cross_val_score(best_clf, X, y, cv=5, scoring='accuracy')
    
    y_train_pred = best_clf.predict(X)
    y_test_pred = best_clf.predict(X_test)
    
    train_accuracy = accuracy_score(y, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average='weighted')
    recall = recall_score(y_test, y_test_pred, average='weighted')
    f1 = f1_score(y_test, y_test_pred, average='weighted')
    
    lb = LabelBinarizer()
    y_test_binarized = lb.fit_transform(y_test)
    y_test_prob = best_clf.predict_proba(X_test)
    roc_auc = roc_auc_score(y_test_binarized, y_test_prob, average='macro', multi_class='ovr')
    
    test_classification_report = classification_report(y_test, y_test_pred, target_names=label_encoder.inverse_transform(np.unique(y_test)))
    
    # Collect misclassified instances
    misclassified_indices = np.where(y_test != y_test_pred)[0]
    misclassified_instances = []
    for idx in misclassified_indices:
        misclassified_instances.append({
            'Species': original_data.iloc[test_indices[idx]]['Species'],
            'Tribe': original_data.iloc[test_indices[idx]]['Tribe'],
            'True_Label': label_encoder.inverse_transform([y_test.iloc[idx]])[0],
            'Predicted_Label': label_encoder.inverse_transform([y_test_pred[idx]])[0],
            'File_Name':original_data.iloc[test_indices[idx]]["File_Name"]
        })
    
    return best_clf, best_params, cv_scores.mean(), cv_scores.std(), train_accuracy, test_accuracy, precision, recall, f1, roc_auc, test_classification_report, misclassified_instances
 
     
# Define the classifiers and their parameter grids
classifiers = {
    "Random Forest": (RandomForestClassifier(random_state=42), {
        'n_estimators': [100, 200],
        'max_depth': [10, 20],
        'min_samples_split': [2, 10],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', 'log2']
    }),
 
    "K-Nearest Neighbors": (KNeighborsClassifier(), {
        'n_neighbors': [3, 5, 7],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }),
    "Gradient Boosting": (GradientBoostingClassifier(random_state=42), {
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1],
        'max_depth': [3, 5],
        'min_samples_split': [2, 10],
        'min_samples_leaf': [1, 2]
    })
   
}
 
# Evaluate each classifier using GridSearchCV
results = {}
misclassified_instances = {}
for name, (clf, param_grid) in classifiers.items():
    print(f"Evaluating {name} with GridSearchCV...")
    best_clf, best_params, mean_cv_score, std_cv_score, train_accuracy, test_accuracy, precision, recall, f1, roc_auc, test_classification_report, misclassified = evaluate_model_gs(clf, param_grid, X_train_pca, y_train, X_test_pca, y_test, data, test_index)
    
    results[name] = {
        "best_params": best_params,
        "cv_mean_score": mean_cv_score,
        "cv_std_score": std_cv_score,
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
        "test_classification_report": test_classification_report
    }
    misclassified_instances[name] = misclassified
    print(f"Best Params: {best_params}")
    print(f"CV Mean Accuracy: {mean_cv_score} ± {std_cv_score}")
    print(f"Training Accuracy: {train_accuracy}")
    print(f"Test Accuracy: {test_accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print(f"ROC AUC: {roc_auc}")
    print(f"Test Classification Report:\n{test_classification_report}")
    print("="*80)
 
 
# Print a summary of results
for name, result in results.items():
    print(f"{name} - Best Params: {result['best_params']} | CV Mean Accuracy: {result['cv_mean_score']:.2f} ± {result['cv_std_score']:.2f} | Training Accuracy: {result['train_accuracy']:.2f} | Test Accuracy: {result['test_accuracy']:.2f} | Precision: {result['precision']:.2f} | Recall: {result['recall']:.2f} | F1 Score: {result['f1_score']:.2f} | ROC AUC: {result['roc_auc']:.2f}")
 
# Create DataFrame for each classifier's misclassified instances
for name, instances in misclassified_instances.items():
    print(f"Misclassified Instances for {name}:")
    misclassified_df = pd.DataFrame(instances)
    print(misclassified_df)
    print("="*80)
 
