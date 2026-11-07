# Understanding Global Sensitivity Analysis: LHS and PRCC

This document explains the mathematical methods used to evaluate the sensitivity and robustness of the sepsis ODE model, along with a detailed explanation of the generated graphs.

---

## 1. Latin Hypercube Sampling (LHS)

### What is it?
Latin Hypercube Sampling (LHS) is a statistical method for generating a near-random sample of parameter values from a multidimensional distribution. 

### Why was it used?
In biological models, parameters (like bacterial growth rates or immune killing rates) are rarely known with 100% certainty. We need to test the model across thousands of possible parameter combinations to ensure our conclusions hold true even if our base assumptions are slightly off. 

A traditional "grid search" (testing every possible combination of 10 parameters) would take an astronomical amount of time. Random sampling (Monte Carlo) might accidentally cluster samples together, leaving gaps in the data. LHS is a "stratified" sampling method that guarantees every segment of every parameter's range is tested, making it highly computationally efficient.

### How is it calculated?
1. If we want 1,000 samples, we divide the range of each of our 10 parameters into 1,000 equal-probability intervals.
2. We pick exactly one random value from inside each of those 1,000 intervals for every parameter.
3. We randomly shuffle these values and pair them together to create 1,000 unique parameter sets.

**Example**: Imagine you are testing a cake recipe with 3 ingredients: Flour, Sugar, and Butter, and you want to test 5 variations. LHS divides each ingredient's quantity range into 5 bins. It guarantees you will bake exactly one cake with the lowest amount of sugar, exactly one with the highest amount, etc., paired randomly with the flour and butter bins.

---

## 2. Partial Rank Correlation Coefficient (PRCC)

### What is it?
PRCC is a statistical metric used in sensitivity analysis. It measures the strength of the relationship between a single input parameter and the model's final output, while **controlling for** (or mathematically removing) the effects of all the other inputs.

### Why was it used?
Since we varied 10 parameters simultaneously using LHS, the final tissue damage ($D_{max}$) is a messy combination of all 10 changes. If $D_{max}$ goes up, was it because bacterial growth went up, or because tissue repair went down? PRCC isolates each parameter to answer: *"If we keep everything else constant, how strongly does THIS specific parameter affect the outcome?"*

We use the **Rank** version (PRCC instead of just PCC) because biological relationships are often non-linear (e.g., exponential growth). Ranking the data first handles non-linear relationships smoothly.

### How is it calculated?
1. **Rank Transformation**: We convert all the raw parameter values and output $D_{max}$ values into ranks (1st smallest, 2nd smallest, etc.).
2. **Isolate the Parameter**: For a specific parameter (e.g., bacterial growth $k_b$), we run a linear regression predicting $k_b$ using the other 9 parameters, and we take the **residuals** (the part of $k_b$ that the other parameters *cannot* explain).
3. **Isolate the Output**: We run another regression predicting $D_{max}$ using those same 9 parameters, and take the residuals.
4. **Correlation**: We calculate the standard Pearson correlation between those two sets of residuals. This gives a value between -1.0 (strong protective effect) and +1.0 (strong harmful effect).

---

## 3. Explaining the Generated Graphs

### Fig5: PRCC Tornado Plot (`Fig5_PRCC_Tornado.png`)
- **What it shows**: This is a horizontal bar chart ranking the 10 parameters by how much they influence peak tissue damage ($D_{max}$).
- **How to read it**: 
  - **Red bars** going to the right have a positive PRCC. If these parameters increase, tissue damage increases (they are **Pro-sepsis**). 
  - **Blue bars** going to the left have a negative PRCC. If these parameters increase, tissue damage decreases (they are **Protective**).
  - The wider the bar, the stronger the effect. Here, bacterial growth ($k_b$) is the strongest driver.
  - The `***` (or lack thereof) indicates statistical significance (p-value).

### Fig6: Scatter Plots (`Fig6_Phi_vs_Dmax_Scatter.png`)
- **What it shows**: This graph takes the raw data from the LHS simulations and plots just our PySEER genetic multipliers ($\phi_{ROS}$ and $\phi_{stress}$) on the X-axis against the resulting tissue damage ($D_{max}$) on the Y-axis.
- **How to read it**: 
  - The **red dotted horizontal line** is the sepsis threshold ($D = 0.36$).
  - **Red dots** are simulations that resulted in sepsis; **Blue dots** did not.
  - The black dashed trendline shows the positive slope. As the bacterial genetic evasion multipliers increase (moving right on the X-axis), the resulting tissue damage generally increases (moving up on the Y-axis), visually confirming the PRCC results.

### Fig7: Mapping Comparison (`Fig7_Mapping_Comparison.png`)
- **What it shows**: This plot addresses the mathematical translation of genetic statistics. It compares how the model's sepsis predictions change if we use different mathematical functions (exp, 1+$\beta$, $2^\beta$, $10^\beta$) to convert the PySEER $\beta$ statistics into the $\phi$ multipliers.
- **How to read it**:
  - The **blue boxes/violins** show the distribution of peak tissue damage ($D_{max}$) for each mapping method across 200 random simulations.
  - The **red dotted line** is the sepsis threshold.
  - **The key takeaway**: For the first three mappings, the median (thick black line) and the majority of the blue shape remain above the red dotted line (50-59% sepsis). This proves the model's conclusion (that these genes cause sepsis) doesn't just happen because we chose a lucky math function.
  - **The 4th Plot ($10^\beta$)**: The box here looks like a single flat line because the mathematical effect is so massively inflated that nearly every single simulation instantly hits the model's absolute maximum limit for damage ($D_{max} = 1.50$). Because the 25th percentile, the median, and the 75th percentile are all exactly 1.50, the "box" has zero height.
