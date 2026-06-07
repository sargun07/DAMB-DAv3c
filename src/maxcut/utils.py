import numpy as np
import pandas as pd

import config as cfg
from collections import Counter
from scipy.stats import wilcoxon
from pathlib import Path
import zipfile
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
INST_ROOT = DATA_DIR / "raw" / "mqlib_instances"
# =========================================================
# CATEGORY HELPERS
# =========================================================

def categorize_density(density):
    if density < 0.1:
        return "sparse"
    elif density < 0.5:
        return "balanced"
    return "dense"


def categorize_size(nodes):
    if nodes < 1024:
        return "xsmall"
    elif nodes < 2048:
        return "small"
    elif nodes < 4096:
        return "medium"
    elif nodes < 8192:
        return "large"
    return "xlarge"


# =========================================================
# SOLVER COMPARISON
# =========================================================

def compare_scores(a, b, eps=cfg.EPS):

    if abs(a - b) <= eps:
        return "tie"

    if a > b:
        return "win"

    return "loss"


def compute_cut_ratio(a, b):

    is_tie = abs(a - b) <= cfg.EPS


    if b == 0:
        return np.nan

    return a / b


# =========================================================
# FILTERS
# =========================================================

def filter_small_instances(df, solver_col=None):

    df_filtered = df[df[solver_col].notna()] if solver_col else df.copy()
    return df_filtered[
        (df_filtered ["limit"] > cfg.MIN_TIME_LIMIT)
        &
        (df_filtered ["size_cat"].isin(["xsmall", "small"]))
    ].copy()

def filter_main_instances(df, solver_col=None):

    df_filtered = df[df[solver_col].notna()] if solver_col else df.copy()
    return df_filtered[
        (df_filtered ["limit"] > cfg.MIN_TIME_LIMIT)
        &
        (~df_filtered ["size_cat"].isin(["xsmall", "small"]))
    ].copy()

def make_category_label(category, counts_per_category):
    label = cfg.CATEGORY_DISPLAY.get(category, category)
    count = int(counts_per_category.get(category, 0))

    if "\n\n" in label:
        main_label, size_label = label.split("\n\n")
        return f"{main_label} ({count})\n\n{size_label}"

    return f"{label} ({count})"

# =========================================================
# SUMMARY TABLES
# =========================================================

def conparison_summary(df):
    df["category"] = pd.Categorical(
    df["category"],
    categories=cfg.CATEGORY_ORDER,
    ordered=True)

    counts = (df
    .groupby(["category", "int_only", "result"])
    .size()
    .reset_index(name="count")
    .sort_values(["category", "int_only"]))

    pivot = (
    counts.pivot_table(
        index=["category", "int_only"],
        columns="result",
        values="count",
        fill_value=0
    )
    .reset_index())

    total = (
    counts.groupby(["category", "result"])["count"]
    .sum()
    .reset_index())

    total["int_only"] = "total"  

    total_pivot = (
    total.pivot_table(
        index=["category", "int_only"],
        columns="result",
        values="count",
        fill_value=0
    )
    .reset_index())
    pivot_final = pd.concat([pivot, total_pivot], ignore_index=True)

    pivot_final["int_only"] = pd.Categorical(
    pivot_final["int_only"],
    categories=[False, True, "total"],
    ordered=True)

    pivot_final["weight_type"] = pivot_final["int_only"].map({
    False: "float",
    True: "integer",
    "total": "total"})
    pivot_final = pivot_final.sort_values(["category", "int_only"])
    pivot_final["total"] = pivot_final[["loss", "tie", "win"]].sum(axis=1)

    summary = {}

    for _, row in pivot_final.iterrows():
        key = row["category"]
        vals = (row["loss"], row["tie"], row["win"])  

        if row["int_only"] == "total":
            summary[key] = vals
        elif row["int_only"] == False:
            summary[f"{key}_flt"] = vals

    return pivot_final, summary


# =========================================================
# CATEGORY ORDERING
# =========================================================

def apply_category_order(df):

    df["size_cat"] = pd.Categorical(
        df["size_cat"],
        categories=cfg.SIZE_ORDER,
        ordered=True
    )

    df["density_cat"] = pd.Categorical(
        df["density_cat"],
        categories=cfg.DENSITY_ORDER,
        ordered=True
    )

    return df


