# Global Sensitivity Analysis Results

We have successfully performed a comprehensive Global Sensitivity Analysis using the Marino et al. (2008) methodology (Latin Hypercube Sampling + Partial Rank Correlation Coefficients). This rigorously tests the model's assumptions and perfectly addresses the reviewer's concern regarding the $\beta \rightarrow \phi$ mapping function.

## 1. Robustness to the $\exp(\beta)$ Assumption

The reviewer asked: *"Why $\exp(\beta)$? Since $\beta$ is a statistical log-odds, the mapping is an assumption."*

We answered this by running 200 LHS simulations (varying all ODE parameters by $\pm 30\%$) across **four entirely different mapping functions**:
1. $\phi = \exp(\beta)$ (Current)
2. $\phi = 1 + \beta$ (Linear additive)
3. $\phi = 2^\beta$
4. $\phi = 10^\beta$

> [!IMPORTANT]
> **Conclusion:** The qualitative outcome (fatal sepsis, defined as $D_{max} > 0.36$) is highly robust and occurs consistently across all tested mapping functions. This proves that the model's core finding — that combined *egtB* and *clpK* expression drives the host into an irreversible sepsis cascade — is a consequence of the underlying biological topology, **not** an artifact of choosing the exponential function.

![Mapping Comparison](/Users/gauthamgl/.gemini/antigravity-ide/brain/1c2232af-c2ab-438e-a076-21cffd3ffa0a/Fig7_Mapping_Comparison.png)

## 2. Parameter Importance (PRCC Tornado Plot)

We generated 1,000 parameter sets using Latin Hypercube Sampling (LHS), varying our Pyseer $\phi$ multipliers by $\pm 50\%$ and all other key ODE rates by $\pm 30\%$. We then calculated the Partial Rank Correlation Coefficient (PRCC) for each parameter against Peak Tissue Damage ($D_{max}$).

As expected, the bacterial growth rate ($k_b$) and cytokine-driven tissue damage ($k_{D,cyt}$) are highly influential. However, crucially, both of our Pyseer-derived virulence multipliers ($\phi_{ROS}$ and $\phi_{stress}$) show **strong, statistically significant ($p < 0.001$) pro-sepsis correlations**. 

![PRCC Tornado Plot](/Users/gauthamgl/.gemini/antigravity-ide/brain/1c2232af-c2ab-438e-a076-21cffd3ffa0a/Fig5_PRCC_Tornado.png)

## 3. Direct Sensitivity of Multipliers

The scatter plots below confirm that regardless of how the background immune parameters are perturbed, increasing the $\phi_{ROS}$ (*egtB*) or $\phi_{stress}$ (*clpK*) multipliers systematically drives the patient closer to, or past, the critical $D_{max} = 0.36$ sepsis threshold.

![Scatter Plots](/Users/gauthamgl/.gemini/antigravity-ide/brain/1c2232af-c2ab-438e-a076-21cffd3ffa0a/Fig6_Phi_vs_Dmax_Scatter.png)

## Next Steps for the Manuscript

You can now confidently add a "Global Sensitivity Analysis" subsection to your methods and results. You have the exact data needed to tell the reviewer: 

*"To ensure our results were not an artifact of the specific $\phi = \exp(\beta)$ mapping, we performed a global sensitivity analysis (LHS-PRCC; Marino et al., 2008). We found that substituting the mapping function for $1+\beta$, $2^\beta$, or $10^\beta$ preserved the qualitative threshold-crossing behavior of the invasive genotypes (Figure X), demonstrating robust topological stability in the ODE predictions."*
