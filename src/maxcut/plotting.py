import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import Patch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import LogLocator
from matplotlib.lines import Line2D
import config as cfg
import utils



# =========================================================
# GLOBAL STYLE
# =========================================================

def set_plot_style():

    sns.set_theme(style="whitegrid")

    plt.rcParams["figure.dpi"] = cfg.FIG_DPI
    plt.rcParams["savefig.dpi"] = cfg.FIG_DPI


# =========================================================
# SAVE FIGURE
# =========================================================

def save_figure(fig, filename):

    if cfg.SAVE_FIGURES:

        fig.savefig(
            cfg.FIGURE_DIR / filename,
            bbox_inches="tight"
        )


# =========================================================
# GENERIC BAR PLOT
# =========================================================

def plot_bar(
    data,
    x,
    y,
    title=None,
    figsize=cfg.FIGSIZE_STANDARD
):

    fig, ax = plt.subplots(figsize=figsize)

    sns.barplot(
        data=data,
        x=x,
        y=y,
        ax=ax
    )

    if title:
        ax.set_title(title)

    return fig, ax
    

def plot_win_tie_loss_with_float_hatch(
    summary,
    pivot_table,
    title,
    save_name=None,
    loss_label="Solver",
    win_label="DAv3c",
    use_category_loss_labels=False,
    figsize=(12, 8),
):
    """
    summary format:
        summary["medium_sparse"] = (loss, tie, win)
        summary["medium_sparse_flt"] = (loss_float, tie_float, win_float)

    Interpretation:
        loss = loss_label wins
        tie  = both tie
        win  = win_label wins
    """

    set_plot_style()

    counts_per_category = (
    pivot_table[pivot_table["int_only"] == "total"]
    .set_index("category")["total"]
    .to_dict()
    )
    category_order = cfg.CATEGORY_ORDER

    outcome_order = ["loss", "tie", "win"]

    colors = {
        "loss": cfg.BENCHMARK_COLORS["loss"],
        "tie": cfg.BENCHMARK_COLORS["tie"],
        "win": cfg.BENCHMARK_COLORS["win"],
    }

    fig, ax = plt.subplots(figsize=figsize)

    available_categories = [
        c for c in category_order
        if c in summary and sum(summary[c]) > 0
    ]

    x_positions = np.arange(len(available_categories))
    width = 0.9

    for idx, category in enumerate(available_categories):

        base_vals = summary.get(category, (0, 0, 0))
        float_vals = summary.get(f"{category}_flt", (0, 0, 0))

        total = sum(base_vals)

        if total == 0:
            continue

        if use_category_loss_labels:
            current_loss_label = cfg.HEURISTIC_LABEL_BY_CATEGORY.get(
                category,
                loss_label
            )
        else:
            current_loss_label = loss_label

        outcome_labels = {
            "loss": current_loss_label,
            "tie": "Both",
            "win": win_label,
        }

        bottom = 0

        for i, outcome in enumerate(outcome_order):

            base_height = base_vals[i] / total
            float_height = float_vals[i] / total if float_vals else 0

            ax.bar(
                idx,
                base_height,
                bottom=bottom,
                width=width,
                color=colors[outcome],
                edgecolor="black",
            )

            if float_height > 0:
                ax.bar(
                    idx,
                    float_height,
                    bottom=bottom,
                    width=width,
                    color="none",
                    edgecolor="black",
                    hatch=cfg.FLOAT_HATCH,
                )

                ax.text(
                    idx + 0.35,
                    bottom + float_height + 0.005,
                    f"{float_height * 100:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

            if base_height > 0.05:
                middle = bottom + base_height / 2

                ax.text(
                    idx,
                    middle,
                    f"{base_height * 100:.1f}",
                    ha="center",
                    va="center",
                    fontsize=10,
                    weight="bold",
                    path_effects=[
                        pe.withStroke(linewidth=3, foreground="white")
                    ],
                )

                ax.text(
                    idx,
                    middle - 0.04,
                    outcome_labels[outcome],
                    ha="center",
                    va="center",
                    fontsize=9,
                    weight="bold",
                    path_effects=[
                        pe.withStroke(linewidth=3, foreground="white")
                    ],
                )

            elif base_height > 0.01:
                ax.text(
                    idx,
                    bottom + base_height / 2,
                    f"{base_height * 100:.1f} {outcome_labels[outcome]}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    weight="bold",
                )

            bottom += base_height

 
    xtick_labels = [
    utils.make_category_label(c, counts_per_category)
    for c in available_categories]

        
    ax.set_xticks(x_positions)
    ax.set_xticklabels(xtick_labels)

    ax.set_ylabel("Proportion of instances (%)")

    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels([0, 20, 40, 60, 80, 100])

    
    ax.set_title(title)

    ax.tick_params(axis="x", bottom=False, top=False)

    legend_items = [
        mpatches.Patch(
            facecolor="white",
            edgecolor="black",
            hatch=cfg.FLOAT_HATCH,
            label="Float",
        )
    ]

    alegend = ax.legend(handles=legend_items)
    alegend.get_frame().set_alpha(0.4)

    plt.tight_layout()

    if save_name:
        save_figure(fig, save_name)

    return fig, ax


# =========================================================
# FLOAT / INTEGER STACKED BAR PLOT
# =========================================================
def plot_win_tie_loss_by_weight_type(
    pivot_df,
    title,
    save_name=None,
    loss_label="Solver",
    win_label="DAv3c",
    use_category_loss_labels=False,
    figsize=(12, 8),
):
    """
    Plots win-tie-loss proportions separately for integer and float instances.

    pivot_df expected columns:
        category, weight_type, loss, tie, win

    Interpretation:
        loss = loss_label wins
        tie  = both tie
        win  = win_label wins
    """

    set_plot_style()

    outcome_order = ["loss", "tie", "win"]

    colors = {
        "loss": cfg.BENCHMARK_COLORS["loss"],
        "tie": cfg.BENCHMARK_COLORS["tie"],
        "win": cfg.BENCHMARK_COLORS["win"],
    }

    available_categories = []

    counts_per_category = {}

    for category in cfg.CATEGORY_ORDER:

        cat_df = pivot_df[pivot_df["category"] == category]

        if cat_df.empty:
            continue

        int_row = cat_df[cat_df["weight_type"] == "integer"]
        float_row = cat_df[cat_df["weight_type"] == "float"]

        int_count = 0
        float_count = 0

        if not int_row.empty:
            r = int_row.iloc[0]
            int_count = r["loss"] + r["tie"] + r["win"]

        if not float_row.empty:
            r = float_row.iloc[0]
            float_count = r["loss"] + r["tie"] + r["win"]

        if int_count == 0 and float_count == 0:
            continue

        available_categories.append(category)

        counts_per_category[category] = int(int_count + float_count)

    fig, ax = plt.subplots(figsize=figsize)

    x_positions = np.arange(len(available_categories))
    width = 0.38

    for idx, category in enumerate(available_categories):

        cat_df = pivot_df[pivot_df["category"] == category]

        for weight_type, x_shift, hatch in [
            ("integer", -width / 2, None),
            ("float", width / 2, cfg.FLOAT_HATCH),
        ]:

            row = cat_df[cat_df["weight_type"] == weight_type]

            if row.empty:
                continue

            row = row.iloc[0]

            total = row["loss"] + row["tie"] + row["win"]

            if total == 0:
                continue

            if use_category_loss_labels:
                current_loss_label = cfg.HEURISTIC_LABEL_BY_CATEGORY.get(
                    category,
                    loss_label
                )
            else:
                current_loss_label = loss_label

            outcome_labels = {
                "loss": current_loss_label,
                "tie": "Both",
                "win": win_label,
            }

            bottom = 0

            for outcome in outcome_order:

                value = row[outcome] / total

                ax.bar(
                    idx + x_shift,
                    value,
                    bottom=bottom,
                    width=width,
                    color=colors[outcome],
                    edgecolor="black",
                    hatch=hatch,
                )

                if value > 0.05:
                    middle = bottom + value / 2

                    ax.text(
                        idx + x_shift,
                        middle,
                        f"{value * 100:.1f}",
                        ha="center",
                        va="center",
                        fontsize=9,
                        weight="bold",
                        path_effects=[
                            pe.withStroke(linewidth=3, foreground="white")
                        ],
                    )

                    ax.text(
                        idx + x_shift,
                        middle - 0.04,
                        outcome_labels[outcome],
                        ha="center",
                        va="center",
                        fontsize=8,
                        weight="bold",
                        path_effects=[
                            pe.withStroke(linewidth=3, foreground="white")
                        ],
                    )

                elif value > 0.01:
                    ax.text(
                        idx + x_shift,
                        bottom + value / 2,
                        f"{value * 100:.1f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        weight="bold",
                    )

                bottom += value

    xtick_labels = [
        utils.make_category_label(c, counts_per_category)
        for c in available_categories
    ]

    ax.set_xticks(x_positions)
    ax.set_xticklabels(xtick_labels)

    ax.set_ylabel("Proportion of instances (%)")

    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels([0, 20, 40, 60, 80, 100])

    ax.set_ylim(0, 1.03)

    ax.set_title(title)

    ax.tick_params(axis="x", bottom=False, top=False)

    legend_items = [
        mpatches.Patch(
            facecolor="white",
            edgecolor="black",
            label="Integer",
        ),
        mpatches.Patch(
            facecolor="white",
            edgecolor="black",
            hatch=cfg.FLOAT_HATCH,
            label="Float",
        ),
    ]

    alegend = ax.legend(handles=legend_items)
    alegend.get_frame().set_alpha(0.4)

    plt.tight_layout()

    if save_name:
        save_figure(fig, save_name)

    return fig, ax

# =========================================================
# COMBINED SOLVER FLOAT VS INTEGER
# =========================================================

def plot_combined_solver_weighttype_wtl(
    summary,
    title="Performance Comparison by Solver and Weight Type",
    save_name=None,
    loss_label="MQLib Heuristic",
    win_label="Solver",
    figsize=(10, 6),
    legend_alpha=0.7,
):
    """
    Plots win-tie-loss proportions for DAv2, DAv3, and DAv3c,
    with integer and float instances shown as separate bars.

    summary expected columns:
        solver, weight_type, loss, tie, win

    Interpretation:
        loss = loss_label wins
        tie  = both tie
        win  = win_label wins
    """

    set_plot_style()

    solver_order = ["DAv2", "DAv3", "DAv3c"]
    outcome_order = ["loss", "tie", "win"]

    colors = {
        "loss": cfg.BENCHMARK_COLORS["loss"],
        "tie": cfg.BENCHMARK_COLORS["tie"],
        "win": cfg.BENCHMARK_COLORS["win"],
    }

    fig, ax = plt.subplots(figsize=figsize)

    x_positions = np.arange(len(solver_order))
    width = 0.36

    bar_specs = {
        "integer": {
            "x_shift": -width / 2,
            "hatch": None,
        },
        "float": {
            "x_shift": width / 2,
            "hatch": cfg.FLOAT_HATCH,
        },
    }

    for solver_idx, solver in enumerate(solver_order):

        outcome_labels = {
            "loss": loss_label,
            "tie": "Both",
            "win": solver,
        }

        for weight_type, spec in bar_specs.items():

            row = summary[
                (summary["solver"] == solver)
                & (summary["weight_type"] == weight_type)
            ]

            if row.empty:
                continue

            row = row.iloc[0]

            total = row["loss"] + row["tie"] + row["win"]

            if total == 0:
                continue

            bottom = 0
            x = solver_idx + spec["x_shift"]

            for outcome in outcome_order:

                value = row[outcome] / total

                ax.bar(
                    x,
                    value,
                    bottom=bottom,
                    width=width,
                    color=colors[outcome],
                    edgecolor="black",
                    hatch=spec["hatch"],
                )

                if value > 0.05:
                    middle = bottom + value / 2

                    ax.text(
                        x,
                        middle,
                        f"{value * 100:.1f}",
                        ha="center",
                        va="center",
                        fontsize=9,
                        weight="bold",
                        path_effects=[
                            pe.withStroke(linewidth=3, foreground="white")
                        ],
                    )

                    ax.text(
                        x,
                        middle - 0.04,
                        outcome_labels[outcome],
                        ha="center",
                        va="center",
                        fontsize=8,
                        weight="bold",
                        path_effects=[
                            pe.withStroke(linewidth=3, foreground="white")
                        ],
                    )

                elif value > 0.01:
                    ax.text(
                        x,
                        bottom + value / 2,
                        f"{value * 100:.1f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        weight="bold",
                    )

                bottom += value

    ax.set_xticks(x_positions)
    ax.set_xticklabels(solver_order)

    ax.set_ylabel("Proportion of instances (%)")

    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticklabels([0, 20, 40, 60, 80, 100])

    ax.set_ylim(0, 1.03)

    ax.set_title(title)

    ax.tick_params(axis="x", bottom=False, top=False)

    legend_items = [
        mpatches.Patch(
            facecolor="white",
            edgecolor="black",
            label="Integer",
        ),
        mpatches.Patch(
            facecolor="white",
            edgecolor="black",
            hatch=cfg.FLOAT_HATCH,
            label="Float",
        ),
    ]

    legend = ax.legend(
        handles=legend_items,
        frameon=True,
        fontsize=11,
    )

    legend.get_frame().set_alpha(legend_alpha)

    plt.tight_layout()

    if save_name:
        save_figure(fig, save_name)

    return fig, ax


# =========================================================
# GENERIC BOXPLOT
# =========================================================

def plot_boxplot(
    values,
    ylabel,
    title=None,
    save_name=None,
    figsize=cfg.FIGSIZE_STANDARD
):
    set_plot_style()

    fig, ax = plt.subplots(figsize=figsize)

    ax.boxplot(
        values.dropna(),
        vert=True
    )

    ax.set_ylabel(ylabel)

    if title:
        ax.set_title(title)

    plt.tight_layout()

    if save_name:
        save_figure(fig, save_name)

    return fig, ax

# =========================================================
# VIOLIN PLOT
# =========================================================

def plot_violin(
    data,
    labels,
    ylabel,
    title=None,
    log_scale=False,
    showmeans=True,
    save_name=None,
    figsize=cfg.FIGSIZE_STANDARD
):
    set_plot_style()

    fig, ax = plt.subplots(figsize=figsize)

    ax.violinplot(
        data,
        showmeans=showmeans
    )

    ax.set_xticks(
        np.arange(1, len(labels) + 1)
    )

    ax.set_xticklabels(labels)

    ax.set_ylabel(ylabel)

    if log_scale:
        ax.set_yscale("log")

    if title:
        ax.set_title(title)

    plt.tight_layout()

    if save_name:
        save_figure(fig, save_name)

    return fig, ax


def plot_cut_ratio_counts(
    ratio_result,
    solver_label,
    baseline_label,
    title=None,
    save_path=None,
    save_png=True,
    figsize=(10, 5),
):
    """
    Plot cut-ratio count distribution with optional float-instance overlay.
    """

    labels = ratio_result["labels"]
    counts = ratio_result["counts"]
    counts_float = ratio_result["counts_float"]
    total = ratio_result["total"]

    n_colors = 8
    colors = ["#ADD8E6"] * n_colors
    colors = colors[::-1] + ["#FFFACD"] + ["#B2E5B2"] * n_colors

    widths = [0.2 if lab == "{1.000}" else 0.8 for lab in labels]

    fig, ax = plt.subplots(figsize=figsize)

    ax.bar(labels, counts, color=colors, width=widths)
    ax.axvline(8, linestyle="--", color="gray", alpha=0.5)

    for i, count in enumerate(counts):
        if count > 0:
            ax.text(i, count + 0.5, str(count), ha="center", fontsize=12)

    if counts_float is not None:
        ax.bar(
            labels,
            counts_float,
            color="none",
            edgecolor="black",
            width=widths,
            hatch="///",
            label="Float cases",
        )

        for i, count in enumerate(counts_float):
            if count > 0:
                ax.text(i + 0.2, count + 0.5, str(count), ha="center", fontsize=9)

        ax.legend()

    ax.set_xlabel(
        rf"$\mathrm{{Cut}}_{{\mathrm{{{solver_label}}}}} / "
        rf"\mathrm{{Cut}}_{{\mathrm{{{baseline_label}}}}}$"
    )
    ax.set_ylabel("Instance count")

    if title is None:
        title = f"{solver_label} Cut Ratio Count vs {baseline_label} (Total={total})"

    ax.set_title(title)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90)

    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.tick_params(axis="x", which="both", bottom=False, top=False)
    ax.set_xlim(-0.4, len(labels) - 0.6)

    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, bbox_inches="tight")

        if save_png and str(save_path).endswith(".pdf"):
            png_path = str(save_path).replace(".pdf", ".png")
            fig.savefig(png_path, dpi=300, bbox_inches="tight")

    return fig, ax


