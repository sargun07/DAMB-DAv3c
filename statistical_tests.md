# Statistical Significance Tests — Max-Cut Benchmark

This document reports the paired Wilcoxon signed-rank tests from [`06_pairwise_solver_comparison.ipynb`](notebooks/06_pairwise_solver_comparison.ipynb). Results correspond to the notebook analysis using an absolute numerical tie tolerance of `1e-9`.

## Method and interpretation

The tests compare paired objective values on the **same Max-Cut instances**. For each instance, the difference is defined as the **first solver minus the second solver** named in the comparison. Differences with absolute magnitude **at most `1e-9`** are treated as numerical ties and excluded from the two-sided Wilcoxon signed-rank test (`zero_method="wilcox"`).

The null hypothesis concerns symmetry of the paired-difference distribution about zero. Statistical significance is assessed at **α = 0.05** using **Holm-adjusted p-values**. Corrections are performed separately across the seven size–density tests for DAv3c versus MQLib, the seven for DAv3c versus DAv3, and the six for DAv3c versus DAv2; the six solver-by-weight-type tests form a **single additional correction family**. These are distinct families, not one correction over every test in this document.

The tables show `N` (all paired instances), `n` (non-tied pairs used by the test), the number of numerical ties, unadjusted and Holm-adjusted p-values, and the **signed matched-pairs rank-biserial correlation** `r_rb`. A positive `r_rb` favors the **first** solver; a negative value favors the **second**. Non-significance is not proof of equivalence. Differences between subgroup effect sizes are descriptive and are not themselves interaction tests. The comparisons do not identify causal effects of hardware, algorithms, or edge-weight representation.

## 1. Across size–density categories

### 1.1 DAv3c versus category-specific MQLib heuristic

| Category | N | n | Ties | Raw p-value | Holm-adjusted p-value | r_rb | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| Medium–sparse | 279 | 252 | 27 | 1.279055e-02 | 3.586517e-02 | +0.180908 | Significant; DAv3c favored |
| Medium–balanced | 78 | 63 | 15 | 9.399703e-01 | 9.399703e-01 | +0.010913 | Not significant |
| Medium–dense | 50 | 38 | 12 | 1.195506e-02 | 3.586517e-02 | -0.462888 | Significant; MQLib favored |
| Large–sparse | 171 | 164 | 7 | 1.666406e-09 | 1.166484e-08 | +0.542646 | Significant; DAv3c favored |
| Large–balanced | 119 | 103 | 16 | 4.449840e-05 | 2.224920e-04 | -0.463406 | Significant; MQLib favored |
| Large–dense | 41 | 33 | 8 | 1.099177e-04 | 4.396709e-04 | -0.729055 | Significant; MQLib favored |
| Xlarge–sparse | 81 | 81 | 0 | 1.957937e-06 | 1.174762e-05 | -0.608552 | Significant; MQLib favored |

**Summary:** Six of seven categories show significant signed-rank differences after Holm correction; Medium–balanced is the exception. The common category-specific MQLib baseline is not necessarily the same heuristic across categories.

### 1.2 DAv3c versus DAv3

| Category | N | n | Ties | Raw p-value | Holm-adjusted p-value | r_rb | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| Medium–sparse | 279 | 231 | 48 | 8.5845e-11 | 5.1507e-10 | -0.493 | Significant; DAv3 favored |
| Medium–balanced | 78 | 61 | 17 | 8.6590e-05 | 1.7318e-04 | -0.578 | Significant; DAv3 favored |
| Medium–dense | 50 | 38 | 12 | 4.6266e-07 | 2.3133e-06 | -0.849 | Significant; DAv3 favored |
| Large–sparse | 171 | 159 | 12 | 5.7383e-04 | 5.7383e-04 | -0.315 | Significant; DAv3 favored |
| Large–balanced | 119 | 96 | 23 | 5.0163e-11 | 3.5114e-10 | -0.772 | Significant; DAv3 favored |
| Large–dense | 41 | 31 | 10 | 2.2119e-06 | 8.8476e-06 | -0.875 | Significant; DAv3 favored |
| Xlarge–sparse | 81 | 81 | 0 | 4.9881e-05 | 1.4964e-04 | +0.519 | Significant; DAv3c favored |

