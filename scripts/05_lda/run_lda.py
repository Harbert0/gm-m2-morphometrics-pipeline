"""
Step 05: Linear Discriminant Analysis (LDA) on Procrustes-aligned coordinates

Input:
-(metadata + Procrustes-aligned landmark coordinates csv

Output:
- Printed performance metrics (training accuracy, test accuracy, precision,
  recall, F1 score, ROC-AUC)
- Displayed figures (learning curve, confusion matrix heatmap, and decision
  regions when applicable)
- In-memory table of misclassified specimens (misclassified_table)


Notes:
- Features are coordinate columns (X*, Y*).
- Data are standardized, then PCA is applied (retain 95% variance) prior to LDA.
- Target defaults to 'Column1' (diet). Update TARGET_COL if needed.
"""

import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, learning_curve
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, precision_recall_fscore_support, roc_auc_score
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
 
# Load the dataset
file_path = '__file_name__.csv'
data = pd.read_csv(file_path)
data.columns = data.columns.str.replace(r'\s+', '', regex=True)
 
# Encode the target variable
le = LabelEncoder()
data['y_encoded'] = le.fit_transform(data['Column1'])
 
# Extract features (Procrustes coordinates) and target (diet)
X = data.iloc[:, 8:].apply(pd.to_numeric, errors='coerce').fillna(0)
y = data['y_encoded'].values
species = data['Species'].values
tribe = data['Tribe'].values
 
# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
 
# Split the data for initial train and test evaluation
X_train, X_test, y_train, y_test, species_train, species_test, tribe_train, tribe_test = train_test_split(
    X_scaled, y, species, tribe, test_size=0.2, stratify=y, random_state=42)
 
# Perform PCA on the training set and apply it to the test set
pca = PCA(n_components=0.95)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)
 
# Initialize and train LDA on PCA-transformed data
lda = LinearDiscriminantAnalysis()
lda.fit(X_train_pca, y_train)
 
# Predict on test data
y_test_pred = lda.predict(X_test_pca)
 
# Calculate performance metrics
train_accuracy = lda.score(X_train_pca, y_train)
test_accuracy = accuracy_score(y_test, y_test_pred)
precision = precision_score(y_test, y_test_pred, average='weighted')
recall = recall_score(y_test, y_test_pred, average='weighted')
f1 = f1_score(y_test, y_test_pred, average='weighted')
conf_matrix = confusion_matrix(y_test, y_test_pred)
 
# Calculate class-specific precision
class_precisions = precision_recall_fscore_support(y_test, y_test_pred, average=None, labels=np.unique(y_test))[0]
 
# Calculate ROC-AUC for multiclass
y_test_binarized = label_binarize(y_test, classes=np.unique(y))
y_test_prob = lda.predict_proba(X_test_pca)
roc_auc = roc_auc_score(y_test_binarized, y_test_prob, average='macro', multi_class='ovr')
 
# Cross-validation
skf = StratifiedKFold(n_splits=10)
cv_scores = cross_val_score(lda, X_train_pca, y_train, cv=skf)
cv_average_score = np.mean(cv_scores)
cv_std = np.std(cv_scores)
 
# Learning curve
train_sizes, train_scores, test_scores = learning_curve(lda, X_train_pca, y_train, cv=skf, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10))
 
# Plot learning curve
plt.figure()
plt.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color="r", label="Training score")
plt.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color="g", label="Cross-validation score")
plt.fill_between(train_sizes, np.mean(train_scores, axis=1) - np.std(train_scores, axis=1), np.mean(train_scores, axis=1) + np.std(train_scores, axis=1), color="r", alpha=0.1)
plt.fill_between(train_sizes, np.mean(test_scores, axis=1) - np.std(test_scores, axis=1), np.mean(test_scores, axis=1) + np.std(test_scores, axis=1), color="g", alpha=0.1)
plt.title('Learning Curve (LDA)')
plt.xlabel('Training examples')
plt.ylabel('Score')
plt.legend(loc='best')
plt.grid()
plt.show()
 
# Misclassified instances
misclassified = (y_test != y_test_pred)
misclassified_table = pd.DataFrame({
    'True Label': le.inverse_transform(y_test[misclassified]),
    'Predicted Label': le.inverse_transform(y_test_pred[misclassified]),
    'Species': species_test[misclassified],
    'Tribe': tribe_test[misclassified]
})
 
# Check if LDA produced more than one component
if X_train_pca.shape[1] > 1:
    # Plot partition plot (decision regions)
    x_min, x_max = X_train_pca[:, 0].min() - 1, X_train_pca[:, 0].max() + 1
    y_min, y_max = X_train_pca[:, 1].min() - 1, X_train_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                         np.arange(y_min, y_max, 0.01))
 
    Z = lda.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
 
    plt.contourf(xx, yy, Z, alpha=0.4)
    sns.scatterplot(x=X_train_pca[:, 0], y=X_train_pca[:, 1], hue=y_train, palette="deep", alpha=0.6, edgecolor='k')
    plt.title('LDA Decision Regions')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()
else:
    print("LDA did not produce more than one component. Cannot plot decision regions.")
 
# Plot confusion matrix heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=le.classes_, yticklabels=le.classes_)
plt.title('Confusion Matrix Heatmap')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
 
# Display results
results = {    
    'Cross-Validation Average Score': cv_average_score,
    'Cross-Validation Std Dev': cv_std,
    'Training Accuracy': train_accuracy,
    'Test Accuracy': test_accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'ROC AUC': roc_auc,
    'Confusion Matrix': conf_matrix,    
}
results
 
# Display misclassified instances
print("Misclassified Instances:")
misclassified_table
