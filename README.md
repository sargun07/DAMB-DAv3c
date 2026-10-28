# DA Benchmark Extension with DAv3c and Structural Graph Analysis

## Overview

This repository contains code, analysis notebooks, and experimental results for an extension of a Max-Cut benchmark. It investigates the CPU-based Digital Annealer configuration **DAv3c** alongside previously reported results for the hardware-based **DAv2** and **DAv3** systems and selected **MQLib** heuristics.

This project builds on:

- [*A comprehensive benchmark of an Ising machine on the Max-Cut problem*](https://arxiv.org/pdf/2507.22117), which benchmarks Digital Annealer solvers and MQLib heuristics.
- [MQLib](https://github.com/MQLib/MQLib), the original library of Max-Cut and QUBO instances and heuristic implementations.

### Research objective

DAv3 and DAv3c share a broad optimization framework combining parallel tempering and tabu search, but differ in their execution platforms and potentially in implementation details. We compare their observed solution quality with DAv2 and selected MQLib heuristics. **These comparisons do not isolate the contribution of specialized hardware from algorithmic and implementation differences.**

We also study performance differences associated with graph structure and edge-weight characteristics beyond the size and density categories considered in the original benchmark.

The project report and related material are located in [`reports/`](reports/) where available.

## Data availability and required setup

**Large input data are not included in this GitHub repository.** In particular:

1. **MQLib graph instances** must be obtained from the [original MQLib source](https://github.com/MQLib/MQLib) and placed in `data/raw/mqlib_instances/`.
2. **`data/processed/metrics.csv`** is not included because it is large and time-consuming to generate. The metric-generation code is provided in this project's notebooks; run that code to reproduce the file before executing notebooks that depend on it.

Other benchmark results and metadata are distinct from the MQLib graph files. See the relevant notebook input paths and the original [DA Maxcut Benchmark (DAMB)](https://github.com/SalwaShaglel/DAMB) repository for the provenance of reused hardware and heuristic results. **This README does not currently claim a downloadable full-data ZIP or a published Zenodo DOI.**

### 1. Clone this repository

```bash
git clone https://github.com/sargun07/DAMB-DAv3c.git
cd DAMB-DAv3c
```

### 2. Download the MQLib instances

The original MQLib project supplies graph-download scripts and instructions. Start with the [MQLib repository](https://github.com/MQLib/MQLib) and its [download documentation](https://github.com/MQLib/MQLib/tree/master/scripts).

For example, the original repository documents a graph-download script (check its instructions and Python dependencies before running):

```bash
git clone https://github.com/MQLib/MQLib.git
cd MQLib
python scripts/downloadAllGraphs.py instances
```

After downloading and, if necessary, extracting the graphs, **copy the actual instance files** into this project's directory:

```text
DAMB-DAv3c/
└── data/
    └── raw/
        └── mqlib_instances/
            ├── <MQLib instance file 1>
            ├── <MQLib instance file 2>
            └── ...
```

The directory name must be exactly **`mqlib_instances`**, located directly under **`data/raw/`**. Do not place an additional `MQLib/` or `instances/` directory between `mqlib_instances/` and the graph files unless an individual notebook explicitly expects that structure.

You can create the destination directory with:

```bash
mkdir -p data/raw/mqlib_instances
```

The original Digital Annealer benchmark reports using MQLib commit `686a4fc`. When reproducibility requires matching the historical graph collection, use the instance identifiers in the analysis data to verify that the required graphs were downloaded.

### 3. Generate `data/processed/metrics.csv`

**`metrics.csv` is intentionally omitted from the repository.** It contains graph metrics generated from the MQLib instances by the project's notebook code. Its generation can take considerable time, depending on machine specifications and the selected graph set.

1. Ensure the graph files are available in `data/raw/mqlib_instances/`.
2. Create `data/processed/` if it does not already exist.
3. Execute the **05_a_edge_weight_analysis.ipynb** supplied in `notebooks/`.
4. Confirm that its output is saved as **`data/processed/metrics.csv`** before running analyses that load that file.

### Expected directory layout

### Repository Structure

```text
DAMB-DAv3c/
├── README.md
├── requirements.txt
├── statistical_tests.md          # Detailed statistical test results
│
├── data/                         # Benchmark datasets and experimental results
│   ├── metadata/                 # Benchmark metadata
│   ├── processed/                # Processed datasets used in the analyses
│   └── raw/
│       ├── benchmark/            # Previously reported benchmark results
│       ├── dav3c_runs/           # DAv3c experimental outputs
│       └── dav3c_logs/           # DAv3c execution logs
│
├── notebooks/                    # Data preparation and analysis notebooks
│   ├── 00_prepare_benchmark_dataset.ipynb
│   ├── 01_a_build_dataset.ipynb
│   ├── 01_b_runtime_audit.ipynb
│   ├── 02_compute_graph_properties.ipynb
│   ├── 03_build_baseline_dataset.ipynb
│   ├── 04_dav3c_cv_runtime_analysis.ipynb
│   ├── 05_a_edge_weight_analysis.ipynb
│   ├── 05_b_edge_weight_analysis.ipynb
│   ├── 05_c_edge_weight_analysis.ipynb
│   ├── 06_pairwise_solver_comparison.ipynb
│   ├── 07_structural_graph_analysis.ipynb
│   └── 08_bipartite_optimality_analysis.ipynb
│
├── src/maxcut/                   # Shared Python modules
│   ├── config.py
│   ├── utils.py
│   └── plotting.py
│
├── results/figures/              # Generated figures from the analyses
│
├── report/                       # Research report

## Repository contents and analyses

- **Benchmark comparison:** DAv3c results versus DAv2, DAv3, and selected MQLib heuristics across size--density categories.
- **Structural graph analysis:** bipartite, non-bipartite with triangles, and non-bipartite triangle-free instances.
- **Edge-weight representation:** integer versus non-integer weights.
- **Edge-weight concentration:** repeated and diverse integer edge-weight values.
- **Known-optimum analysis:** recovery of analytically known Max-Cut optima for bipartite graphs with non-negative edge weights.

Where the relevant processed datasets have been generated, they combine instance identifiers, graph properties, solver objectives, and/or runtime information. The authoritative inputs and outputs for each analysis are the paths specified in its notebook.

## Reproducibility

### DAv3c experimental environment

The DAv3c experiments used:

- **CPU:** AMD EPYC 9275F 24-Core Processor
- **Logical CPUs:** 48
- **RAM:** 754 GiB
- **Operating system:** Red Hat Enterprise Linux 9.4
- **Python:** 3.11.7

### Run the analyses

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies using the dependency file **actually present in the repository** (for example, `requirements.txt` or `requirement.txt`):

```bash
pip install -r requirements.txt
```

Run the notebooks in `notebooks/` in dependency order: download the source graphs, generate the required metrics and other processed data, and then run the analytical notebooks. A notebook requiring `data/processed/metrics.csv` cannot run successfully until that file has been generated or extracted from a separately supplied archive.

## Data provenance and citation

**MQLib instances and heuristic implementations:**

Dunning, I., Gupta, S., and Silberholz, J. (2018). *What Works Best When? A Systematic Evaluation of Heuristics for Max-Cut and QUBO.* INFORMS Journal on Computing, 30(3), 608--624. [MQLib repository](https://github.com/MQLib/MQLib).

**Previously reported Digital Annealer and heuristic benchmark results:**

[*A comprehensive benchmark of an Ising machine on the Max-Cut problem*](https://arxiv.org/pdf/2507.22117). [DAMB repository](https://github.com/SalwaShaglel/DAMB).

