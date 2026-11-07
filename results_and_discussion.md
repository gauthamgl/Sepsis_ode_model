# Results

To determine the most critical drivers of peak tissue damage ($D_{max}$) and to validate the stability of the sepsis predictions to parameter uncertainty, a global sensitivity analysis was performed utilizing Latin Hypercube Sampling (LHS) and Partial Rank Correlation Coefficient (PRCC) analysis [X1]. Over a set of 1,000 LHS simulations spanning the parameter space, 55.7% of the parameter combinations resulted in the tissue damage state variable crossing the sepsis threshold ($D_{max} > 0.36$). The resulting $D_{max}$ values ranged from 0.101 to 1.501, demonstrating a wide dynamic range in response to parameter variations.

The PRCC analysis quantified the independent influence of each parameter on $D_{max}$ while controlling for the other variables [Y1]. All 10 assessed parameters were found to be statistically significant drivers of tissue damage ($p < 10^{-5}$). The bacterial growth rate ($k_b$) exerted the strongest pro-sepsis effect (PRCC = $+0.7589$). Furthermore, cytokine-driven tissue damage ($k_{D,cyt}$) was a major contributor to pathogenesis (PRCC = $+0.5179$). The PySEER-derived multipliers representing genotype-driven immune evasion were also among the strongest drivers: the clpK/clpB-associated stress evasion multiplier ($\phi_{stress}$) had a PRCC of $+0.5397$, and the egtB-associated ROS evasion multiplier ($\phi_{ROS}$) had a PRCC of $+0.4056$. The strong positive monotonic relationships between these multipliers and $D_{max}$ are depicted in [Y2]. Conversely, parameters associated with tissue repair ($d_D$, PRCC = $-0.4158$) and neutrophil oxidative killing ($k_{NB,ox}$, PRCC = $-0.2499$) were strongly protective, correlating with reduced peak damage.

To investigate whether the transition to a sepsis state was sensitive to the functional form of the $\beta \rightarrow \phi$ mapping, the sensitivity analysis was repeated using four alternative mapping functions: $\exp(\beta)$, $1 + \beta$, $2^\beta$, and $10^\beta$. The qualitative sepsis outcome, defined as crossing the $D > 0.36$ threshold, was consistently preserved across all evaluated mappings [Y3]. The proportion of simulations progressing to sepsis was 59.0% for $\exp(\beta)$, 55.0% for $1 + \beta$, 50.5% for $2^\beta$, and 93.5% for $10^\beta$. 

# Discussion

The global sensitivity analysis underscores the critical dependence of sepsis progression on unrestricted bacterial replication and immune evasion. The strong influence of the PySEER-derived multipliers ($\phi_{stress}$ and $\phi_{ROS}$) highlights the mechanistic importance of the bacterial genetic background in determining the severity of the host response. 

A key concern addressed in this study was whether the qualitative model predictions were overly sensitive to the mathematical translation of statistical GWAS effect sizes into mechanistic ODE multipliers. While the $10^\beta$ mapping produced more extreme values that clustered at the upper simulation bound ($D_{max} = 1.50$), all mappings consistently predicted that the invasive genotype combinations possess a strong baseline propensity for causing sepsis. This consistency demonstrates that the core conclusions drawn from the integrated PySEER-ODE framework are highly reliable and do not artifactually depend on the default exponential mapping choice.

---
### Embedded Figures
- **[Y1]**: `Fig5_PRCC_Tornado.png` - Tornado plot of PRCC values showing parameter importance.
- **[Y2]**: `Fig6_Phi_vs_Dmax_Scatter.png` - Scatter plots depicting the relationship between PySEER multipliers ($\phi_{ROS}$ and $\phi_{stress}$) and $D_{max}$.
- **[Y3]**: `Fig7_Mapping_Comparison.png` - Box and violin plots comparing peak tissue damage and threshold crossing behavior across the four alternative $\beta \rightarrow \phi$ mapping functions.