**Summary:** All seven categories show significant differences. The signed-rank direction favors DAv3 in six categories and DAv3c in Xlarge–sparse.

### 1.3 DAv3c versus DAv2

DAv2 results are unavailable for Xlarge instances. The comparison therefore covers **738 common Medium and Large instances**.

| Category | N | n | Ties | Raw p-value | Holm-adjusted p-value | r_rb | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| Medium–sparse | 279 | 239 | 40 | 1.4428e-11 | 8.6565e-11 | -0.504 | Significant; DAv2 favored |
| Medium–balanced | 78 | 68 | 10 | 4.5707e-02 | 1.3712e-01 | -0.279 | Not significant |
| Medium–dense | 50 | 44 | 6 | 6.4758e-05 | 3.2379e-04 | -0.661 | Significant; DAv2 favored |
| Large–sparse | 171 | 161 | 10 | 4.5209e-01 | 4.5209e-01 | +0.068 | Not significant |
| Large–balanced | 119 | 113 | 6 | 8.4852e-02 | 1.6970e-01 | -0.187 | Not significant |
| Large–dense | 41 | 37 | 4 | 6.8601e-03 | 2.7441e-02 | -0.502 | Significant; DAv2 favored |

**Summary:** Three of six categories are significant after Holm correction: Medium–sparse, Medium–dense and Large–dense, all favoring DAv2. The raw Medium–balanced p-value is below 0.05 but is **not significant after Holm correction**.

## 2. Across edge-weight representations

The same **738 instances** are used for each DA solver: **349 integer-weighted** and **389 non-integer-weighted** instances. Each DA solver is compared with the corresponding category-specific MQLib heuristic. Holm correction is applied **jointly across all six tests** in this section.

| Solver | Weight type | N | n | Ties | Raw p-value | Holm-adjusted p-value | r_rb | Result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| DAv2 | Integer | 349 | 290 | 59 | 4.271613e-20 | 2.135806e-19 | +0.621993 | Significant; DAv2 favored |
| DAv2 | Non-integer | 389 | 360 | 29 | 1.204062e-08 | 3.612185e-08 | +0.346599 | Significant; DAv2 favored |
| DAv3 | Integer | 349 | 265 | 84 | 8.218066e-25 | 4.930839e-24 | +0.728869 | Significant; DAv3 favored |
| DAv3 | Non-integer | 389 | 331 | 58 | 2.489975e-13 | 9.959901e-13 | +0.464201 | Significant; DAv3 favored |
| DAv3c | Integer | 349 | 272 | 77 | 9.478094e-01 | 9.478094e-01 | +0.004579 | Not significant |
| DAv3c | Non-integer | 389 | 381 | 8 | 6.829402e-02 | 1.365880e-01 | +0.107776 | Not significant |

**Summary:** Both DAv2 and DAv3 show significant signed-rank differences favoring the DA solver against the selected heuristic on both weight types. No statistically significant difference is detected for DAv3c on either weight type. The larger positive `r_rb` values for DAv2 and DAv3 on integer-weighted instances are descriptive; these tests do not determine whether the effect differs significantly by weight type.

## Reproducibility notes

- All reported test results use an absolute paired-objective difference threshold `abs(diff) <= 1e-9` for numerical ties.
- Numerical ties are excluded from the Wilcoxon test. Therefore `n = N - Ties` in each table.
- Two-sided Wilcoxon tests are run using SciPy, with Holm adjustment using `statsmodels.stats.multitest.multipletests(method="holm")`.
- The rank-biserial effect is calculated from positive and negative signed-rank sums after excluding numerical ties: `r_rb = (W_plus - W_minus) / (W_plus + W_minus)`.
