# Statistical Significance Tests — Max-Cut Benchmark

This document consolidates the reported paired Wilcoxon signed-rank test results. The analyses and executable test implementations remain in their original Jupyter notebooks.

## Method and interpretation

The tests compare paired objective values for the **same Max-Cut instances**. The null hypothesis is that the distribution of paired differences is symmetric about zero (often summarized as a zero median paired difference under a symmetry assumption). Statistical significance is assessed at **α = 0.05** using the reported *p*-values; effect size is reported as **r**. An insignificant result means insufficient evidence of a systematic paired difference, **not** equivalence. The *p*-values and the unsigned effect-size magnitudes below do **not**, by themselves, establish which solver performs better: direction must be read alongside the paired differences or win–tie–loss results. These tests do not directly establish a causal effect of edge-weight representation.

**Multiple comparisons:** These are the supplied unadjusted significance labels; whether *p*-value correction was applied must be verified in the source notebooks. Some findings close to α = 0.05 may change if a correction is applied.

## 1. Across size–density categories

**Original analysis notebook:** [06_pairwise_solver_comparison.ipynb](https://github.com/sargun07/DAMB-DAv3c/blob/main/notebooks/06_pairwise_solver_comparison.ipynb)

### 1.1 DAv3c versus category-specific MQLib heuristic

| Category | n | p-value | r | Reported result |
|---|---:|---:|---:|---|
| Medium–sparse | 255 | 2.81 × 10⁻² | 0.138 | Significant |
| Medium–balanced | 65 | 9.09 × 10⁻¹ | 0.014 | Not significant |
| Medium–dense | 38 | 1.20 × 10⁻² | 0.403 | Significant |
| Large–sparse | 165 | 1.86 × 10⁻⁹ | 0.468 | Significant |
| Large–balanced | 103 | 4.45 × 10⁻⁵ | 0.402 | Significant |
| Large–dense | 33 | 1.10 × 10⁻⁴ | 0.636 | Significant |
| Xlarge–sparse | 81 | 1.96 × 10⁻⁶ | 0.529 | Significant |

**Takeaway:** Significant paired differences in six of seven categories; medium–balanced is the exception.

### 1.2 DAv3c versus DAv3

| Category | n | p-value | r | Reported result |
|---|---:|---:|---:|---|
| Medium–sparse | 236 | 7.40 × 10⁻¹⁴ | 0.487 | Significant |
| Medium–balanced | 64 | 5.21 × 10⁻⁵ | 0.506 | Significant |
| Medium–dense | 38 | 4.63 × 10⁻⁷ | 0.740 | Significant |
| Large–sparse | 160 | 2.80 × 10⁻⁴ | 0.287 | Significant |
| Large–balanced | 96 | 5.02 × 10⁻¹¹ | 0.671 | Significant |
| Large–dense | 31 | 2.21 × 10⁻⁶ | 0.764 | Significant |
| Xlarge–sparse | 81 | 4.99 × 10⁻⁵ | 0.451 | Significant |

**Takeaway:** Significant paired differences in all seven categories.

### 1.3 DAv3c versus DAv2

| Category | n | p-value | r | Reported result |
|---|---:|---:|---:|---|
| Medium–sparse | 244 | 6.42 × 10⁻¹² | 0.440 | Significant |
| Medium–balanced | 69 | 4.75 × 10⁻² | 0.239 | Significant |
| Medium–dense | 44 | 6.48 × 10⁻⁵ | 0.575 | Significant |
| Large–sparse | 162 | 4.75 × 10⁻¹ | 0.056 | Not significant |
| Large–balanced | 113 | 8.49 × 10⁻² | 0.162 | Not significant |
| Large–dense | 37 | 6.86 × 10⁻³ | 0.438 | Significant |

**Takeaway:** Significant paired differences in four of six categories; large–sparse and large–balanced are not significant. DAv2 was not evaluated on Xlarge instances.

## 2. Across edge-weight representations

The following tests compare each DA variant with its **category-specific MQLib heuristic**, separately for integer- and non-integer-weighted instances.

**Original analysis notebook:** [06_pairwise_solver_comparison.ipynb](https://github.com/sargun07/DAMB-DAv3c/blob/main/notebooks/06_pairwise_solver_comparison.ipynb) *(confirm this is the notebook containing the edge-weight tests; otherwise replace with the correct link).*

| Solver | Weight type | Reported test n | p-value | r | Reported result |
|---|---|---:|---:|---:|---|
| DAv2 | Integer | 289 | 5.48 × 10⁻²⁰ | 0.538 | Significant |
| DAv2 | Non-integer | 360 | 1.36 × 10⁻⁸ | 0.299 | Significant |
| DAv3 | Integer | 298 | 1.18 × 10⁻²⁰ | 0.540 | Significant |
| DAv3 | Non-integer | 378 | 2.98 × 10⁻⁵ | 0.215 | Significant |
| DAv3c | Integer | 305 | 9.53 × 10⁻¹ | 0.003 | Not significant |
| DAv3c | Non-integer | 435 | 6.43 × 10⁻¹ | 0.022 | Not significant |

**Takeaway:** DAv2 and DAv3 show significant paired differences from their heuristic baselines in both weight subsets; DAv3c does not. This supports the observed performance differences of the hardware-based variants **within** each subset, but does not test whether integer and non-integer weights cause different solver behavior.

## Checks before publication

1. **Sample-size inconsistency:** The common medium/large subset has been described as 349 integer-weighted and 389 non-integer-weighted instances, yet the DAv3c non-integer test reports **n = 435**. Verify whether this test uses a different population, whether *n* denotes something else, or whether the value is a transcription error. Do not change it without checking the originating notebook.
2. **Meaning of n:** Some Wilcoxon counts differ between comparisons, possibly because zero-difference pairs are excluded or because comparison subsets differ. Confirm how the notebook computes the reported *n* and document this consistently.
3. **Multiple-testing corrections and zero handling:** Confirm the Wilcoxon alternative, zero-handling option, meaning/formula of effect size *r*, and whether reported *p*-values are adjusted.
4. **Notebook link:** Confirm the exact notebook containing the edge-weight tests and update its reference above if different.
