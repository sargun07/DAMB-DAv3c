from pathlib import Path
import numpy as np

# =========================================================
# ROOT PATHS
# =========================================================
# Project root is assumed to be three levels above this file.
# Example: src/config/settings.py -> project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Main data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"                  # Original/raw input files
PROCESSED_DIR = DATA_DIR / "processed"      # Cleaned and processed datasets
METADATA_DIR = DATA_DIR / "metadata"        # Metadata and auxiliary files

# Main results directory
RESULTS_DIR = ROOT_DIR / "results"

# Output directories for different result types
FIGURE_DIR = RESULTS_DIR / "figures"
TABLE_DIR = RESULTS_DIR / "tables"
STAT_DIR = RESULTS_DIR / "statistics"
EXPORT_DIR = RESULTS_DIR / "exports"
LOG_DIR = RESULTS_DIR / "logs"

# Notebook directory
NOTEBOOK_DIR = ROOT_DIR / "notebooks"

# =========================================================
# RANDOMNESS
# =========================================================
# Global random seed for reproducibility.
RANDOM_SEED = 42

# =========================================================
# NUMERICAL CONSTANTS
# =========================================================
# Small tolerance used for floating-point comparisons.
EPS = 1e-9

# Minimum time-limit fraction used in filtered benchmark analyses.
MIN_TIME_LIMIT = 0.25

# Runtime bounds used for DAv3c runtime analysis.
DAV3C_MIN_RUNTIME = 1
DAV3C_MAX_RUNTIME = 3600

# =========================================================
# CATEGORY ORDERS
# =========================================================
# Standard order for graph-size categories.
SIZE_ORDER = [
    "xsmall",
    "small",
    "medium",
    "large",
    "xlarge"
]

# Standard order for density categories.
DENSITY_ORDER = [
    "sparse",
    "balanced",
    "dense"
]

# Order for structural graph categories.
STRUCTURAL_ORDER = [
    "bipartite",
    "triangle_free",
    "triangle_dense"
]

# Order for edge-weight repetition/diversity categories.
CATEGORY_ORDER_UW = [
    "uniform",
    "strongly_repeated",
    "weakly_repeated",
    "highly_diverse"
]

# =========================================================
# PLOT SETTINGS
# =========================================================
# Default resolution for saved figures.
FIG_DPI = 300

# Global switch controlling whether plots are saved to disk.
SAVE_FIGURES = True

# Common figure sizes used across plotting functions.
FIGSIZE_STANDARD = (8, 5)
FIGSIZE_WIDE = (12, 5)

# =========================================================
# SOLVER SETTINGS AND COLORS
# =========================================================
# Solver order used in tables, plots, and comparisons.
SOLVERS = ["DAv2", "DAv3", "DAv3c", "heuristic"]

# Consistent solver colors used across all figures.
SOLVER_COLORS = {
    "DAv3c": "#1f77b4",
    "DAv2": "#ff7f0e",
    "DAv3": "#2ca02c",
    "heuristic": "#d62728"
}

# =========================================================
# SIZE-DENSITY CATEGORY ORDER
# =========================================================
# Combined size-density category order used for grouped plots.
CATEGORY_ORDER = [
    "xsmall_sparse",
    "xsmall_balanced",
    "xsmall_dense",

    "small_sparse",
    "small_balanced",
    "small_dense",

    "medium_sparse",
    "medium_balanced",
    "medium_dense",

    "large_sparse",
    "large_balanced",
    "large_dense",

    "xlarge_sparse",
    "xlarge_balanced",
    "xlarge_dense"
]

# =========================================================
# CATEGORY DISPLAY LABELS
# =========================================================
# Display labels for size-density plots.
# New lines are used to group density labels under each size category.
CATEGORY_DISPLAY = {
    "xsmall_sparse": "Sparse",
    "xsmall_balanced": "Balanced\n\nXsmall",
    "xsmall_dense": "Dense",

    "small_sparse": "Sparse",
    "small_balanced": "Balanced\n\nSmall",
    "small_dense": "Dense",

    "medium_sparse": "Sparse",
    "medium_balanced": "Balanced\n\nMedium",
    "medium_dense": "Dense",

    "large_sparse": "Sparse",
    "large_balanced": "Balanced\n\nLarge",
    "large_dense": "Dense",

    "xlarge_sparse": "Sparse\n\nXlarge",
    "xlarge_balanced": "Balanced\n\nXlarge",
    "xlarge_dense": "Dense\n\nXlarge"
}

# MQLib heuristic selected for each size-density category.
HEURISTIC_LABEL_BY_CATEGORY = {
    "medium_sparse": "BURER2002",
    "medium_balanced": "PAL2004bMTS2",
    "medium_dense": "PAL2004bMTS2",

    "large_sparse": "BURER2002",
    "large_balanced": "PAL2004bMTS2",
    "large_dense": "PAL2004bMTS2",

    "xlarge_sparse": "MERZ1999GLS",
}

# =========================================================
# BENCHMARK COLORS
# =========================================================
# Colors used for win/tie/loss outcome visualizations.
BENCHMARK_COLORS = {
    "loss": "#ADD8E6",
    "tie": "#FFFACD",
    "win": "#B2E5B2"
}

# =========================================================
# HATCH SETTINGS
# =========================================================
# Hatch patterns used to visually distinguish float and integer instances.
FLOAT_HATCH = "///"
INTEGER_HATCH = None

# =========================================================
# CUT-RATIO BINNING
# =========================================================
# Bins used to group DAv3c/heuristic cut-value ratios.
# Values below 1 indicate DAv3c is worse than the heuristic,
# exactly 1 indicates a tie, and values above 1 indicate DAv3c is better.
CUT_RATIO_BINS = np.array([
    -np.inf, 0.986, 0.988, 0.990, 0.992, 0.994, 0.996, 0.998,
    1.000, 1.0000001,
    1.002, 1.004, 1.006, 1.008, 1.01, 1.012, 1.014,
    np.inf
])

# Human-readable labels corresponding to CUT_RATIO_BINS.
CUT_RATIO_LABELS = [
    "(-inf, 0.986)", "[0.986, 0.988)", "[0.988, 0.990)", "[0.990, 0.992)",
    "[0.992, 0.994)", "[0.994, 0.996)", "[0.996, 0.998)",
    "[0.998, <1)", "{1.000}",
    "(>1, 1.002]", "(1.002, 1.004]", "(1.004, 1.006]",
    "(1.006, 1.008]", "(1.008, 1.01]", "(1.01, 1.012]",
    "(1.012, 1.014]", "(1.014, inf)"
]