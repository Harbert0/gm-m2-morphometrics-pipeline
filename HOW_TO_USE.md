# How to Use This Repository

This repository accompanies the manuscript:

**Decoding Diets: Applying Machine Learning Models to Geometric Morphometric Analysis of Bovid Dental Mesowear Signatures**

The purpose of this repository is to provide a transparent and reproducible workflow for moving from digitized mandibular second molar landmark coordinates to geometric morphometric analysis and supervised dietary classification.

The workflow includes:

1. landmark digitization in ImageJ/Fiji,
2. coordinate preparation,
3. Generalized Procrustes Analysis with sliding semilandmarks,
4. metadata merging,
5. Principal Component Analysis,
6. Linear Discriminant Analysis,
7. machine learning classification,
8. model evaluation and visualization.

---

## 1. Software Used

The analyses were conducted using ImageJ/Fiji and Python.

| Analysis step                   | Software/packages           | Purpose                                                                             |
|---------------------------------|-----------------------------|-------------------------------------------------------------------------------------|
| Landmark digitization           | ImageJ/Fiji                 | Manual placement and export of two-dimensional landmark coordinates                 |
| Coordinate preparation          | Python, pandas, numpy       | Reshape and organize coordinate data                                                |
| Generalized Procrustes Analysis | Python, custom scripts      | Align landmark configurations by translation, rotation, and scaling                 |
| Sliding semilandmarks           | Python, custom scripts      | Slide semilandmarks along the outline to improve anatomical correspondence          |
| Metadata merging                | Python, pandas              | Combine Procrustes-aligned coordinates with specimen metadata                       |
| PCA                             | Python, scikit-learn        | Reduce dimensionality of Procrustes-aligned shape coordinates                       |
| LDA                             | Python, scikit-learn        | Baseline supervised dietary classification                                          |
| Random Forest                   | Python, scikit-learn        | Nonlinear supervised classification                                                 |
| k-nearest neighbors             | Python, scikit-learn        | Distance-based supervised classification                                            |
| Gradient Boosting               | Python, scikit-learn        | Nonlinear ensemble classification                                                   |
| Model evaluation                | Python, scikit-learn        | Accuracy, precision, recall, F1 score, ROC AUC, confusion matrices, learning curves |
| Plotting                        | Python, matplotlib, seaborn | Visualization of analysis outputs                                                   |

** Note:  R/geomorph was not directly executed in this repository. The GPA and sliding semilandmark workflow is conceptually consistent with established geometric morphometric procedures used in geomorph, but the analyses provided here were conducted in Python.
          All scripts included in this repository are implemented in Python unless otherwise noted.


---

## 2. Input Data

The dataset used in the manuscript is provided as:

```
Example_Data.csv
```

This file corresponds to the supplementary coordinate table associated with the manuscript.

The file includes specimen information and two-dimensional landmark coordinates.

Each specimen contains 23 coordinate points:

| Coordinate            | Landmark type             | Description                                                                          |
|-----------------------|---------------------------|--------------------------------------------------------------------------------------|
| X1, Y1                | Fixed anatomical landmark | Lowest point between the two cusps of the lingual surface                            |
| X2/Y2 through X22/Y22 | Sliding semilandmarks     | Semilandmarks along the occlusal outline of the entoconid cusp                       |
| X23, Y23              | Fixed anatomical landmark | End of the hypoconulid and edge of M2 between the second and third mandibular molars |

Landmarks 1 and 23 are treated as fixed anatomical landmarks. Landmarks 2 through 22 are treated as semilandmarks.

---

## 3. Environment Setup

To reproduce the Python analysis environment, use either the conda environment file or the pip requirements file.

### Option 1: Conda

```bash
conda env create -f environment.yml
conda activate gm-m2-morphometrics
```

### Option 2: pip

```bash
pip install -r requirements.txt
```

The conda environment is recommended because it provides a more consistent software environment across operating systems.

---

## 4. Recommended Run Order

The scripts are organized numerically to reflect the order of the analysis pipeline.

Run the folders in this order:

```
scripts/00_imagej/
scripts/01_prepare_coordinates/
scripts/02_gpa/
scripts/03_merge_metadata/
scripts/04_pca/
scripts/05_lda/
scripts/06_ml_models/
```

Each folder corresponds to a major step in the workflow.

---

## 5. Step-by-Step Workflow

### Step 0: Landmark digitization in ImageJ/Fiji

Folder:

```
scripts/00_imagej/
```

