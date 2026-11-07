# Global Sensitivity Analysis for the Pyseer-ODE Sepsis Model

## Background

The reviewer will inevitably ask: **"Why did you use exp(β) to map GWAS log-odds into ODE rate multipliers?"** The answer is that `exp(β)` recovers the odds ratio — a natural, unitless multiplier — but it is still an *assumption*, not a measured biological rate. 

A **Global Sensitivity Analysis (GSA)** using **Latin Hypercube Sampling (LHS)** combined with **Partial Rank Correlation Coefficients (PRCC)** (per Marino et al. 2008, *J. Theor. Biol.*) will:

1. Systematically vary φ multipliers across a wide range (not just `exp(β)` but also `1+β`, `2^β`, `10^β`, uniform random perturbations)
2. Simultaneously vary all key ODE rate parameters (±20–50%)
3. Measure whether the **qualitative outcome** (fatal sepsis: $D > 0.36$ vs. survival) remains robust regardless of the mapping function
4. Identify which parameters the model is most/least sensitive to

This directly addresses the reviewer's concern: *"Even if the β→φ mapping is different, the sepsis vs. survival outcome is preserved."*

## Proposed Changes

### Sensitivity Analysis Script

#### [NEW] [sensitivity_analysis.py](file:///Users/gauthamgl/Desktop/capstone/sensitivity_analysis.py)

A standalone Python script that:

1. **Defines the parameter space** — 10 key parameters to vary:
   - `φ_ROS` (egtB multiplier) — varied ±50% around `exp(0.394) = 1.48`
   - `φ_stress` (clpK multiplier) — varied ±50% around `exp(0.434) = 1.54`
   - `φ_abx` (resistance multiplier) — varied ±50% around `exp(0.738) = 2.09`
   - `k_b` (bacterial growth rate)
   - `k_NB_ox` (neutrophil oxidative killing)
   - `k_D_comp` (quadratic damage amplification)
   - `kappa_IL10` (IL-10 suppression strength)
   - `k_IL10_cyt` (CARS cytokine-driven IL-10 production)
   - `d_D` (tissue damage repair rate)
   - `E_max` (antibiotic maximum efficacy)

2. **Latin Hypercube Sampling (LHS)** — Generates N=1000 parameter combinations uniformly spanning the ranges, ensuring maximal coverage of the parameter space (stratified sampling).

3. **Runs 1000 simulations** — For each LHS sample, runs the full ODE with the perturbed parameters and records:
   - Peak Damage ($D_{max}$) — the primary clinical outcome
   - Peak Bacterial Load ($B_{max}$)
   - Time to bacterial clearance (if cleared)
   - Binary sepsis outcome ($D_{max} > 0.36$? yes/no)

4. **Computes PRCC** — Calculates the Partial Rank Correlation Coefficient between each input parameter and each output metric. PRCC measures the monotonic relationship between a single parameter and the output *while controlling for all other parameters*.

5. **Generates publication-ready figures**:
   - **Tornado plot** — Horizontal bar chart showing PRCC values for $D_{max}$, ranked by magnitude
   - **Scatter plots** — φ_ROS, φ_stress, φ_abx vs. $D_{max}$ with LOESS trend line
   - **Alternative mapping comparison** — Box plot comparing $D_{max}$ distributions under `exp(β)`, `1+β`, `2^β`, and `10^β` mappings

> [!IMPORTANT]
> The alternative mapping comparison is the key figure that directly answers the reviewer's question. It will show four box plots side by side demonstrating that the qualitative outcome (sepsis threshold crossing) is preserved across all reasonable mapping functions.

## Verification Plan

### Automated Tests
- Run the sensitivity analysis script end-to-end
- Verify that 1000 simulations complete without numerical errors
- Confirm PRCC values fall within [-1, +1]
- Verify figures are generated in `individual_graphs/`

### Manual Verification
- Inspect tornado plot to confirm φ multipliers and `k_D_comp` have the highest PRCC (expected)
- Confirm the alternative mapping box plot shows consistent sepsis outcomes across all mapping functions

## Open Questions

> [!NOTE]
> **Sample size**: N=1000 is standard per Marino et al. (2008). This will take approximately 3–5 minutes to run. Should I increase to N=2000 for extra robustness?

> [!NOTE]
> **Parameter ranges**: I plan to use ±50% for the φ multipliers and ±30% for the ODE rate constants. This is aggressive enough to satisfy reviewers that the model is robust. Does this seem reasonable to you?
