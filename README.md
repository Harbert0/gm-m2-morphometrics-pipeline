# gm-m2-morphometrics-pipeline

A reproducible geometric morphometrics and classification workflow for investigating associations between mandibular second molar (M2) cusp shape and dietary categories in bovids.

## About the project

This repository accompanies the manuscript *Decoding Diets: Applying Machine Learning Models to Geometric Morphometric Analysis of Bovid Dental Mesowear Signatures*. It provides the computational workflow for converting digitized 2D dental landmarks into aligned shape coordinates, visualizing major patterns of shape variation, assessing phylogenetic signal, and evaluating dietary classification using linear and nonlinear statistical models.

## Getting started

**For installation, required data, exact run order, input paths, expected outputs, and troubleshooting, see [HOW_TO_USE.md](HOW_TO_USE.md).** 

## Data Processing workflow

1. **Landmark digitization:** M2 outline coordinates are digitized in ImageJ/Fiji and organized into a consistent specimen-by-coordinate table.
2. **Shape alignment:** Generalized Procrustes Analysis (GPA) removes translation, rotation, and scale differences. The supplied Python workflow provides an optional tangent-constrained semilandmark sliding procedure; whether sliding occurs depends on the GPA notebook setting.
3. **Exploratory shape analysis:** Principal Component Analysis (PCA) summarizes axes of aligned shape variation and supports scatter plots and shape-model visualizations.
4. **Supervised classification:** Linear Discriminant Analysis (LDA), Random Forest, k-nearest neighbors, and Gradient Boosting are used to evaluate relationships between shape predictors and dietary groups. Modeling workflows perform their own PCA rather than relying on exported exploratory PCA scores; shape-only and shape-plus-centroid-size variants are compared.
5. **Phylogenetic signal:** Pagel's λ is estimated separately for species-averaged Procrustes coordinate traits using an induced Open Tree of Life phylogeny, with false-discovery-rate correction.

The downstream PCA, LDA, ML, and phylogenetic analyses are **separate branches from the GPA-aligned coordinate dataset**, not four required sequential transformations.

## Repository structure

```text
Data/
scripts/
  00_imagej/
  01_prepare_coordinates/
  02_gpa/
  03_pca/
  04_lda/
  05_ml_models/
HOW_TO_USE.md
README.md
environment.yml
requirements.txt
software.md
LICENSE
```

The R phylogenetic script `Pagals_Lambda.R` is provided separately; consult [HOW_TO_USE.md](HOW_TO_USE.md) for its location and execution.

## Reproducibility and interpretation

The workflow provides coordinate processing, exploratory visualization, model fitting, cross-validation, held-out evaluation, and phylogenetic-signal estimates. Classification performance should be interpreted in the context of dietary class overlap, sampling, and potential taxonomic structure. Refer to the manuscript for the experimental rationale, analysis choices, and interpretation of results.

**Methodological note:** The uploaded GPA notebook currently sets `SLIDE_SEMILANDMARKS = False`. The optional sliding code uses a tangent-constrained distance-to-reference rule; The results in the manuscript for LDA and ML workflows were used with `SLIDE_SEMILANDMARKS = TRUE`

## References

Baken E, Collyer M, Kaliontzopoulou A, Adams D (2021). geomorph v4.0 and gmShiny: enhanced analytics and a new graphical interface for a comprehensive morphometric experience. *Methods in Ecology and Evolution*, 12, 2355–2363.

Adams D, Collyer M, Kaliontzopoulou A, Baken E (2025). *Geomorph: Software for geometric morphometric analyses.* R package version 4.0.10. https://cran.r-project.org/package=geomorph.

These geomorph references provide methodological context; the supplied GPA notebook uses a custom Python implementation rather than executing R/geomorph.

## License

See [LICENSE](LICENSE).
