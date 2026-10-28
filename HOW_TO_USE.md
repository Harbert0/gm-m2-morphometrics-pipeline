# How to Use This Repository

This is the **primary execution guide** for the `gm-m2-morphometrics-pipeline` repository, accompanying *Decoding Diets: Applying Machine Learning Models to Geometric Morphometric Analysis of Bovid Dental Mesowear Signatures*. For scientific background and citations, see [README.md](README.md).

## 1. Pipeline and run order

```text
M2 images
  → scripts/00_imagej/                Digitization/export
  → scripts/01_prepare_coordinates/   Format XY coordinates
  → scripts/02_gpa/                   GPA, aligned coordinates + metadata
       ├─ scripts/03_pca/             Exploratory PCA, plots and shape models
       ├─ scripts/04_lda/             LDA with model-specific PCA
       ├─ scripts/05_ml_models/       ML with PCA in modeling pipelines
       └─ Pagals_Lambda.R             Species-level coordinate phylogenetic signal
```

**Important:** PCA, LDA, ML, and Pagel's λ are separate analyses of the GPA-aligned coordinate table. You do **not** need to run the exploratory PCA notebook before running LDA or ML; the classification workflows handle their own PCA. The R analysis uses coordinates directly, not PCA scores.

The current repository contains `00_imagej`, `01_prepare_coordinates`, `02_gpa`, `03_pca`, `04_lda`, and `05_ml_models`.

## 2. Get the code and install software

Install ImageJ/Fiji, Python (preferably using conda), and Jupyter Notebook/JupyterLab. **R is additionally needed only for Pagel's λ.**

```bash
git clone https://github.com/Harbert0/gm-m2-morphometrics-pipeline.git
cd gm-m2-morphometrics-pipeline
conda env create -f environment.yml
conda activate gm-m2-morphometrics
jupyter lab
```

Alternative Python dependency installation:

```bash
pip install -r requirements.txt
```

The environment name shown above follows the existing guide; if the `name:` field in `environment.yml` differs, activate that name instead. Open notebooks in Jupyter and run their cells **top to bottom**, after updating configuration paths.

**Path convention:** Several uploaded notebooks use `../../results/...`. These relative paths assume the Jupyter working directory is the notebook's analysis folder (`scripts/02_gpa`, etc.). Check `Path.cwd()` in a code cell. Relative paths resolve against the working directory, not necessarily the notebook location. If unsure, set absolute paths.

## 3. Prepare the input data

### Step 0 — ImageJ/Fiji digitization (`scripts/00_imagej/`)

Digitize the 2D M2 outline consistently across specimens using the repository's ImageJ workflow and export the landmark XY coordinates. Keep the **same landmark numbering and anatomical orientation** for every specimen. Refer to the macro's instructions for its exact invocation and export naming.

### Step 1 — Coordinate formatting (`scripts/01_prepare_coordinates/`)

Run `prepare_coordinates.py` using the input and output settings defined in that script. The resulting table must have one row per specimen and 23 coordinate pairs named in the form:

```text
X1, Y1, X2, Y2, ... X23, Y23
```

Retain the metadata needed by later analyses (particularly `Species`, dietary class, and identifiers). Check that each specimen has 46 numeric coordinate values and that points are in the same order. **The command-line interface and exact output filename of `prepare_coordinates.py` were not verified from its full source in this review**; use the script's settings/help rather than assuming an undocumented command-line flag.

## 4. Run Generalized Procrustes Analysis (`scripts/02_gpa/`)

Open the GPA notebook (`GPA_Procrustes_workflow.ipynb` or the equivalent filename in the repository). At the top of the notebook set, for example:

```python
INPUT_FILE = Path("../../Data/Example_Data.csv")  # replace with actual prepared CSV
OUTPUT_DIR = Path("../../results/gpa")
SLIDE_SEMILANDMARKS = False
```

The uploaded GPA version contains `INPUT_FILE = Path("INSERT FILE PATH HERE")`; **replace this placeholder** before running. Run cells from top to bottom.

`SLIDE_SEMILANDMARKS` is **False by default** in the uploaded notebook, so that setting runs GPA without sliding. If enabled, the notebook uses its custom tangent-constrained semilandmark sliding procedure. Do not describe a default run as TPS bending-energy sliding. Check the actual landmark indices in the notebook before enabling sliding.

**Primary downstream input:**

```text
results/gpa/procrustes_aligned_coordinates.csv
```

**Other GPA outputs:** `gpa_specimen_summary.csv`, `gpa_convergence_history.csv`, `gpa_mean_shape.csv` and diagnostic plots such as aligned-shape overlay, convergence and Procrustes-distance histogram (when generated).

Before proceeding, verify that the aligned CSV contains `X1`, `Y1`, ... and that the needed specimen metadata survived preprocessing.

## 5. Run downstream analyses independently

Each of the next three notebooks reads `procrustes_aligned_coordinates.csv`. They can be run in any order after GPA.

### A. Exploratory PCA (`scripts/03_pca/`)

Open the PCA notebook and set:

```python
INPUT_FILE = Path("../../results/gpa/procrustes_aligned_coordinates.csv")
OUTPUT_DIR = Path("../../results/pca")
```

**Important code check:** In the supplied PCA notebook, one active cell also contains an absolute path under `/Users/rebeccaharbert/...` in `pd.read_csv(...)`. Replace that read with `pd.read_csv(INPUT_FILE)` or remove the obsolete cell before using the notebook on another machine. Run the notebook in order.