Purpose:

This folder contains the ImageJ/Fiji macro or instructions used to export two-dimensional landmark coordinates from mandibular second molar images.

The digitization workflow begins with manual placement of landmarks along the occlusal outline of the entoconid cusp.

Output from this step:

```
raw landmark coordinate file
```

The exported coordinates are then used as input for the Python preprocessing scripts.

---

### Step 1: Prepare coordinate data

Folder:

```
scripts/01_prepare_coordinates/
```

Purpose:

This step reshapes and organizes the landmark coordinate data exported from ImageJ/Fiji.

This step ensures that each specimen has the correct coordinate structure:

```
X1, Y1, X2, Y2, ..., X23, Y23
```

Output from this step:

```
cleaned coordinate table
```

This cleaned coordinate file is used for Generalized Procrustes Analysis.

---

### Step 2: Generalized Procrustes Analysis and sliding semilandmarks

Folder:

```
scripts/02_gpa/
```

Purpose:

This step performs Generalized Procrustes Analysis on the two-dimensional landmark configurations.

The GPA procedure removes non-shape variation associated with position, orientation, and scale.

Landmark treatment:

- Landmarks 1 and 23 are fixed anatomical landmarks.
- Landmarks 2 through 22 are treated as sliding semilandmarks.

The semilandmarks are slid along the outline to improve correspondence among specimens.

Output from this step:

```
Procrustes-aligned coordinates
```

These coordinates represent shape variation after removing non-shape variation.

---

### Step 3: Merge Procrustes coordinates with metadata

Folder:

```
scripts/03_merge_metadata/
```

Purpose:

This step combines the Procrustes-aligned coordinates with specimen metadata, including taxonomic and dietary information.

Output from this step:

```
analysis-ready dataset
```

This file is used for PCA, LDA, and machine learning analyses.

---

### Step 4: Principal Component Analysis

Folder:

```
scripts/04_pca/
```

Purpose:

This step performs Principal Component Analysis on the Procrustes-aligned coordinates.

PCA is used to summarize major axes of shape variation and reduce dimensionality prior to classification.

Output from this step:

```
PCA scores
PCA variance summary
PCA plots
```

The PCA scores are used as predictors in the supervised classification analyses.

---

### Step 5: Linear Discriminant Analysis

Folder:

```
scripts/05_lda/
```

Purpose:

This step performs Linear Discriminant Analysis using PCA scores as input variables and dietary category as the response variable.

LDA is included as a baseline supervised classification method.

Output from this step may include:

```
LDA classification results
cross-validation accuracy
held-out test-set performance
confusion matrix
misclassification summary
```

---

### Step 6: Machine learning classification

Folder:

```
scripts/06_ml_models/
```

Purpose:

This step trains and evaluates nonlinear machine learning models for dietary classification.

Models included:

- Random Forest
- k-nearest neighbors
- Gradient Boosting

The machine learning models are trained using PCA scores as input variables and dietary category as the response variable.

The dataset is split into training and testing subsets using stratified sampling to preserve dietary class representation.

Hyperparameter tuning is performed using cross-validation within the training data only.

Final model performance is evaluated once on the held-out test set.

Output from this step may include:

```
model performance summaries
accuracy
precision
recall
F1 score
ROC AUC
confusion matrices
learning curves
misclassification summaries
```

---

## 6. Notes on Data Leakage Prevention

To avoid data leakage, model fitting and preprocessing steps used for classification are performed within the training data and then applied to validation or test data.

The held-out test set is not used during model tuning.

Final model performance is assessed only after model selection is complete.

---

## 7. Expected Outputs

By running the complete workflow, users should be able to generate:

- cleaned landmark coordinate files,
- Procrustes-aligned coordinates,
- PCA scores,
- PCA variance summaries,
- LDA results,
- Random Forest results,
- k-nearest neighbors results,
- Gradient Boosting results,
- classification metrics,
- confusion matrices,
- learning curves,
- misclassification summaries.

---

## 8. Relationship to the Manuscript

This repository provides the computational workflow associated with the geometric morphometric and classification analyses described in the manuscript.

The repository is intended to clarify:

1. which programs were used,
2. where each analysis was conducted,
3. how the coordinate data were processed,
4. how GPA and sliding semilandmarks were implemented,
5. how PCA, LDA, and machine learning models were run,
6. how model performance was evaluated.

---



All scripts included in this repository are implemented in Python unless otherwise noted.

---


