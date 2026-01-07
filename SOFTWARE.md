# Software and version information

This repository documents the software environment used to develop and run the
geometric morphometrics and machine learning analyses presented in the associated
thesis and manuscript.

---

## Python environment

- Python version: **3.10**
- Platform: **macOS (Apple Silicon / Intel compatible)**

### Required Python packages
The following Python packages are required to run the analysis scripts:

- numpy
- pandas
- scipy
- scikit-learn
- matplotlib
- seaborn

All machine learning analyses in this repository use classical statistical and
machine learning models (e.g., LDA, Random Forest, k-Nearest Neighbors, Gradient
Boosting). Neural network models were not used in this workflow.

---

## ImageJ / Fiji

- ImageJ distribution: **Fiji (ImageJ)**
- ImageJ version: **1.53 or later**

ImageJ was used exclusively for landmark digitization. Landmarks were defined
as point ROIs and managed using the ROI Manager. Export of landmark coordinates
was performed using a custom ImageJ macro included in this repository.

Assumptions:
- Landmarks are digitized in a consistent order
- All landmarks are present in the ROI Manager prior to export

---

## R / geomorph (methodological reference)

Although R and geomorph were not executed directly in this repository, the
analytical approach for Generalized Procrustes Analysis (GPA) and sliding
semilandmarks follows established geometric morphometric procedures as
implemented in the geomorph R package:

- Baken, E. K., Collyer, M. L., Kaliontzopoulou, A., & Adams, D. C. (2021).
  *geomorph v4.0 and gmShiny: Enhanced analytics and a new graphical interface
  for a comprehensive morphometric experience*. Methods in Ecology and Evolution.
- Adams, D. C., Collyer, M. L., Kaliontzopoulou, A., & Baken, E. K. (2025).
  *geomorph: Software for geometric morphometric analyses* (R package).

These references are provided to document the methodological framework rather
than the executed software environment.

---

## Reproducibility notes

- Random seeds are fixed where applicable to ensure reproducible results.
- PCA is fit on training data only when used in supervised classification.
- Figures are displayed interactively unless explicitly exported by the user.
