"""
Step 04: Principal Component Analysis (PCA) on Procrustes-aligned coordinates

Input:
- SuperImposed_GM_M2_4.csv  (metadata + Procrustes-aligned landmark coordinates)

Output:
- PC_transformed_coordinates_with_metadata.csv
- results/figures/scree_plot.png
- results/figures/pca_pc1_pc2_by_group.png  (if grouping column exists)

Notes:
- This script performs PCA on coordinate columns only (X*, Y*).
- Metadata columns are preserved and concatenated back to PC scores.
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
 
# Step 1: Load the CSV file
df = pd.read_csv('SuperImposed_GM_M2_4.csv')  
# Strip whitespace and other non-visible characters from the column names
df.columns = df.columns.str.replace(r'\s+', '', regex=True)
 
print(df.head)
 
# Step 2: Extract Procrustes coordinates columns
coordinate_columns = [col for col in df.columns if col.startswith('X') or col.startswith('Y')]
procrustes_df = df[coordinate_columns]
 
# Display the first few rows of the Procrustes coordinates dataframe
print("Procrustes coordinates:")
print(procrustes_df.head())
 
# Step 3: Perform PCA on the Procrustes coordinates
pca = PCA()
principal_components = pca.fit_transform(procrustes_df)
 
# Calculate the explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
 
# Calculate the cumulative explained variance
cumulative_explained_variance = np.cumsum(explained_variance_ratio)
 
# Determine the number of components needed to explain 95% of the variance
n_components_95 = np.argmax(cumulative_explained_variance >= 0.95) + 1
 
print(f"Number of components needed to explain 95% of the variance: {n_components_95}")
 
# Create a DataFrame with PCA results
pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(principal_components.shape[1])])
 
# Add back the relevant metadata (e.g., species, diet)
metadata_columns = ['Species', 'Column1', 'Tribe', 'File_Name']
pca_df = pd.concat([df[metadata_columns], pca_df], axis=1)
 
# Display the explained variance ratio
print("Explained Variance Ratio:")
print(pca.explained_variance_ratio_)
print("PCA Dataframe Head:")
print(pca_df.head)
 
# export transformed coordinates as new CSV file 
pca_df.to_csv('PC_transformed_coordinates_with_metadata.csv', index=False)
 
# Step 4: Scree Plot
plt.figure(figsize=(8, 5))
plt.plot(np.arange(1, len(explained_variance_ratio) + 1), explained_variance_ratio, 'o-', linewidth=2, color='blue')
plt.title('Scree Plot')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.xticks(np.arange(1, len(explained_variance_ratio) + 1))
plt.grid(True)
plt.show()
 
# Step 5: Visualize the first two principal components Hue on Diet
# Custom palette
palette = {
    'browser': '#1f77b4',  # Blue
    'mixed feeder': '#2ca02c',  # Green
    'grazer': '#ff7f0e',  # Orange
    'frugivore': '#d62728'  # Red 
}
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Column1', palette=palette)
plt.title('PCA of Procrustes Coordinates by Dietary Category')
plt.xlabel('Principal Component 1 = 59%')
plt.ylabel('Principal Component 2 = 26%')
plt.legend(title='Diet')
plt.show()
 
# Add convex hulls
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import numpy as np
 
# Assume `pca_df` is your DataFrame and 'Column1' contains the dietary categories
 
# Custom palette
palette = {
    'browser': '#1f77b4',  # Blue
    'mixed feeder': '#2ca02c',  # Green
    'grazer': '#ff7f0e',  # Orange
    'frugivore': '#d62728'  # Red 
}
 
plt.figure(figsize=(10, 6))
 
# Scatter plot
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Column1', palette=palette)
 
# Calculate and plot convex hulls
for diet, color in palette.items():
    points = pca_df[pca_df['Column1'] == diet][['PC1', 'PC2']].values
    if len(points) > 2:  # Convex hull requires at least 3 points
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        plt.fill(hull_points[:, 0], hull_points[:, 1], color=color, alpha=0.3)
 
plt.title('PCA of Procrustes Coordinates by Dietary Category')
plt.xlabel('Principal Component 1 = 59%')
plt.ylabel('Principal Component 2 = 26%')
plt.legend(title='Diet')
plt.show()
 
# Generate and Visualize Shape Models
def plot_shape_model(shape, title):
    x_coords = shape[::2]
    y_coords = shape[1::2]
    plt.plot(x_coords, y_coords, marker='o')
    plt.title(title)
    plt.xlabel('X coordinates')
    plt.ylabel('Y coordinates')
    plt.axis('equal')
 
# Calculate the mean shape
mean_shape = procrustes_df.mean(axis=0).values
pc1_vector = pca.components_[0]
pc2_vector = pca.components_[1]
 
# Number of standard deviations to visualize the shape changes
num_sd = 2
 
# Generate shape models for PC1 and PC2
shape_model_pc1_plus = mean_shape + num_sd * np.sqrt(pca.explained_variance_[0]) * pc1_vector
shape_model_pc1_minus = mean_shape - num_sd * np.sqrt(pca.explained_variance_[0]) * pc1_vector
shape_model_pc2_plus = mean_shape + num_sd * np.sqrt(pca.explained_variance_[1]) * pc2_vector
shape_model_pc2_minus = mean_shape - num_sd * np.sqrt(pca.explained_variance_[1]) * pc2_vector
 
# Plot the shape models
plt.figure(figsize=(12, 6))
 
plt.subplot(2, 2, 1)
plot_shape_model(shape_model_pc1_plus, 'PC1 + 2 SD')
 
plt.subplot(2, 2, 2)
plot_shape_model(shape_model_pc1_minus, 'PC1 - 2 SD')
 
plt.subplot(2, 2, 3)
plot_shape_model(shape_model_pc2_plus, 'PC2 + 2 SD')
 
plt.subplot(2, 2, 4)
plot_shape_model(shape_model_pc2_minus, 'PC2 - 2 SD')
 
plt.tight_layout()
plt.show()
 
# PCA plot based on Tribe
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Tribe', palette='Set2')
plt.title('PCA of Procrustes Coordinates by Tribe')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
# Place the legend below the plot
plt.legend(title='Tribe', bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=4)
plt.tight_layout(rect=[0, 0.1, 1, 1])  # Adjust the layout to make room for the legend
plt.show()
 