Outputs include `pca_scores_with_metadata.csv`, `pca_explained_variance.csv`, `pca_loadings.csv`, scree and PC scatter plots, loadings heatmap, and PC1/PC2 shape-model visualizations.

**Use:** exploratory interpretation of shape variation, *not* as a mandatory source of scores for either classifier.

### B. Linear Discriminant Analysis (`scripts/04_lda/`)

Open the LDA notebook and configure:

```python
INPUT_FILE = Path("../../results/gpa/procrustes_aligned_coordinates.csv")
OUTPUT_DIR = Path("../../results/lda")
```

The uploaded LDA notebook has a second, active `INPUT_FILE` assignment with `INSERT FILE PATH...` that **overrides** the usable path above it. Remove/replace that placeholder. Then run cells in order.

This workflow evaluates PC dimensionality with leave-one-out cross-validation; runs LDA with internally constructed PC predictors; compares shape-only and shape-plus-centroid-size predictors; and evaluates held-out test performance.

Main outputs include `lda_loocv_pc_selection.csv`, `lda_model_performance_summary.csv`, `lda_classification_report.csv`, `lda_confusion_matrix.csv`, `lda_test_set_predictions.csv`, `lda_misclassified_specimens.csv`, `lda_shape_vs_shape_cs_comparison.csv`, and plots/learning curves. Check the output directory for additional PCA and deformation-grid figures.

### C. Machine-learning classification (`scripts/05_ml_models/`)

Open the ML notebook and check:

```python
INPUT_FILE = Path("../../results/gpa/procrustes_aligned_coordinates.csv")
FALLBACK_INPUT_FILE = Path("../../Example_Data.csv")
OUTPUT_DIR = Path("../../results/ml_models")
```

The notebook will read the primary file if it exists, **otherwise it uses the fallback**. Confirm the printed chosen input: if you intend to classify GPA-aligned coordinates, ensure the primary CSV exists. A fallback run may not represent the same analysis.

Run all cells top to bottom. The models include Random Forest, k-nearest neighbors, and Gradient Boosting; the ML workflow fits PCA inside its training/cross-validation pipelines, and compares shape-only with shape-plus-centroid-size variants.

Outputs include `ml_model_performance_summary.csv`, `ml_model_metric_summary.csv`, `ml_shape_cs_model_performance_summary.csv`, `ml_shape_vs_shape_cs_comparison.csv`, misclassification CSVs, classification reports, confusion matrices, learning curves, and comparison figures.

## 6. Pagel's λ in R (separate analysis)

Locate `Pagals_Lambda.R` (note its uploaded filename spelling; check the path in your GitHub checkout) and open it in R/RStudio. It calls `install.packages` for `ape`, `phytools`, `dplyr`, `stringr`, `readr`, and `rotl`; install these if needed. The script also contacts the **Open Tree of Life** service, so internet access is required.

Run the script and use the file-picker from:

```r
data <- read_csv(file.choose())
```

Select `results/gpa/procrustes_aligned_coordinates.csv`. It expects a `Species` column and coordinate columns exactly named `X1`, `Y1`, and so forth. The script averages coordinates by species; matches species to Open Tree Taxonomy; generates an induced tree; adds Grafen branch lengths if none are present; estimates Pagel's λ per coordinate; and applies FDR correction.

Outputs are saved **to R's working directory**, including:

```text
bovid_tree_from_open_tree_renamed.tre
pagels_lambda_procrustes_coordinates.csv
pagels_lambda_procrustes_summary.csv
```

Use `getwd()` to see where they were written. Inspect the reported unmatched species and the number of matched tips before interpreting the analysis. The script uses a topology-derived branch-length approximation when required; those are not calibrated divergence times.

## 7. Troubleshooting and reproducibility checks

| Issue | Action |
|---|---|
| `FileNotFoundError` | Replace all `INSERT FILE PATH` placeholders and check `Path.cwd()` against relative paths. |
| PCA reads local `/Users/...` path | Replace the hard-coded `pd.read_csv(...)` line with `pd.read_csv(INPUT_FILE)`. |
| LDA cannot read its input | Remove its later placeholder `INPUT_FILE` assignment, which overrides the earlier valid path. |
| ML unexpectedly uses example data | Inspect the printed chosen input and ensure GPA output exists at `INPUT_FILE`. |
| Missing metadata columns | Verify that preprocessing and GPA retain specimen ID, `Species`, diet, and other required metadata. |
| Different results from manuscript | Confirm the input dataset, random seeds, train/test partitions, PC-selection settings, centroid-size option, and semilandmark sliding setting. |
| Pagel's λ species mismatch | Inspect Open Tree name-matching and unmatched-species diagnostics; verify exact `Species` names. |

The scripts are provided for research reproducibility. **Before claiming an exact reproduction of manuscript results**, record your script commit, package versions, data version, GPA sliding flag, and modeling configurations. In particular, changing sliding or using a fallback input changes the analysis.

## 8. Documentation scope

- [README.md](README.md): scientific background, aims, methods overview, and references.
- **HOW_TO_USE.md (this file):** execution order, input configuration, outputs, troubleshooting.
- `software.md`: additional software information.
- `environment.yml` and `requirements.txt`: Python environment specifications.


---



