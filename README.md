# Translating Bacterial Population Genomics into Infection Dynamics: A Mechanistic ODE Model of Sepsis

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Field](https://img.shields.io/badge/Field-Systems%20Biology%20%7C%20Microbial%20GWAS-brightgreen.svg)]()

> **Mechanistic Ordinary Differential Equation (ODE) models of Gram-negative sepsis (*Klebsiella pneumoniae*) integrating microbial genome-wide association study (`pyseer` mGWAS) effect sizes with host immune dynamics, endotoxin (LPS) release kinetics, and antibiotic PK/PD.**

---

## 📌 Repository Contents

This repository provides the core ODE simulation models, full mathematical derivations, and sample accession identifiers used in the study:

| File | Description |
| :--- | :--- |
| **[`pyseer_ode_model.py`](pyseer_ode_model.py)** | Core 9-compartment ODE sepsis model simulating bacterial load ($B$), neutrophils ($N$), macrophages ($M$), cytokines ($\text{IL-6}, \text{TNF-}\alpha, \text{IL-10}$), tissue damage ($D$), and antibiotic PK/PD compartments ($A_{\text{depot}}, A_{\text{plasma}}$). |
| **[`pyseer_ode_lps_extended.py`](pyseer_ode_lps_extended.py)** | Extended 10-compartment model incorporating free endotoxin (LPS) release kinetics, bacteriolysis bursts, inoculum dose-response, and time-to-treatment golden window analysis. |
| **[`pyseer_ode_mathematical_explanation.md`](pyseer_ode_mathematical_explanation.md)** | Complete mathematical formulation, parameter tables, rate equations, and analytical derivations. |
| **[`srr_ids.txt`](srr_ids.txt)** | List of 100 NCBI SRA Run accessions (`SRR...`) for the clinical *Klebsiella pneumoniae* sepsis blood isolates. |
| **[`sample_accessions_manifest.csv`](sample_accessions_manifest.csv)** | Full metadata manifest of all 200 isolates (100 sepsis blood isolates with SRA SRR IDs and BioProjects, and 100 non-sepsis control assemblies from NCBI RefSeq/GenBank and BV-BRC/PATRIC). |

---

## 🔬 Scientific Overview

Microbial genome-wide association studies (mGWAS) using linear mixed models (`pyseer`) identify statistical associations between bacterial accessory genes and invasive bacteremia. We translate these statistical effect sizes ($\beta$) into mechanistic biological rate multipliers:

$$\phi = \exp(\beta)$$

- **$\phi_{\text{stress}} = \exp(0.434) = 1.543$** (*clpK/clpB* operon): Chaperone-mediated resistance to proteotoxic and thermal stress, reducing clearance rates.
- **$\phi_{\text{ROS}} = \exp(0.394) = 1.483$** (*egtB* ergothioneine pathway): Scavenges reactive oxygen species, blunting neutrophil oxidative burst killing.
- **$\phi_{\beta\text{-lactam}} = \exp(0.350) = 1.419$** (*bla_1* / IS6 elements): Attenuates antibiotic-mediated bacteriolysis.

---

## 🧬 Study Dataset & Accessions

The genomic association study utilized 200 *Klebsiella pneumoniae* isolates:
- **100 Sepsis Blood Isolates:** Downloaded from the NCBI Sequence Read Archive (SRA) across BioProjects `PRJNA1199555`, `PRJNA787062`, `PRJNA945449`, `PRJNA790720`, `PRJNA1259250`, and `PRJNA853564`. All Run accessions are listed in [`srr_ids.txt`](srr_ids.txt).
- **100 Non-Sepsis Control Isolates:** Downloaded from NCBI RefSeq/GenBank and BV-BRC (PATRIC) representing non-invasive colonization and respiratory/urinary isolates.

All accession numbers and metadata are cataloged in [`sample_accessions_manifest.csv`](sample_accessions_manifest.csv).

---

## 🚀 Running the Models

### Prerequisites
The models require Python 3.9+ with `numpy`, `scipy`, and `matplotlib`:
```bash
pip install numpy scipy matplotlib
```

### Core 9-Compartment Simulation
```bash
python3 pyseer_ode_model.py
```

### Extended 10-Compartment LPS & Treatment Delay Simulation
```bash
python3 pyseer_ode_lps_extended.py
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