def compute_cut_ratio_counts(
    df,
    solver_col,
    baseline_col,
    int_col="int_only",
    eps=1e-9,
):
    """
    Compute cut-ratio bin counts for solver vs baseline.

    Ratio = solver_col / baseline_col.
    Ties are forced to ratio = 1 and placed in the {1.000} bin.
    Float instances are counted separately for overlay plotting.
    """

    df = df.copy()

    df["is_tie"] = (df[solver_col] - df[baseline_col]).abs() <= eps
    df["ratio"] = np.nan

    # Valid division
    mask_valid = df[baseline_col] != 0
    df.loc[mask_valid, "ratio"] = (
        df.loc[mask_valid, solver_col] / df.loc[mask_valid, baseline_col]
    )

    # Both zero means tie
    mask_both_zero = (df[baseline_col] == 0) & (df[solver_col] == 0)
    df.loc[mask_both_zero, "ratio"] = 1.0
    df.loc[mask_both_zero, "is_tie"] = True

    # Enforce all ties to ratio = 1
    df.loc[df["is_tie"], "ratio"] = 1.0

    # Avoid non-ties being visually counted as exact ties
    mask_false_one = (~df["is_tie"]) & (df["ratio"] == 1.0)

    df.loc[
        mask_false_one & (df[solver_col] > df[baseline_col]),
        "ratio"
    ] = 1.0000001

    df.loc[
        mask_false_one & (df[solver_col] < df[baseline_col]),
        "ratio"
    ] = 0.9999999

    def _get_counts(values, is_tie_mask):
        idx = np.digitize(values, cfg.CUT_RATIO_BINS) - 1

        # Tie bin index
        idx[is_tie_mask] = 8

        # Ensure non-tie losses stay below 1 and wins stay above 1
        idx[~is_tie_mask & (values < 1)] = np.minimum(
            idx[~is_tie_mask & (values < 1)], 7
        )
        idx[~is_tie_mask & (values > 1)] = np.maximum(
            idx[~is_tie_mask & (values > 1)], 9
        )

        idx = np.clip(idx, 0, len(cfg.CUT_RATIO_LABELS) - 1)

        counter = Counter(idx)
        return [counter.get(i, 0) for i in range(len(cfg.CUT_RATIO_LABELS))]

    counts_all = _get_counts(
        df["ratio"].to_numpy(),
        df["is_tie"].to_numpy()
    )

    if int_col in df.columns:
        mask_float = ~df[int_col].fillna(True)
        counts_float = _get_counts(
            df.loc[mask_float, "ratio"].to_numpy(),
            df.loc[mask_float, "is_tie"].to_numpy()
        )
    else:
        counts_float = None

    return {
        "df": df,
        "labels": cfg.CUT_RATIO_LABELS,
        "counts": counts_all,
        "counts_float": counts_float,
        "total": sum(counts_all),
        "tie_count": int(df["is_tie"].sum()),
        "ratio_one_count": int((df["ratio"] == 1.0).sum()),
    }

def run_wilcoxon(df, col_a, col_b, label):
    # Paired differences
    diff = df[col_a] - df[col_b]
    
    # Remove NaNs
    diff = diff.dropna()
    
    # Remove zero differences (ties)
    diff = diff[diff != 0]
    
    print(f"\n=== {label} ===")
    print(f"Samples used: {len(diff)}")
    
    if len(diff) == 0:
        print("No valid samples after removing ties.")
        return
    
    # Wilcoxon test
    stat, p_value = wilcoxon(diff, alternative='two-sided')
    
    # Effect size (rank-biserial correlation)
    n = len(diff)
    z = (stat - (n*(n+1)/4)) / np.sqrt(n*(n+1)*(2*n+1)/24)
    r = abs(z) / np.sqrt(n)
    
    print(f"Wilcoxon statistic: {stat}")
    print(f"p-value: {p_value:.4e}")
    print(f"Effect size (r): {r:.4f}")
    
    # Interpretation
    if p_value < 0.05:
        print("Result: Statistically significant")
    else:
        print("Result: Not statistically significant")

def wilcoxon_by_category(df, col_a, col_b, category_col="category"):
    results = []

    for cat in sorted(df[category_col].dropna().unique()):
        sub = df[df[category_col] == cat]
        
        diff = sub[col_a] - sub[col_b]
        diff = diff.dropna()
        diff = diff[diff != 0]  # remove ties
        
        n = len(diff)
        
        if n < 10:  # avoid unreliable small samples
            results.append((cat, n, None, None, None, "Too small"))
            continue
        
        stat, p = wilcoxon(diff,alternative="two-sided")
        
        # Effect size (r)
        z = (stat - (n*(n+1)/4)) / np.sqrt(n*(n+1)*(2*n+1)/24)
        r = abs(z) / np.sqrt(n)
        
        results.append((cat, n, stat, p, r,
                        "Significant" if p < 0.05 else "Not significant"))

    return results

