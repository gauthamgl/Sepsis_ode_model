# Pyseer + ODE Sepsis Model — Complete Mathematical Explanation

## Table of Contents

1. [Overview](#overview)
2. [The IL-10 Suppression Multiplier](#1-the-il-10-suppression-multiplier-s_il10)
3. [Bacterial Dynamics](#2-bacterial-dynamics)
4. [Innate Immune Cell Dynamics](#3-innate-immune-cell-dynamics)
5. [Cytokine Network](#4-cytokine-network)
6. [Tissue Damage Index (D) — DAMP Dynamics](#5-tissue-damage-index-d--damp-dynamics)
7. [One-Compartment Antibiotic PK/PD (with Absorption Depot)](#6-one-compartment-antibiotic-pharmacokinetics--pharmacodynamics)
8. [Pyseer Gene Effect Size Integration](#7-pyseer-gene-effect-size-integration)
9. [Complete Worked Example](#8-complete-worked-example)
10. [Summary of All Variables and Parameters](#9-summary-of-all-variables--parameters)

---

## Overview

This document describes a **nine-compartment Ordinary Differential Equation (ODE) model** of gram-negative sepsis. The model tracks the following state variables over time:

| Variable | Meaning |
|----------|---------|
| **B** | Normalised bacterial load |
| **N** | Activated neutrophil concentration |
| **M** | Activated macrophage concentration |
| **IL-6** | Interleukin-6 (pro-inflammatory cytokine) |
| **TNF-α** | Tumour necrosis factor alpha (pro-inflammatory cytokine) |
| **IL-10** | Interleukin-10 (anti-inflammatory cytokine) |
| **D** | Tissue damage index (DAMP signalling burden) |
| **A_depot** | Antibiotic depot compartment |
| **A_plasma** | Antibiotic plasma compartment |

The key innovation is that **statistical effect sizes (β)** from pyseer mGWAS (microbial genome-wide association study) are converted into **mechanistic rate multipliers (φ)** via the exponential transformation `φ = exp(β)`, directly linking population genomics to infection dynamics.

---

## 1. The IL-10 Suppression Multiplier (S_IL10)

### Formula

```
S_IL10 = 1 / (1 + κ_IL10 × [IL-10])
```

### What it does

IL-10 is an **anti-inflammatory cytokine**. This multiplier ranges from 0 to 1 and acts as a universal "brake" on immune activity:

- When **IL-10 = 0** → S_IL10 = 1 → no suppression (full immune activity)
- When **IL-10 is very high** → S_IL10 → 0 → almost complete immune suppression

### Why this form?

This is a **Hill-type inhibition function** with Hill coefficient n = 1. It produces a smooth, saturable suppression effect. The parameter κ_IL10 controls how sensitive the system is to IL-10.

### Example

If κ_IL10 = 5.0 and IL-10 = 0.2:

```
S_IL10 = 1 / (1 + 5.0 × 0.2) = 1 / (1 + 1.0) = 1/2 = 0.5
```

> This means immune activities (neutrophil/macrophage killing, cytokine production) operate at **50% efficiency**.

---

## 2. Bacterial Dynamics

### Formula

```
dB/dt = k_b × B × (1 - B)                                        [Logistic growth]
      - d_b × B                                                   [Natural death]
      - k_surv × B                                                [Baseline immune surveillance]
      - (k_NB_ox/φ_ROS + k_NB_pep) × (N - N₀) × B × S_IL10      [Neutrophil killing]
      - (k_MB/φ_stress) × (M - M₀) × B × S_IL10                  [Macrophage killing]
      - E_abx × B                                                 [Antibiotic killing]
```

### Term-by-term breakdown

| Term | Formula | Biological Meaning |
|------|---------|-------------------|
| **Logistic growth** | k_b × B × (1 − B) | Bacteria multiply but saturate at a maximum carrying capacity (B = 1). Growth rate is fastest at intermediate populations. |
| **Natural death** | d_b × B | Spontaneous bacterial death/clearance. |
| **Baseline surveillance** | k_surv × B | Constant low-level immune clearance even before adaptive response kicks in. |
| **Neutrophil killing (oxidative)** | (k_NB_ox / φ_ROS) × (N − N₀) × B × S_IL10 | ROS-mediated killing by activated neutrophils (above resting level N₀). Reduced by egtB virulence (φ_ROS > 1 divides the rate). |
| **Neutrophil killing (peptide)** | k_NB_pep × (N − N₀) × B × S_IL10 | Non-oxidative antimicrobial peptide killing. Not affected by egtB. |
| **Macrophage killing** | (k_MB / φ_stress) × (M − M₀) × B × S_IL10 | Phagocytic killing by activated macrophages. Reduced by clpK/clpB virulence (φ_stress > 1). |
| **Antibiotic killing** | E_abx × B | Pharmacodynamic drug effect (see section 6). |

### Why (N − N₀) and (M − M₀)?

N₀ and M₀ are the **resting baseline** populations. Only the fraction **above** baseline represents actively fighting immune cells. This ensures the model doesn't overestimate killing when the immune system is at rest.

### Example

Suppose at time t:
- B = 0.5, N = 0.3, N₀ = 0.05, M = 0.2, M₀ = 0.05
- k_b = 0.6, d_b = 0.1, k_surv = 0.05
- k_NB_ox = 0.8, k_NB_pep = 0.3, k_MB = 0.6
- φ_ROS = 1.48 (egtB present), φ_stress = 1.54 (clpK present)
- S_IL10 = 0.5, E_abx = 0

```
Growth       = 0.6 × 0.5 × (1 - 0.5) = 0.6 × 0.5 × 0.5 = 0.15
Natural death = 0.1 × 0.5 = 0.05
Surveillance  = 0.05 × 0.5 = 0.025
Neutrophil killing = (0.8/1.48 + 0.3) × (0.3 - 0.05) × 0.5 × 0.5
                   = (0.537 + 0.3) × 0.25 × 0.5 × 0.5
                   = 0.837 × 0.0625 = 0.0523
Macrophage killing = (0.6/1.54) × (0.2 - 0.05) × 0.5 × 0.5
                   = 0.390 × 0.15 × 0.5 × 0.5 = 0.0146

dB/dt = 0.15 - 0.05 - 0.025 - 0.0523 - 0.0146 - 0
      = +0.0081 (bacteria are slowly increasing)
```

> **Interpretation**: With virulence genes reducing immune killing (φ_ROS = 1.48, φ_stress = 1.54) and IL-10 suppression at 50%, bacteria are barely being contained — dB/dt is slightly positive.

---

## 3. Innate Immune Cell Dynamics

### Neutrophils

```
dN/dt = (k_N_rec × B + k_N_cyt × (IL-6 + TNF-α)) × S_IL10      [Recruitment & activation]
      - d_N × (N - N₀)                                            [Decay to baseline]
```

### Macrophages

```
dM/dt = (k_M_bact × B + k_M_cyt × (IL-6 + TNF-α)) × S_IL10     [Recruitment & activation]
      - d_M × (M - M₀)                                            [Decay to baseline]
```

### Logic

Both equations share the same structure:

1. **Recruitment** is driven by:
   - **Direct bacterial stimulation** (bacteria attract immune cells)
   - **Cytokine-mediated activation** (IL-6 and TNF-α amplify the immune response)
2. **IL-10 suppresses** recruitment via S_IL10
3. **Decay** pulls the population back toward resting baseline (N₀ or M₀)

### Example (Neutrophils)

- B = 0.5, IL-6 = 0.3, TNF-α = 0.1, N = 0.3, N₀ = 0.05
- k_N_rec = 0.5, k_N_cyt = 0.3, d_N = 0.1, S_IL10 = 0.5

```
Recruitment = (0.5 × 0.5 + 0.3 × (0.3 + 0.1)) × 0.5
            = (0.25 + 0.12) × 0.5 = 0.185
Decay       = 0.1 × (0.3 - 0.05) = 0.025

dN/dt = 0.185 - 0.025 = +0.16 (neutrophils are increasing)
```

---

## 4. Cytokine Network

### IL-6 (pro-inflammatory)

```
d[IL-6]/dt = (k_IL6_N × N + k_IL6_M × M) × B × S_IL10     [Production by neutrophils & macrophages]
           - d_IL6 × [IL-6]                                  [Natural degradation]
```

- Both neutrophils and macrophages produce IL-6 when they encounter bacteria
- Production is suppressed by IL-10

### TNF-α (pro-inflammatory)

```
d[TNF-α]/dt = k_TNF_M × M × B × S_IL10                     [Macrophage-driven production]
            - d_TNF × [TNF-α]                                [Natural degradation]
```

- TNF-α is **predominantly macrophage-driven** (no neutrophil term)

### IL-10 (anti-inflammatory)

```
d[IL-10]/dt = k_IL10_M × (M - M₀)                           [Macrophage-derived]
            + k_IL10_cyt × (IL-6 + TNF-α)                    [Pro-inflammatory-driven]
            - d_IL10 × [IL-10]                                [Degradation]
```

- IL-10 production increases with activated macrophages AND with high pro-inflammatory cytokines
- This creates a **negative feedback loop**: more inflammation → more IL-10 → suppressed inflammation

### The Feedback Loop (Key System Behavior)

```
                    ┌──────────────────────────────────┐
                    │                                  │
 Bacteria ──→ Neutrophils ──→ IL-6 ──→ recruits more Neutrophils & Macrophages
    │              │            │
    │              │            └──→ triggers IL-10 production
    │              │
    └────→ Macrophages ──→ TNF-α ──→ recruits more Neutrophils & Macrophages
                │              │
                │              └──→ triggers IL-10 production
                │
                └──→ IL-10 ──→ SUPPRESSES all of the above (via S_IL10)
```

This negative feedback loop is what determines whether infection resolves or spirals into sepsis.

---

## 5. Tissue Damage Index (D) — DAMP Dynamics

### Formula

```
dD/dt = k_D_bact × B                      [Direct bacterial toxicity]
      + k_D_cyt × (IL-6 + TNF-α)          [Inflammatory collateral damage]
      + k_D_comp × D²                     [Self-amplifying cascade]
      - d_D × D                           [Tissue repair]
```

### Term-by-term breakdown

| Term | Meaning |
|------|---------|
| **k_D_bact × B** | Bacteria directly damage tissue through toxins (e.g., LPS endotoxin). More bacteria = more direct tissue injury. |
| **k_D_cyt × (IL-6 + TNF-α)** | Pro-inflammatory cytokines cause collateral tissue damage (immune-mediated injury). This is the "friendly fire" component of sepsis. |
| **k_D_comp × D²** | **Quadratic self-amplification**. Damaged tissue releases DAMPs (Damage-Associated Molecular Patterns), which trigger MORE inflammation, which causes MORE damage. This term makes the system **bistable** — once D crosses a critical threshold, damage becomes self-sustaining even without bacteria. |
| **d_D × D** | Natural tissue repair and DAMP clearance. |

### Why D² (quadratic) is crucial

The D² term is what creates the **sepsis tipping point**. Consider:

- At **low D** (say D = 0.1): D² = 0.01 — negligible self-amplification
- At **moderate D** (say D = 0.3): D² = 0.09 — starting to matter
- At **high D** (say D = 0.5): D² = 0.25 — significant positive feedback

This creates a **bifurcation**: below a critical threshold, repair wins and D → 0. Above the threshold, self-amplification wins and D → ∞ (organ failure).

### The Sepsis Threshold: D = 0.36

The model defines **D = 0.36** as the sepsis threshold. Above this value, the system crosses an "unstable manifold" and transitions to an **irreversible inflammatory attractor** — meaning the damage becomes self-sustaining and the patient enters septic organ failure, consistent with the Sepsis-3 consensus definition.

### How D is calculated — Step by Step Example

Let's walk through how D evolves over a 3-step example with time steps of Δt = 1 hour:

**Parameters:**
- k_D_bact = 0.05
- k_D_cyt = 0.02
- k_D_comp = 0.10
- d_D = 0.04

**Step 1: t = 0h → t = 1h**
- Initial: D = 0.0, B = 0.4, IL-6 = 0.1, TNF-α = 0.05

```
dD/dt = 0.05 × 0.4 + 0.02 × (0.1 + 0.05) + 0.10 × 0.0² - 0.04 × 0.0
      = 0.020     + 0.003              + 0.0          - 0.0
      = 0.023

D(1h) = 0.0 + 0.023 × 1 = 0.023
```

**Step 2: t = 1h → t = 2h**
- Now: D = 0.023, B = 0.5 (growing), IL-6 = 0.2, TNF-α = 0.1

```
dD/dt = 0.05 × 0.5 + 0.02 × (0.2 + 0.1) + 0.10 × 0.023² - 0.04 × 0.023
      = 0.025     + 0.006              + 0.00005        - 0.00092
      = 0.03013

D(2h) = 0.023 + 0.03013 × 1 = 0.05313
```

**Step 3: t = 2h → t = 3h**
- Now: D = 0.053, B = 0.6, IL-6 = 0.35, TNF-α = 0.15

```
dD/dt = 0.05 × 0.6 + 0.02 × (0.35 + 0.15) + 0.10 × 0.05313² - 0.04 × 0.05313
      = 0.030     + 0.010               + 0.00028       - 0.00213
      = 0.03815

D(3h) = 0.05313 + 0.03815 × 1 = 0.09128
```

> **Key observation**: D accelerates over time. At early stages, bacterial toxicity dominates. As cytokines rise, the cytokine term grows. Eventually, D² positive feedback takes over. If D reaches 0.36, the system tips into irreversible organ damage.

### Graphical intuition for D dynamics

```
D
|
|                                          ___--- SEPSIS (D > 0.36)
|                                     ___/
|                                ___/
|  Sepsis threshold --------- / -------- D = 0.36
|                           /
|                        /    ← D² kicks in
|                     /
|                  /
|              /
|          /
|      / ← Linear growth (bacterial + cytokine damage)
|   /
|_/__________________________________ time
```

---

## 6. One-Compartment Antibiotic Pharmacokinetics & Pharmacodynamics (with Absorption Depot)

### PK Model (Drug Concentration Over Time)

**Depot compartment** (absorption):

```
dA_depot/dt = -k_a × A_depot + Σ Dose × δ(t - t_n)
```

**Plasma compartment** (elimination):

```
dA_plasma/dt = k_a × A_depot × F - k_el × A_plasma
```

| Symbol | Meaning |
|--------|---------|
| k_a | Absorption rate constant |
| δ(t − t_n) | Dirac delta: instantaneous dose at time t_n |
| F | Bioavailability (= 1.0 for IV) |
| k_el | Elimination rate constant |

### Drug Parameters

| Drug | Dose | Interval | k_el | Half-life |
|------|------|----------|------|-----------|
| **Ceftriaxone** | 60.0 mg/L | Every 24h | 0.087 | ~8 hours |
| **Meropenem** | 40.0 mg/L | Every 8h | 0.69 | ~1 hour |

Treatment starts at **t = 6 hours** post-infection.

### PD Model (Drug Effect)

First, calculate **effective concentrations** (modified by resistance):

```
A_eff   = A_plasma / φ_abx
MIC_eff = MIC_base 
```

Then, the killing effect uses a **Hill function**:

```
              ┌  E_max × (A_eff)^n / (EC50^n + (A_eff)^n)    if A_eff ≥ MIC_eff
E_abx =       │
              └  0                                             otherwise
```

Where: **n = 2.5**, **EC₅₀ = 2.0**, **E_max = 0.40**.

### Effect of resistance gene (bla_1 + IS6)

- φ_abx = exp(0.350 + 0.388) ≈ 2.09
- This **reduces** effective drug concentration: A_eff = A_plasma / 2.09
- The intrinsic MIC remains the same: MIC_eff = MIC_base
- Net effect: the drug appears **weaker** against resistant bacteria
- **Only applies to ceftriaxone** (beta-lactam); meropenem (carbapenem) is unaffected

### Example

Suppose A_plasma = 30 mg/L, MIC_base = 4 mg/L:

**Without resistance (φ_abx = 1.0):**
```
A_eff   = 30 / 1.0 = 30
MIC_eff = 4 × 1.0 = 4
A_eff (30) ≥ MIC_eff (4) ✓

E_abx = 0.40 × 30^2.5 / (2.0^2.5 + 30^2.5)
      = 0.40 × 4930 / (5.66 + 4930)
      = 0.40 × 0.999 = 0.399 (near maximal killing)
```

**With resistance (φ_abx = 2.09):**
```
A_eff   = 30 / 2.09 = 14.35
MIC_eff = 4 
A_eff (14.35) ≥ MIC_eff (4) ✓

E_abx = 0.40 × 14.35^2.5 / (2.0^2.5 + 14.35^2.5)
      = 0.40 × 754 / (5.66 + 754)
      = 0.40 × 0.993 = 0.397
```

> In this case, because the concentration is still well above EC₅₀, resistance doesn't dramatically reduce killing yet. However, as the drug clears (half-life decay), the resistant strain will fall below MIC_eff **sooner** than the susceptible strain, creating a critical window of subtherapeutic exposure.

---

## 7. Pyseer Gene Effect Size Integration

This is the **core innovation** — connecting statistical genomics to mechanistic modelling.

### The Transformation: β → φ

```
φ = e^β
```

Where **β** is the **log-odds coefficient** from pyseer's linear mixed model (LMM). It tells us how much a gene's presence increases the odds of the invasive/sepsis phenotype.

### Why exp(β)?

In logistic regression, β represents a **log-odds ratio**. Exponentiating converts it to an **odds ratio** (multiplicative effect):

| β (log-odds) | φ = exp(β) | Interpretation |
|---------------|------------|----------------|
| 0 | 1.0 | No effect |
| +0.394 | 1.48 | 48% increase in odds of virulence |
| +0.434 | 1.54 | 54% increase in odds of virulence |
| +0.738 | 2.09 | 109% increase (combined bla_1 + IS6) |

### Gene-Specific Mappings

#### 1. egtB (β = +0.394, φ_ROS = 1.48)

- **Biological function**: Catalyzes ergothioneine biosynthesis, a potent antioxidant
- **Mechanism**: Ergothioneine scavenges reactive oxygen species (ROS), reducing neutrophil oxidative burst killing
- **Model effect**: Divides the oxidative killing rate:

```
k_NB_ox → k_NB_ox / φ_ROS = k_NB_ox / 1.48
```

> This means oxidative killing is reduced to **67%** of normal (1/1.48 = 0.68).

#### 2. clpK/clpB (β = +0.434, φ_stress = 1.54)

- **Biological function**: Disaggregase/chaperone system that refolds aggregated proteins
- **Mechanism**: Enables bacteria to survive the proteotoxic stress inside macrophage phagolysosomes
- **Model effect**: Divides macrophage bactericidal rate:

```
k_MB → k_MB / φ_stress = k_MB / 1.54
```

> Macrophage killing reduced to **65%** of normal (1/1.54 = 0.65).

#### 3. bla_1 + IS6 transposase (β = +0.350 + 0.388 = +0.738, φ_abx = 2.09)

- **Biological function**: Beta-lactamase gene mobilized by IS6 transposable element
- **Mechanism**: Hydrolyzes beta-lactam antibiotics (e.g., ceftriaxone), conferring resistance
- **Model effect**: Modifies antibiotic pharmacodynamics:

```
A_eff   = A_plasma / φ_abx
MIC_eff = MIC_base
```

> Only affects **ceftriaxone** (beta-lactam); meropenem (carbapenem) is intrinsically stable against beta-lactamases.

---

## 8. Complete Worked Example

### Scenario: Invasive genotype, untreated (all virulence genes active)

**Initial conditions (t = 0):**

| Variable | Value | Meaning |
|----------|-------|---------|
| B₀ | 0.01 | Small initial bacterial inoculum |
| N₀ | 0.05 | Resting neutrophil level |
| M₀ | 0.05 | Resting macrophage level |
| IL-6₀ | 0.0 | No initial cytokines |
| TNF-α₀ | 0.0 | No initial cytokines |
| IL-10₀ | 0.0 | No initial anti-inflammatory |
| D₀ | 0.0 | No initial tissue damage |

**Virulence modifiers:**
- φ_ROS = exp(0.394) = 1.48
- φ_stress = exp(0.434) = 1.54
- φ_abx = exp(0.738) = 2.09 (irrelevant since no antibiotic)

### Computing the first time step (Euler method, Δt = 0.1h)

At t = 0, IL-10 = 0, so **S_IL10 = 1/(1 + κ × 0) = 1** (no suppression initially).

**1. Bacteria (dB/dt):**
```
Growth:       k_b × 0.01 × (1 - 0.01) = k_b × 0.0099 ≈ 0.006 (if k_b ≈ 0.6)
Death:        d_b × 0.01 = 0.001
Surveillance: k_surv × 0.01 = 0.0005
Neutrophil:   (k_NB_ox/1.48 + k_NB_pep) × (0.05 - 0.05) × 0.01 × 1 = 0
              ↑ (N = N₀, so no activated neutrophils yet!)
Macrophage:   (k_MB/1.54) × (0.05 - 0.05) × 0.01 × 1 = 0
              ↑ (M = M₀, so no activated macrophages yet!)

dB/dt ≈ 0.006 - 0.001 - 0.0005 = 0.0045
B(0.1h) = 0.01 + 0.0045 × 0.1 = 0.01045
```

> **Early phase**: Bacteria grow almost unopposed because immune cells haven't been recruited above baseline yet.

**2. Neutrophils (dN/dt):**
```
Recruitment = (k_N_rec × 0.01 + k_N_cyt × (0 + 0)) × 1 = k_N_rec × 0.01
Decay       = d_N × (0.05 - 0.05) = 0

dN/dt = k_N_rec × 0.01 (small but positive — beginning to recruit)
```

**3. Tissue Damage (dD/dt):**
```
dD/dt = k_D_bact × 0.01 + k_D_cyt × (0 + 0) + k_D_comp × 0² - d_D × 0
      = k_D_bact × 0.01  (small initial damage from bacteria)
```

### What happens over 168 hours (7 days)?

The ODE solver (e.g., Runge-Kutta 4th order) integrates all 9 equations simultaneously. The typical trajectory for an **untreated invasive strain**:

| Time | B | N | M | IL-6 | TNF-α | IL-10 | D | Phase |
|------|---|---|---|------|-------|-------|---|-------|
| 0h | 0.01 | 0.05 | 0.05 | 0.0 | 0.0 | 0.0 | 0.0 | Inoculation |
| 6h | ~0.3 | ~0.15 | ~0.12 | ~0.15 | ~0.08 | ~0.02 | ~0.05 | Exponential bacterial growth |
| 12h | ~0.6 | ~0.35 | ~0.25 | ~0.40 | ~0.20 | ~0.08 | ~0.15 | Immune response peaks |
| 24h | ~0.7 | ~0.30 | ~0.22 | ~0.35 | ~0.18 | ~0.12 | ~0.30 | IL-10 suppression begins |
| 36h | ~0.8 | ~0.20 | ~0.15 | ~0.25 | ~0.12 | ~0.15 | **0.38** | **D > 0.36: SEPSIS** |
| 72h | ~0.9 | ~0.12 | ~0.10 | ~0.15 | ~0.08 | ~0.18 | ~0.60 | Irreversible organ failure |
| 168h | ~1.0 | ~0.08 | ~0.07 | ~0.10 | ~0.05 | ~0.15 | ~0.85 | Terminal |

> **CAUTION**: At ~36h, D crosses the 0.36 threshold. The D² self-amplification term now dominates, driving damage upward even as immune cells are being suppressed by IL-10 and the bacterial load saturates.

---

## 9. Summary of All Variables & Parameters

### State Variables

| Symbol | Description | Units |
|--------|-------------|-------|
| B | Normalised bacterial load | Dimensionless [0, 1] |
| N | Activated neutrophil concentration | Normalised |
| M | Activated macrophage concentration | Normalised |
| IL-6 | Interleukin-6 | Normalised |
| TNF-α | Tumour necrosis factor alpha | Normalised |
| IL-10 | Interleukin-10 | Normalised |
| D | Tissue damage index / DAMP | Normalised |
| A_depot | Antibiotic in depot compartment | mg/L |
| A_plasma | Antibiotic in plasma | mg/L |

### Key Parameters

| Symbol | Description |
|--------|-------------|
| k_b | Bacterial growth rate |
| d_b | Bacterial natural death rate |
| k_surv | Baseline immune surveillance rate |
| k_NB_ox | Neutrophil oxidative killing rate |
| k_NB_pep | Neutrophil peptide killing rate |
| k_MB | Macrophage bactericidal rate |
| k_N_rec | Neutrophil recruitment by bacteria |
| k_N_cyt | Neutrophil recruitment by cytokines |
| k_M_bact | Macrophage recruitment by bacteria |
| k_M_cyt | Macrophage recruitment by cytokines |
| k_IL6_N | IL-6 production rate by neutrophils |
| k_IL6_M | IL-6 production rate by macrophages |
| k_TNF_M | TNF-α production rate by macrophages |
| k_IL10_M | IL-10 production by macrophages |
| k_IL10_cyt | IL-10 production by cytokines |
| k_D_bact | Damage rate from bacteria |
| k_D_cyt | Damage rate from cytokines |
| k_D_comp | Damage self-amplification coefficient |
| d_N, d_M, d_IL6, d_TNF, d_IL10, d_D | Respective decay/clearance rates |
| κ_IL10 | IL-10 suppression sensitivity |
| N₀, M₀ | Resting baseline for neutrophils/macrophages |
| k_a | Drug absorption rate |
| F | Bioavailability |
| k_el | Elimination rate constant |
| E_max | Maximum antibiotic killing effect |
| EC₅₀ | Half-maximal effective concentration |
| n | Hill coefficient |
| MIC_base | Baseline minimum inhibitory concentration |

### Virulence Modifiers (from pyseer)

| Gene | β | φ = exp(β) | Target Parameter | Effect |
|------|---|------------|-----------------|--------|
| egtB | +0.394 | 1.48 (φ_ROS) | k_NB_ox / φ_ROS | ↓ Oxidative killing by 32% |
| clpK/clpB | +0.434 | 1.54 (φ_stress) | k_MB / φ_stress | ↓ Macrophage killing by 35% |
| bla_1 + IS6 | +0.738 | 2.09 (φ_abx) | A_eff / φ_abx, MIC × φ_abx | ↓ Ceftriaxone efficacy |

---

## Summary of the Complete System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM OVERVIEW                                │
│                                                                        │
│   VIRULENCE GENES (pyseer β → φ)                                      │
│   ┌─────────────────────────────────────────────┐                      │
│   │ egtB     → φ_ROS = 1.48   → ↓ Neutrophil   │                      │
│   │ clpK/clpB→ φ_stress = 1.54→ ↓ Macrophage   │                      │
│   │ bla_1+IS6→ φ_abx = 2.09  → ↓ Ceftriaxone  │                      │
│   └─────────────────────────────────────────────┘                      │
│                                                                        │
│   BACTERIA (B)                                                         │
│      ↕ logistic growth                                                 │
│      ↓ killed by N, M, antibiotics                                     │
│      ↓ stimulates recruitment of N, M                                  │
│      ↓ produces tissue damage (D)                                      │
│                                                                        │
│   IMMUNE CELLS                    CYTOKINES                            │
│   ┌──────────┐  produce  ┌────────────────┐                            │
│   │ N (Neut) │──────────→│ IL-6, TNF-α    │──→ recruit more N, M       │
│   │ M (Macro)│──────────→│                │                            │
│   └──────────┘           └───────┬────────┘                            │
│        ↑                         │                                     │
│        │ suppress (S_IL10)       ↓ triggers                            │
│        │                   ┌──────────┐                                │
│        └───────────────────│  IL-10   │                                │
│                            └──────────┘                                │
│                                                                        │
│   TISSUE DAMAGE (D)                                                    │
│   ┌─────────────────────────────────────────┐                          │
│   │  Sources: bacteria + cytokines + D²     │                          │
│   │  Repair: d_D × D                        │                          │
│   │  THRESHOLD: D = 0.36 → SEPSIS           │                          │
│   └─────────────────────────────────────────┘                          │
│                                                                        │
│   ANTIBIOTICS (PK/PD)                                                  │
│   ┌─────────────────────────────────────────┐                          │
│   │  Depot → Plasma → E_abx (Hill function) │                          │
│   │  Modified by φ_abx resistance           │                          │
│   └─────────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────┘
```

> **The model's central insight**: pyseer's statistical associations (β values) are not just correlations — when mapped through the exponential transformation φ = exp(β), they become quantitative predictions of how much each virulence gene degrades specific immune defence mechanisms. This bridges the gap between population-level GWAS and mechanistic infection modelling.