def plot_optimality_percentage_per_solver(labels, values, count,file_name):
    
    fig, ax = plt.subplots()

    bars = ax.bar(
        labels,
        values
    )

    # Add percentage labels on top
    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{val:.1f}%",
            ha='center',
            va='bottom'
        )

    plt.ylabel("% Optimal (gap = 0)")
    plt.title(f"Optimality Rate per Solver n=({count})")
    plt.tight_layout()
    if file_name:
        save_figure(fig, file_name)
    plt.show()

    return fig, ax


def plot_solver_objective_gaps(
    df,
    objective_col="Objective Value",
    filename="solver_objective_gaps_cdf.pdf",
    figsize=(8, 5),
):
    """
    Plot empirical CDF of solver gaps relative to the best-known objective value.

    Gap is computed as:

        gap = Objective Value - solver value

    Therefore:
    - gap = 0 means the solver reached the best-known value
    - larger gap means worse performance
    """

    df = df.dropna(subset=cfg.SOLVERS + [objective_col])

    fig, ax = plt.subplots(figsize=figsize)

    for solver in cfg.SOLVERS:

        if solver not in df.columns:
            continue

        gaps = (df[objective_col] - df[solver])/df[objective_col]
        gaps = gaps.dropna().sort_values()

        if len(gaps) == 0:
            continue

        cdf = np.arange(1, len(gaps) + 1) / len(gaps)

        ax.plot(
            gaps,
            cdf,
            label=solver,
            color=cfg.SOLVER_COLORS.get(solver, "gray"),
            linewidth=2,
        )

    ax.axvline(0, linestyle="--", linewidth=1, color="black")

    ax.set_xlabel("Gap to Optimal Objective Value")
    ax.set_ylabel("Cumulative Fraction of Instances")
    ax.set_title("CDF of Solver Gap Distribution")
    ax.grid(alpha=0.3)
    ax.legend()

    fig.tight_layout()

    if filename:
        save_figure(fig, filename)

    plt.show()

    return fig, ax