def run_wilcoxon_multiple_dfs(
    comparisons,
    group_col=None,
    min_n=1,
    alpha=0.05,
    remove_ties=True,
):
    results = []

    for comp in comparisons:

        df = comp["df"]
        solver_col = comp["solver_col"]
        baseline_col = comp["baseline_col"]
        comparison_label = comp["label"]

        if group_col is None:
            groups = [("all", df)]
        else:
            groups = [
                (group, df[df[group_col] == group])
                for group in sorted(df[group_col].dropna().unique())
            ]

        for group_name, subset in groups:

            diff = subset[solver_col] - subset[baseline_col]
            diff = diff.dropna()

            if remove_ties:
                diff = diff[diff != 0]

            n = len(diff)

            if n < min_n:
                results.append({
                    "comparison": comparison_label,
                    "group": group_name,
                    "n": n,
                    "wilcoxon_stat": np.nan,
                    "p_value": np.nan,
                    "effect_size_r": np.nan,
                    "median_difference": np.nan,
                    "mean_difference": np.nan,
                    "significant": False,
                    "status": "Too small",
                })
                continue

            stat, p_value = wilcoxon(diff, alternative="two-sided")

            z = (
                stat - (n * (n + 1) / 4)
            ) / np.sqrt(
                n * (n + 1) * (2 * n + 1) / 24
            )

            r = abs(z) / np.sqrt(n)

            results.append({
                "comparison": comparison_label,
                "group": group_name,
                "n": n,
                "wilcoxon_stat": stat,
                "p_value": p_value,
                "effect_size_r": r,
                "median_difference": np.median(diff),
                "mean_difference": np.mean(diff),
                "significant": p_value < alpha,
                "status": "Significant" if p_value < alpha else "Not significant",
            })

    return pd.DataFrame(results)

def print_wilcoxon_Pairwise_results(results, title):
    print(f"\n=== {title} ===")
    for cat, n, stat, p, r, status in results:
        if p is None:
            print(f"{cat:20s} | n={n:3d} | Skipped ({status})")
        else:
            print(f"{cat:20s} | n={n:3d} | p={p:.2e} | r={r:.3f} | {status}")


