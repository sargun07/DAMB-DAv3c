# DA Benchmark Extension with DAv3c and Structural Graph Analysis

## Overview
This repository contains the implementation, datasets, analysis scripts, and experimental results for our Max-Cut benchmark extension project. 

The project extends the benchmark study introduced in:
* **[A comprehensive benchmark of an Ising machine on the Max-Cut problem](https://arxiv.org/pdf/2507.22117)**

The original benchmark compared Digital Annealer solvers (DAv2 and DAv3) against state-of-the-art MQLib heuristics and showed highly competitive performance of the DA framework on large Max-Cut benchmark instances. The MQLib heuristics used in the original benchmark are based on:
* **[MQLib: A collection of Max-Cut and QUBO heuristics.](https://github.com/MQLib/MQLib)**

### Research Objective
However, it remains unclear whether the strong performance observed in DAv2 and DAv3 primarily originates from:
1. The underlying optimization algorithm, or
2. The specialized Digital Annealer hardware acceleration.

To investigate this, this project extends the benchmark by incorporating **DAv3c**, the CPU-based software implementation of DAv3. DAv3c includes mechanisms such as:
* Parallel tempering
* Tabu Search

This allows the optimization methodology to be analyzed separately from the specialized hardware platform.

In addition to extending the benchmark with DAv3c, this project also investigates how structural graph properties influence solver behavior. The original benchmark primarily analyzed solver performance across graph size and density categories. In this work, we additionally explore how other structural properties affect solver performance across different graph families.

> 📄 The complete project report and analysis are available in the [reports/](reports/) directory.

---

## Repository Contents

### 1. DAv2, DAv3, and MQLib Benchmark Data
The original benchmark data comparing DAv2, DAv3, and MQLib heuristics is included in this repository and obtained from:
* **[DA Maxcut Benchmark (DAMB)](https://github.com/SalwaShaglel/DAMB)**

The benchmark contains instance-specific objective values and runtime limits for all evaluated solvers.

### 2. DAv3c Experimental Results
The DAv3c experimental results generated in this project are stored in: [data/raw/DAv3c](Dav3c/) directory

The experiments follow the same benchmark setup and instance-specific runtime limits used in the original benchmark study.

### 3. Structural Graph Metrics
This repository also contains precomputed structural graph metrics for all benchmark instances. The processed structural metrics dataset is stored in: [data/processed/graph_metrics.csv](GRAPH PROPERTIES)

The computed graph properties include:
* Negative weight fraction
* Triangle count
* Transitivity
* Average clustering coefficient
* Cyclomatic number
* Bridge count
* Bridge fraction
* Unique edge-weight statistics

### 4. Baseline Dataset
The repository contains a consolidated baseline dataset containing all evaluated instances and solver outputs. The baseline dataset is available in:
* `data/processed/baseline_dataset.csv`

The baseline dataset includes:
* Objective values from all solvers
* Graph metadata
* Runtime information
* Structural graph properties

For each instance, the dataset additionally records:
* The maximum objective value obtained across all evaluated solvers
* The solver(s) that achieved that value

---

## Analyses Performed

1. **DAv3c Solver Benchmark Extension**  
   We compare DAv3c against DAv2, DAv3, and selected MQLib heuristics across the benchmark dataset[cite: 1].
2. **Structural Graph Analysis**  
   We analyze how graph structures influenced by odd-cycle behavior affect solver performance[cite: 1]. The structural analyses include:
   * Bipartite graphs[cite: 1]
   * Triangle-free graphs[cite: 1]
   * Non-bipartite triangle-rich graphs[cite: 1]
3. **Edge-Weight Representation Analysis**  
   We analyze solver behavior separately for:
   * Integer-weighted instances[cite: 1]
   * Floating-point-weighted instances[cite: 1]
4. **Unique Edge-Weight Dominance Analysis**  
   For integer-weighted instances, we further analyze how repeated and dominant edge-weight distributions influence solver performance[cite: 1].
5. **Bipartite Optimality Analysis**  
   We analyze solver optimality behavior on bipartite non-negative benchmark instances, where the Max-Cut optimum is theoretically attainable[cite: 1].

---

## Repository Structure

```text
.
├── data/
│   ├── raw/
│   │   ├── dav3c/                 # DAv3c experimental outputs
│   │   ├── benchmark/             # Original benchmark datasets
│   ├──  processed/
│   │    ├── baseline_dataset.csv   # Master benchmark data with maximum objective value for each instances per for all solvers with graph properties
│   │    ├── baseline_enriched.csv  # Master benchmark data without graph properties
│   │    ├── final_dataset.parquet  # Consolidated master dataset with maxcut values of all the solvers & for all runs
│   │    ├── graph_metrics.csv      # Computed topological structural metrics
│   │    └── graph_uweight_dominance.csv  # Computed repeating weight dominance over the edges
│   ├──  metadata/
│   │    └── baseline.csv            # Dataset containing time limit for each instance
├── results/
│   └── figures/               # Generated charts and visualizations
├── reports/
│   └── report.pdf             # Complete project report and analysis
├── notebooks/                 # Jupyter notebooks for EDA and analyses
├── src/       
└── requirement.txt             
```
## Reproducibility

### Experimental Environment
The DAv3c experiments were executed on the following system configuration:

* **CPU:** AMD EPYC 9275F 24-Core Processor
* **Logical CPUs:** 48
* **RAM:** 754 GiB
* **Operating System:** Red Hat Enterprise Linux 9.4
* **Python Version:** 3.11.7

> **Note:** DAv3c was evaluated as the CPU-based software implementation of the Digital Annealer framework.

---

### Running the Repository

#### 1. Clone the Repository
```bash
git clone https://github.com/sargun07/DAMB-DAv3c.git
cd DAMB-DAv3c

#### 2. Create an environment
```bash
python -m venv venv
source venv/bin/activate

#### 3. Install dependencies
```bash
pip install -r requirements.txt

#### 4. Repository Data
The repository already comes pre-packaged with the necessary data files:
*Original benchmark datasets
*DAv3c experimental outputs
*Processed datasets
*Structural graph metrics


The main consolidated datasets are available at:
*data/processed/baseline_dataset.csv
*data/processed/graph_metrics.csv

#### 5. Run the Analysis
Analysis Notebooks: Located in the notebooks/ directory. These can be executed directly using Jupyter Notebook or JupyterLab.
Core Utilities: Core analysis utilities and plotting functions are structured inside the src/ directory.