def plot_edge_weight_distribution(
    df,
    nodes_col="nodes",
    unique_weights_col="unique weights",
    int_only_col="int_only",
    file_name=None
):

    fig, ax = plt.subplots(figsize=(10, 6))

    df_int = df[df[int_only_col] == True]
    df_float = df[df[int_only_col] == False]


    ax.scatter(
        df_int[nodes_col],
        df_int[unique_weights_col],
        marker=".",
        alpha=0.25,
        color="blue"
    )

    ax.scatter(
        df_float[nodes_col],
        df_float[unique_weights_col],
        marker=".",
        alpha=0.12,
        color="red"
    )

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Integer instances',
            markerfacecolor='blue', markersize=6),
        Line2D([0], [0], marker='o', color='w', label='Float instances',
            markerfacecolor='red', markersize=6)
    ]

    ax.legend(handles=legend_elements, loc="upper left", frameon=False)

    ax.set_yscale("log")
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto'))

    ax.axvline(4096, linestyle='--', color='gray', alpha=0.4)
    ax.axvline(8192, linestyle='--', color='gray', alpha=0.4)
    ax.axhline(46, linestyle='--', color='gray', alpha=0.4)
    ax.axhline(8190, linestyle='--', color='gray', alpha=0.4)

    ax.set_xlabel("Vertices")
    ax.set_ylabel("Unique Weights")

    ticks = [2048, 4096, 8192] + [20000 + x for x in range(0, 40000, 10000)]
    labels = [2048, 4096, 8192] + [str(20000 + x) for x in range(0, 40000, 10000)]

    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=90)

    yticks = [1, 46, 8190, 1.8152427e7]
    ylabels = ["1", "46", "8.19K", "18.15M"]

    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)

    axins = inset_axes(ax, width="70%", height="70%")

    axins.hist(
        df[nodes_col],
        bins=np.arange(min(df[nodes_col]), max(df[nodes_col]) + 500, 500),
        edgecolor='gray',
        alpha=0.2
    )

    axins.set_ylabel("Instance counts - log scale")
    axins.set_yscale('log')

    axins.axvline(4096, linestyle='--', color='gray', alpha=0.4)
    axins.axvline(8192, linestyle='--', color='gray', alpha=0.4)

    axins.set_xticks(ticks)
    axins.set_xticklabels(labels, rotation=90)

    axins2 = inset_axes(ax, width="35%", height="35%")

    axins2.hist(
        df[unique_weights_col],
        bins=30,
        edgecolor='gray',
        alpha=0.2
    )

    axins2.set_xlabel("Unique Weights")
    axins2.set_yscale("log")

    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2)

    if file_name:
        save_figure(fig, file_name)
    plt.show()