def make_weighttype_wtl_summary(df, solver_name):
    """
    Creates win-tie-loss counts by weight type for one solver.

    Expected columns:
        int_only, result

    Returns columns:
        solver, weight_type, loss, tie, win
    """

    summary = (
        df.groupby(["int_only", "result"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["loss", "tie", "win"], fill_value=0)
        .reset_index()
        .rename(columns={"int_only": "weight_type"})
    )

    summary["weight_type"] = summary["weight_type"].replace({
        "int": "integer",
        "flt": "float",
        "integer": "integer",
        "float": "float",
    })

    summary["solver"] = solver_name

    return summary[["solver", "weight_type", "loss", "tie", "win"]]

def tie_loss_win_counts(df_dav2=None, df_dav3=None, df_dav3c=None):
    """
    Combines win-tie-loss counts for DAv2, DAv3, and DAv3c
    by integer/float weight type.
    """

    solver_dfs = {
        "DAv2": df_dav2,
        "DAv3": df_dav3,
        "DAv3c": df_dav3c,
    }

    summary = pd.concat(
        [
            make_weighttype_wtl_summary(df, solver_name)
            for solver_name, df in solver_dfs.items()
            if df is not None
        ],
        ignore_index=True,
    )
    

    summary["weight_type"] = summary["weight_type"].replace({
    True: "integer",
    False: "float"})

    return summary


# Find ZIP file
def find_zip_for_graph(graph_name: str) -> Path | None:
    hit = list(INST_ROOT.rglob(f"{graph_name}.zip"))
    if hit:
        return hit[0]

    hit2 = [p for p in INST_ROOT.rglob("*.zip") if graph_name in p.stem]
    return hit2[0] if hit2 else None


# Read Edgelist
def read_edgelist_from_zip(zip_path: Path):
    with zipfile.ZipFile(zip_path, "r") as zfp:
        inner_files = [n for n in zfp.namelist() if not n.endswith("/")]
        if not inner_files:
            raise ValueError(f"No files inside zip: {zip_path}")

        inner_name = inner_files[0]
        data = zfp.read(inner_name).decode("utf-8", errors="ignore").splitlines()

    edges = []
    nodes = set()

    for line in data:
        line = line.strip()
        if not line or line.startswith(("#", "%", "c", "p")):
            continue

        parts = re.split(r"\s+", line)
        if len(parts) <= 2:
            continue

        try:
            u = int(parts[0])
            v = int(parts[1])
            w = float(parts[2]) 
        except ValueError:
            continue

        edges.append((u, v, w))
        nodes.update([u, v])

    if not edges:
        raise ValueError(f"No edges parsed from {zip_path}")

    # Normalize to 0-based
    if not any(u == 0 or v == 0 for u, v, _ in edges):
        edges = [(u - 1, v - 1, w) for u, v, w in edges]

    n = max(max(u, v) for u, v, _ in edges) + 1
    return n, edges


def compute_distribution_stats(series):
    """
    Compute descriptive statistics for a numeric pandas Series.
    """

    vals = series.dropna()

    return {
        "min": vals.min(),
        "q25": np.percentile(vals, 25),
        "median": np.median(vals),
        "q75": np.percentile(vals, 75),
        "max": vals.max(),
        "mean": vals.mean(),
        "std": vals.std(),
        "unique_count": vals.nunique(),
        "count": len(vals),
    }

def compare_structure_metric(
    df,
    metric_col,
    structure_groups=None,
    round_digits=4
):
    """
    Compute descriptive statistics for a metric
    across structure groups.
    """

    if structure_groups is None:
        structure_groups = [
            "non_bipartite_with_triangles",
            "non_bipartite_triangle_free",
        ]

    rows = []

    for group in structure_groups:

        subset = df[df["structure_group"] == group]

        stats = compute_distribution_stats(
            subset[metric_col]
        )

        stats["structure_group"] = group

        rows.append(stats)

    result_df = pd.DataFrame(rows)

    # reorder columns
    result_df = result_df[
        [
            "structure_group",
            "count",
            "min",
            "q25",
            "median",
            "q75",
            "max",
            "mean",
            "std",
            "unique_count",
        ]
    ]

    return result_df.round(round_digits)

def classify_float_weight_structure(unique_ratio, unique_weights):
    if unique_weights == 1:
        return "uniform"
    elif unique_ratio < 0.05:
        return "u05"
    elif unique_ratio < 0.10:
        return "u10"
    elif unique_ratio < 0.50:
        return "u50"
    elif unique_ratio == 1:
        return 'allU'
    elif unique_ratio > 0.95:
        return 'gt95'
    elif unique_ratio > 0.75:
        return 'gt75'
    else:
        return "None"
    
def classify_weight_structure(n90, unique_weights):

    if unique_weights == 1:
        return "uniform"

    elif n90 <= 5:
        return "strongly_repeated"

    elif n90 <= 50:
        return "weakly_repeated"

    else:
        return "highly_diverse"
    
def get_cdf_table(
    df,
    objective_col="Objective Value",
    thresholds=[1e-6, 0.01, 0.05, 0.1, 0.2, 0.5],
):
    """
    Generate a CDF table showing the fraction of instances solved
    within specified relative-gap thresholds.

    Relative gap is computed as:

        (Objective Value - Solver Value) / Objective Value

    A tolerance is used so that tiny numerical errors are treated
    as optimal solutions.
    """

    stats = []

    df = df.dropna(subset=cfg.SOLVERS + [objective_col])

    for solver in cfg.SOLVERS:

        gaps = (
            (df[objective_col] - df[solver]) /
            df[objective_col]
        )

        gaps = gaps.dropna()

        # Treat tiny floating-point errors as exact zero
        gaps = gaps.mask(gaps <= cfg.EPS, 0.0)

        gaps = gaps.sort_values()

        total_n = len(gaps)

        if total_n == 0:
            continue

        solver_results = {
            "Solver": solver,
            "n": total_n
        }

        for t in thresholds:

            fraction = (gaps <= t).mean()

            if t == cfg.EPS:
                col_name = rf"Gap $\leq 10^{{-6}}$"
            else:
                col_name = f"Gap ≤ {t}"

            solver_results[col_name] = f"{fraction:.2%}"

        stats.append(solver_results)

    cdf_df = pd.DataFrame(stats).set_index("Solver")

    return cdf_df

def pairwise_win_tie_loss_by_weight_category(
    df,
    solver_a,
    solver_b,
    category_col="weight_frequency_category",
    eps=1e-9
):
    results = []

    for category, group in df.groupby(category_col):

        # keep only rows where both solvers have values
        sub = group[[solver_a, solver_b]].dropna()

        n = len(sub)

        if n == 0:
            results.append({
                "category": category,
                "n": 0,
                f"{solver_a}_wins": 0,
                "ties": 0,
                f"{solver_b}_wins": 0,
                f"{solver_a}_win_pct": np.nan,
                "tie_pct": np.nan,
                f"{solver_b}_win_pct": np.nan,
            })
            continue

        diff = sub[solver_a] - sub[solver_b]

        a_wins = (diff > eps).sum()
        ties = (diff.abs() <= eps).sum()
        b_wins = (diff < -eps).sum()

        results.append({
            "category": category,
            "n": n,
            f"{solver_a}_wins": a_wins,
            "ties": ties,
            f"{solver_b}_wins": b_wins,
            f"{solver_a}_win_pct": a_wins / n * 100,
            "tie_pct": ties / n * 100,
            f"{solver_b}_win_pct": b_wins / n * 100,
        })

    return pd.DataFrame(results)

    