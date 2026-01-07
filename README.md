# gm-m2-morphometrics-pipeline
Reproducible pipeline for geometric morphpometrics of bovid M2 landmarks: ImageJ export -> Generalized Procrustes Analysis  with sliding semilandmarks ->PCA -> LDA and ML classification

# Geometric Morphometrics Pipeline (GPA with Sliding Semilandmarks)


This repository contains a reproducible geometric morphometrics workflow for
processing 2D landmark data from digitized specimens. The pipeline implements
Generalized Procrustes Analysis (GPA) with sliding semilandmarks, followed by
multivariate and supervised classification analyses of Procrustes-aligned shapes.

The workflow follows established geometric morphometric procedures for GPA and 
semilandmark sliding (e.g., geomorph; Adams et al., 2025; Baken et al., 2021). 
GPA and semilandmakr sliding were implemented in Python using a custom workflow 
conceptually aligned with the geomorph framework. 

---

## Pipeline overview

1. **Landmark digitization and export (ImageJ)**
   - Digitized landmarks are exported as shifted XY coordinates using an ImageJ macro.

2. **Coordinate preprocessing**
   - Landmark coordinates are reshaped and formatted for GPA.

3. **Generalized Procrustes Analysis with sliding semilandmarks**
   - GPA is used to remove variation due to translation, rotation, and scale.
   - The first and last landmarks are treated as fixed anatomical landmarks,
     while intermediate points are treated as sliding semilandmarks.
   - Semilandmarks are adjusted to minimize thin-plate spline (TPS) bending energy
     relative to a reference shape.
   - GPA and semilandmark sliding are implemented in Python using a custom workflow
     conceptually consistent with geomorph.

4. **Metadata concatenation**
   - Procrustes-aligned coordinates are merged with specimen metadata.

5. **Multivariate analysis**
   - Principal Component Analysis (PCA) of Procrustes-aligned coordinates.

6. **Classification**
   - Linear Discriminant Analysis (LDA)
   - Machine learning models (Random Forest, kNN, Gradient Boosting)
   - Cross-validation, learning curves, and misclassification analysis

---

## References


Baken E, Collyer M, Kaliontzopoulou A, Adams D (2021). “geomorph v4.0 and gmShiny: enhanced analytics and a new graphical interface for a comprehensive morphometric experience.” Methods in Ecology and Evolution, 12, 2355-2363.

Adams D, Collyer M, Kaliontzopoulou A, Baken E (2025). “Geomorph: Software for geometric morphometric analyses. R package version 4.0.10.” https://cran.r-project.org/package=geomorph.