def plot_n_weights_90_histogram(
    df,
    col="n_weights_90",
    title="Distribution of Dominant Weight Diversity",
    file_name=None
):
    data = df[col].dropna()

    # Region counts
    n_concentrated = ((data >= 1) & (data <= 5)).sum()
    n_transitional = ((data > 5) & (data <= 50)).sum()
    n_heterogeneous = (data > 50).sum()

    # Use log-spaced bins because highly diverse has very large values
    bins = np.unique(
        np.concatenate([
            np.arange(1, 55, 1),
            np.logspace(np.log10(55), np.log10(data.max()), 25)
        ])
    )

    fig, ax = plt.subplots(figsize=(9, 4.8))

    # Background regions
    ax.axvspan(1, 5, alpha=0.12, label="Concentrated")
    ax.axvspan(5, 50, alpha=0.10, label="Transitional")
    ax.axvspan(50, data.max(), alpha=0.08, label="Heterogeneous")

    # Histogram
    ax.hist(data, bins=bins, edgecolor="black", linewidth=0.6)

    # Boundary lines
    ax.axvline(5, linestyle=":", linewidth=2)
    ax.axvline(50, linestyle=":", linewidth=2)

    # Log scale for long tail
    ax.set_xscale("log")

    # Labels
    ax.set_xlabel(r"$n_{\mathrm{weights},90}$")
    ax.set_ylabel("Number of instances")
    ax.set_title(title)

    # Smart count labels
    ymax = ax.get_ylim()[1]
       
    ax.text(
        5,
        ymax * 0.98,
        "5",
        ha="right",
        va="top",
        fontsize=10
    )

    ax.text(
        50,
        ymax * 0.98,
        "50",
        ha="right",
        va="top",
        fontsize=10
    )

    ax.text(
        2.2, ymax * 0.88,
        f"Concentrated\n1–5\nn = {n_concentrated}",
        ha="center", va="top", fontsize=10
    )

    ax.text(
        16, ymax * 0.88,
        f"Transitional\n6–50\nn = {n_transitional}",
        ha="center", va="top", fontsize=10
    )

    ax.text(
        300, ymax * 0.88,
        f"Heterogeneous\n>50\nn = {n_heterogeneous}",
        ha="center", va="top", fontsize=10
    )

    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()

    if file_name is not None:
        save_figure(fig, file_name)
        

    plt.show()
