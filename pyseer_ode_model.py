"""
══════════════════════════════════════════════════════════════════════════════
Gram-Negative Bacterial Sepsis — Full Publication Suite
ODE Immune Model with Cascading Organ Failure & Delayed IL-10 CARS Kinetics
(Includes Robust Float Handling, Stiff ODE Tolerances, & Calibrated Control)
══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ─── PUBLICATION AESTHETICS ───────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "figure.dpi": 300,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.2,
    "lines.linewidth": 2.5,
})

# ═══════════════════════════════════════════════════════════════════════
# 1.  GENE PROFILE
# ═══════════════════════════════════════════════════════════════════════
@dataclass
class GeneProfile:
    """
    Encodes pyseer-identified virulence genes and translates beta
    coefficients into mechanistic multipliers used in the ODE system.
    """
    egtB:         bool = False
    clpKB_operon: bool = False
    bla_1:        bool = False
    group_5277:   bool = False

    _BETA_egtB:  float = field(default=0.394, init=False, repr=False)
    _BETA_clpKB: float = field(default=0.434, init=False, repr=False)
    _BETA_bla:   float = field(default=0.350, init=False, repr=False)
    _BETA_IS6:   float = field(default=0.388, init=False, repr=False)

    @property
    def phi_ROS(self) -> float:
        return float(np.exp(self._BETA_egtB)) if self.egtB else 1.0

    @property
    def phi_stress(self) -> float:
        return float(np.exp(self._BETA_clpKB)) if self.clpKB_operon else 1.0

    @property
    def phi_abx(self) -> float:
        if not (self.bla_1 or self.group_5277):
            return 1.0
        beta = (self._BETA_bla if self.bla_1 else 0.0) + \
               (self._BETA_IS6 if self.group_5277 else 0.0)
        return float(np.exp(beta))

    @property
    def virulence_score(self) -> float:
        s = 0.0
        if self.egtB:         s += self._BETA_egtB
        if self.clpKB_operon: s += self._BETA_clpKB
        if self.bla_1:        s += self._BETA_bla
        if self.group_5277:   s += self._BETA_IS6
        return s


# ═══════════════════════════════════════════════════════════════════════
# 2.  MODEL PARAMETERS
# ═══════════════════════════════════════════════════════════════════════
@dataclass
class ModelParameters:
    """
    All rate constants in per-hour units (time axis = hours).
    Concentrations normalised (0–1) unless noted (mg/L for antibiotics).
    """
    # ── Bacterial growth / death ──────────────────────────────
    k_b:    float = 0.45
    d_b:    float = 0.12

    # ── Baseline surveillance killing ─────────────────────────
    # Increased to 0.050 to ensure wild-type control naturally resolves
    k_surv: float = 0.050

    # ── Neutrophil dynamics ───────────────────────────────────
    N_0:      float = 1.0
    k_N_rec:  float = 1.50
    k_N_cyt:  float = 0.20
    d_N:      float = 0.09
    k_NB_ox:  float = 0.50
    k_NB_pep: float = 0.22

    # ── Macrophage dynamics ───────────────────────────────────
    M_0:      float = 1.0
    k_M_bact: float = 0.40
    k_M_cyt:  float = 0.30
    d_M:      float = 0.012
    k_MB:     float = 0.55

    # ── Cytokine production ───────────────────────────────────
    k_IL6_N:    float = 0.65
    k_IL6_M:    float = 1.20
    k_TNF_M:    float = 0.95

    # ── CARS Kinetics ─────────────────────────────────────────
    k_IL10_M:   float = 0.05
    k_IL10_cyt: float = 0.80

    # ── Cytokine degradation (/hr) ────────────────────────────
    d_IL6:  float = 0.40
    d_TNF:  float = 0.70
    d_IL10: float = 0.30

    # ── IL-10 immunosuppression ───────────────────────────────
    kappa_IL10: float = 0.55

    # ── Tissue damage / DAMP ─────────────────────────────────
    k_D_bact: float = 0.12
    k_D_cyt:  float = 0.06
    d_D:      float = 0.018

    # ── Cascading Organ Failure (quadratic amplification) ─────
    k_D_comp: float = 0.05

    # ── Antibiotic PD (Emax Hill model) ──────────────────────
    E_max:    float = 0.40
    EC50:     float = 2.0
    hill_n:   float = 2.5
    MIC_base: float = 0.50


# ═══════════════════════════════════════════════════════════════════════
# 3.  ANTIBIOTIC DOSING
# ═══════════════════════════════════════════════════════════════════════
@dataclass
class AntibioticDosing:
    drug_name:       str   = "Ceftriaxone"
    dose_mg_L:       float = 60.0
    interval_hr:     float = 24.0
    route:           str   = "IV"
    bioavailability: float = 1.0
    start_hr:        float = 6.0
    duration_days:   float = 7.0
    k_el:            float = 0.087  # Changed from CL to k_el
    k_a:             float = 5.0

    def dose_schedule(self, t_max_hr: float) -> List[float]:
        t_end = self.start_hr + self.duration_days * 24.0
        times, t = [], self.start_hr
        while t <= min(t_end, t_max_hr):
            times.append(t)
            t += self.interval_hr
        return times

def ceftriaxone(start_hr: float = 6.0) -> AntibioticDosing:
    return AntibioticDosing(
        drug_name="Ceftriaxone", dose_mg_L=60.0, interval_hr=24.0,
        start_hr=start_hr, k_el=0.087, k_a=5.0)

def meropenem(start_hr: float = 6.0) -> AntibioticDosing:
    return AntibioticDosing(
        drug_name="Meropenem", dose_mg_L=40.0, interval_hr=8.0,
        start_hr=start_hr, k_el=0.69, k_a=5.0)

def genes_control()    -> GeneProfile: return GeneProfile()
def genes_egtB_only()  -> GeneProfile: return GeneProfile(egtB=True)
def genes_clpKB_only() -> GeneProfile: return GeneProfile(clpKB_operon=True)
def genes_bla_IS6()    -> GeneProfile: return GeneProfile(bla_1=True, group_5277=True)
def genes_invasive()   -> GeneProfile:
    return GeneProfile(egtB=True, clpKB_operon=True, bla_1=True, group_5277=True)


# ═══════════════════════════════════════════════════════════════════════
# 4.  ODE SYSTEM
# ═══════════════════════════════════════════════════════════════════════
def sepsis_odes(
    t: float,
    y: np.ndarray,
    params: ModelParameters,
    genes: GeneProfile,
    dosing: Optional[AntibioticDosing],
) -> List[float]:

    B, N, M, IL6, TNF, IL10, D, A_dep, A_p = y
    p, g = params, genes

    B, IL6, TNF, IL10, D, A_dep, A_p = [
        max(v, 0.0) for v in [B, IL6, TNF, IL10, D, A_dep, A_p]]
    N = max(N, p.N_0)
    M = max(M, p.M_0)

    supp = 1.0 / (1.0 + p.kappa_IL10 * IL10)
    N_act = N - p.N_0
    M_act = M - p.M_0

    A_eff   = A_p / g.phi_abx
    MIC_eff = p.MIC_base  # Removed g.phi_abx multiplier here
    if A_eff >= MIC_eff:
        E_abx = p.E_max * (A_eff ** p.hill_n) / (
            p.EC50 ** p.hill_n + A_eff ** p.hill_n)
    else:
        E_abx = 0.0

    dB = (
        p.k_b  * B * (1.0 - B)
      - p.d_b  * B
      - p.k_surv * B
      - (p.k_NB_ox  / g.phi_ROS)    * N_act * B * supp
      - p.k_NB_pep                  * N_act * B * supp
      - (p.k_MB     / g.phi_stress) * M_act * B * supp
      - E_abx * B
    )

    dN = ((p.k_N_rec * B + p.k_N_cyt * (IL6 + TNF)) * supp) - (p.d_N * N_act)
    dM = ((p.k_M_bact * B + p.k_M_cyt * (IL6 + TNF)) * supp) - (p.d_M * M_act)

    # Using N and M (total cells, including resting) to drive the initial cytokine storm
    dIL6 = ((p.k_IL6_N * N + p.k_IL6_M * M) * B * supp) - (p.d_IL6 * IL6)
    dTNF = (p.k_TNF_M * M * B * supp) - (p.d_TNF * TNF)

    # ── DELAYED RESOLUTION PHASE IL-10 KINETICS ──
    dIL10 = (p.k_IL10_M * M_act + p.k_IL10_cyt * (IL6 + TNF)) - (p.d_IL10 * IL10)

    dD = (
        p.k_D_bact * B
      + p.k_D_cyt  * (IL6 + TNF)
      + p.k_D_comp * (D ** 2)
    ) - (p.d_D * D)

    if D > 1.5 and dD > 0:
        dD = 0.0

    if dosing is not None:
        dA_dep = -dosing.k_a * A_dep
        dA_p   =  dosing.k_a * A_dep * dosing.bioavailability - dosing.k_el * A_p  # Changed from dosing.CL
    else:
        dA_dep, dA_p = 0.0, 0.0

    return [dB, dN, dM, dIL6, dTNF, dIL10, dD, dA_dep, dA_p]


# ═══════════════════════════════════════════════════════════════════════
# 5.  SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════════════
def run_simulation(
    genes:    GeneProfile,
    dosing:   Optional[AntibioticDosing] = None,
    params:   Optional[ModelParameters]  = None,
    t_max_hr: float = 168.0,
    B0:       float = 0.05,  # Reduced starting inoculum so control naturally clears
    dt:       float = 0.25,
) -> Tuple[np.ndarray, np.ndarray]:

    if params is None:
        params = ModelParameters()

    y0 = np.array([B0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    dose_times: List[float] = dosing.dose_schedule(t_max_hr) if dosing else []
    breakpoints = sorted(set([0.0] + dose_times + [t_max_hr]))

    seg_t: List[np.ndarray] = []
    seg_y: List[np.ndarray] = []
    y_cur = y0.copy()

    for i in range(len(breakpoints) - 1):
        t0, t1 = breakpoints[i], breakpoints[i + 1]
        if t1 <= t0:
            continue

        # Robust float comparison for dose injection
        if dosing is not None and any(abs(t0 - dt_dose) < 1e-9 for dt_dose in dose_times):
            y_cur[7] += dosing.dose_mg_L

        n_pts = max(int((t1 - t0) / dt) + 1, 5)

        # ── Added tight tolerances for numerical stiffness ──
        sol = solve_ivp(
            sepsis_odes,
            (t0, t1),
            y_cur,
            args=(params, genes, dosing),
            t_eval=np.linspace(t0, t1, n_pts),
            method="RK45",
            rtol=1e-6,
            atol=1e-9,
        )

        seg_t.append(sol.t)
        seg_y.append(sol.y)
        y_cur = np.maximum(sol.y[:, -1], 0.0)

    return np.concatenate(seg_t), np.concatenate(seg_y, axis=1)


# ═══════════════════════════════════════════════════════════════════════
# 6.  VISUALISATIONS
# ═══════════════════════════════════════════════════════════════════════
PALETTE = {
    "Control (no genes)":          "#2c7bb6",
    "egtB only":                   "#abd9e9",
    "clpK/clpB only":              "#fdae61",
    "bla_1 + IS6 (no Abx)":        "#d7191c",
    "Invasive – no treatment":     "#B71C1C",
    "Invasive + Ceftriaxone":      "#2E7D32",
    "Invasive + Meropenem":        "#00695C",
}
_DASH = {
    k: ("--" if "no" in k.lower() and "abx" not in k.lower() else "-")
    for k in PALETTE
}

def _t_days(t: np.ndarray) -> np.ndarray:
    return t / 24.0

def plot_clinical_summary(results: Dict, t_max_hr: float = 168.0, save_path: str = "Fig1_Clinical_Summary.png") -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for name, (t, y) in results.items():
        c, ls, td = PALETTE.get(name, "gray"), _DASH.get(name, "-"), _t_days(t)
        axes[0, 0].semilogy(td, np.maximum(y[0], 1e-6), color=c, ls=ls, label=name)
        axes[0, 1].plot(td, y[3] + y[4],               color=c, ls=ls, label=name)
        axes[1, 0].plot(td, y[6],                       color=c, ls=ls, label=name)
        axes[1, 1].plot(td, y[8],                       color=c, ls=ls, label=name)

    axes[1, 0].axhline(0.36, color="red", ls=":", lw=1.5, label="Point of No Return ($D = 0.36$)")
    axes[1, 0].axhspan(0.36, 1.5, color="red", alpha=0.05)

    cfg = [
        ("Bacterial Burden",      "B (normalised, log)",       True),
        ("Cytokine Storm",        "IL-6 + TNF-α (normalised)", False),
        ("Active Tissue DAMPs",   "Damage Index ($D$)",         False),
        ("Plasma Antibiotics",    "Concentration (mg/L)",       False),
    ]
    for ax, (ttl, ylab, do_clearance) in zip(axes.flatten(), cfg):
        ax.set_title(ttl, fontweight="bold")
        ax.set_ylabel(ylab)
        ax.set_xlabel("Time (days)")
        ax.set_xlim([0, t_max_hr / 24])
        ax.grid(alpha=0.3, ls=":")
        if do_clearance:
            ax.axhline(1e-3, color="gray", ls=":", lw=1.2, label="Clearance Threshold")

    h0, l0 = axes[0, 0].get_legend_handles_labels()
    hD, lD = axes[1, 0].get_legend_handles_labels()
    extra = [(h, l) for h, l in zip(hD, lD) if l not in l0]
    if extra:
        h_extra, l_extra = zip(*extra)
        fig.legend(list(h0) + list(h_extra), list(l0) + list(l_extra), loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=False)
    else:
        fig.legend(h0, l0, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=False)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.show()

def plot_full_panel(results: Dict, t_max_hr: float = 168.0, save_path: str = "Fig2_Full_State_Variables.png") -> None:
    fig = plt.figure(figsize=(15, 11))
    fig.suptitle("Gram-Negative Sepsis — Full ODE State Variables\nPyseer genes: egtB (β=+0.394) · clpK/clpB operon (β=+0.434) · bla_1 + IS6 transposase (β=+0.350)", fontsize=13, fontweight="bold", y=1.02)
    gs = gridspec.GridSpec(3, 3, hspace=0.42, wspace=0.32)
    axes = [fig.add_subplot(gs[r, c]) for r in range(3) for c in range(3)]

    _META = [
        ("Bacterial Load (B)",         "B (normalised)"),
        ("Neutrophil Activity",        "Fold vs. resting"),
        ("Macrophage Activity",        "Fold vs. resting"),
        ("IL-6 (pro-inflammatory)",    "Normalised conc."),
        ("TNF-α (pro-inflammatory)",   "Normalised conc."),
        ("IL-10 (anti-inflammatory)",  "Normalised conc."),
        ("Tissue Damage / DAMP",       "Damage index"),
        ("Antibiotic – Depot",         "mg/L"),
        ("Antibiotic – Plasma",        "mg/L"),
    ]

    for i, (ax, (var, ylabel)) in enumerate(zip(axes, _META)):
        for name, (t, y) in results.items():
            ax.plot(_t_days(t), y[i], color=PALETTE.get(name, "gray"), ls=_DASH.get(name, "-"), label=name)
        ax.set_title(var, fontsize=10, fontweight="bold")
        ax.set_xlabel("Time (days)", fontsize=9)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.set_xlim([0, t_max_hr / 24])
        ax.grid(alpha=0.2)
        if i == 0: ax.axhline(0.001, color="gray", ls=":", lw=1.2, label="Clearance threshold")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.05), frameon=False)
    plt.savefig(save_path, bbox_inches="tight")
    plt.show()

def plot_phase_portrait(results: Dict, save_path: str = "Fig3_Phase_Portrait.png") -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    for name, (t, y) in results.items():
        if "Invasive" not in name and "Control" not in name: continue
        c, ls = PALETTE.get(name, "gray"), _DASH.get(name, "-")
        ax.plot(y[0], y[6], color=c, ls=ls, label=name)
        ax.scatter(y[0, 0],  y[6, 0],  color=c, marker="o", s=50, zorder=5)
        ax.scatter(y[0, -1], y[6, -1], color=c, marker="*", s=150, zorder=5, edgecolor="black")

    ax.axhline(0.36, color="red", ls=":", lw=1.5, alpha=0.5)
    ax.text(0.02, 0.37, "Sepsis Threshold (Irreversible Cascade)", color="red", fontsize=8, fontweight="bold", alpha=0.7)
    ax.set_title("System Attractors: Infection Trajectory", fontweight="bold")
    ax.set_xlabel("Bacterial Load ($B$)")
    ax.set_ylabel("Active Tissue Damage ($D$)")
    ax.grid(alpha=0.3, ls=":")
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.show()

def plot_lollipop_contributions(results: Dict, save_path: str = "Fig4_Gene_Lollipop.png") -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Individual Gene Contributions to Invasive Severity", fontsize=12, fontweight="bold")
    metric_labels = ["Peak Bacteria ($B_{max}$)", "Peak Cytokines (IL-6 + TNF-α)", "Peak Tissue Damage ($D_{max}$)"]
    names   = list(results.keys())
    metrics = np.array([[y[0].max(), (y[3] + y[4]).max(), y[6].max()] for (_, (_, y)) in results.items()])
    colors = [PALETTE.get(n, "gray") for n in names]

    for j, (ax, label) in enumerate(zip(axes, metric_labels)):
        ax.hlines(y=names, xmin=0, xmax=metrics[:, j], color=colors, alpha=0.65, linewidth=3.5)
        ax.scatter(metrics[:, j], names, color=colors, s=110, zorder=3, edgecolor="white", linewidths=0.8)
        ax.set_xlabel(label, fontweight="bold")
        ax.grid(axis="x", alpha=0.3, ls=":")
        for i_row, val in enumerate(metrics[:, j]):
            ax.text(val + max(val * 0.02, 0.002), i_row, f"{val:.3f}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.show()

def plot_individual_panels(results: Dict, t_max_hr: float = 168.0, prefix: str = "Fig_Individual_") -> None:
    _META = [
        ("Bacterial Load",             "B (normalised)", True),
        ("Neutrophil Activity",        "Fold vs. resting", False),
        ("Macrophage Activity",        "Fold vs. resting", False),
        ("IL-6 (pro-inflammatory)",    "Normalised conc.", False),
        ("TNF-α (pro-inflammatory)",   "Normalised conc.", False),
        ("IL-10 (anti-inflammatory)",  "Normalised conc.", False),
        ("Tissue Damage (DAMP)",       "Damage index", False),
        ("Antibiotic Plasma",          "mg/L", False),
    ]

    import os
    os.makedirs("individual_graphs", exist_ok=True)

    for i, (var, ylabel, log_scale) in enumerate(_META):
        # Index mapping to match original ODE array output, omitting Depot (idx 7) which is less relevant for publication
        idx = i if i < 7 else 8
        fig, ax = plt.subplots(figsize=(6, 4))
        for name, (t, y) in results.items():
            if log_scale:
                ax.semilogy(_t_days(t), np.maximum(y[idx], 1e-6), color=PALETTE.get(name, "gray"), ls=_DASH.get(name, "-"), label=name)
            else:
                ax.plot(_t_days(t), y[idx], color=PALETTE.get(name, "gray"), ls=_DASH.get(name, "-"), label=name)
        
        ax.set_title(var, fontsize=12, fontweight="bold")
        ax.set_xlabel("Time (days)", fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_xlim([0, t_max_hr / 24])
        ax.grid(alpha=0.2)
        
        if log_scale: ax.axhline(1e-3, color="gray", ls=":", lw=1.2, label="Clearance threshold")
        if "Damage" in var: ax.axhline(0.36, color="red", ls=":", lw=1.5, label="Point of No Return")

        ax.legend(loc="best", frameon=False, fontsize=8)
        
        safe_name = var.replace(" ", "_").replace("/", "").replace("α", "alpha").replace("–", "").replace("(", "").replace(")", "")
        plt.tight_layout()
        plt.savefig(f"individual_graphs/{prefix}{i+1}_{safe_name}.png", bbox_inches="tight", dpi=300)
        plt.close(fig)

def plot_individual_lollipops(results: Dict, prefix: str = "Fig_Individual_Lollipop_") -> None:
    metric_labels = ["Peak Bacteria (B_max)", "Peak Cytokines (IL-6 + TNF-alpha)", "Peak Tissue Damage (D_max)"]
    names   = list(results.keys())
    metrics = np.array([[y[0].max(), (y[3] + y[4]).max(), y[6].max()] for (_, (_, y)) in results.items()])
    colors = [PALETTE.get(n, "gray") for n in names]

    import os
    os.makedirs("individual_graphs", exist_ok=True)

    for j, label in enumerate(metric_labels):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hlines(y=names, xmin=0, xmax=metrics[:, j], color=colors, alpha=0.65, linewidth=3.5)
        ax.scatter(metrics[:, j], names, color=colors, s=110, zorder=3, edgecolor="white", linewidths=0.8)
        ax.set_xlabel(label, fontweight="bold")
        ax.grid(axis="x", alpha=0.3, ls=":")
        for i_row, val in enumerate(metrics[:, j]):
            ax.text(val + max(val * 0.02, 0.002), i_row, f"{val:.3f}", va="center", fontsize=9)
            
        safe_name = label.replace(" ", "_").replace("(", "").replace(")", "").replace("+", "plus").replace("-", "")
        plt.tight_layout()
        plt.savefig(f"individual_graphs/{prefix}{j+1}_{safe_name}.png", bbox_inches="tight", dpi=300)
        plt.close(fig)

def print_outcome_table(results: Dict) -> None:
    print("\n" + "═" * 95)
    print("  SIMULATION OUTCOME SUMMARY")
    print("  Clearance threshold: B < 0.001  |  Sepsis threshold: D > 0.36")
    print("═" * 95)
    hdr = (f"  {'Scenario':<42}  {'Peak B':>7}  {'Final B':>7}  "
           f"{'Outcome':>11}  {'Peak IL-6':>9}  {'Peak D':>8}  {'Sepsis':>6}")
    print(hdr)
    print("─" * 95)
    for name, (t, y) in results.items():
        Bp   = y[0].max()
        Bf   = y[0, -1]
        pIL6 = y[3].max()
        pD   = y[6].max()
        out  = "✓ CLEARED" if Bf < 0.001 else f"✗ {Bf:.4f}"
        sep  = "YES" if pD > 0.36 else "no"
        print(f"  {name:<42}  {Bp:>7.3f}  {Bf:>7.4f}  "
              f"{out:>11}  {pIL6:>9.3f}  {pD:>8.3f}  {sep:>6}")
    print("═" * 95)


if __name__ == "__main__":
    T_MAX = 168.0

    treatment_scenarios = {
        "Control (no genes)":      (genes_control(),  None),
        "Invasive – no treatment": (genes_invasive(), None),
        "Invasive + Ceftriaxone":  (genes_invasive(), ceftriaxone()),
        "Invasive + Meropenem":    (genes_invasive(), meropenem()),
    }

    gene_scenarios = {
        "Control (no genes)":      (genes_control(),    None),
        "egtB only":               (genes_egtB_only(),  None),
        "clpK/clpB only":          (genes_clpKB_only(), None),
        "bla_1 + IS6 (no Abx)":    (genes_bla_IS6(),    None),
        "Invasive – no treatment": (genes_invasive(),   None),
    }

    results_tx = {}
    results_gene = {}

    for name, (g, d) in treatment_scenarios.items():
        results_tx[name] = run_simulation(genes=g, dosing=d, t_max_hr=T_MAX)

    for name, (g, d) in gene_scenarios.items():
        results_gene[name] = run_simulation(genes=g, dosing=d, t_max_hr=T_MAX)

    print("Simulations complete! Data is now saved in memory for other cells to use.")

    # Print the outcome tables
    print_outcome_table(results_tx)
    print_outcome_table(results_gene)

    # Generate the main visualization suite
    plot_clinical_summary(results_tx)
    plot_full_panel(results_tx)
    plot_lollipop_contributions(results_gene)
    
    # Generate separated high-res graphs for the paper
    print("Generating separated high-res individual graphs...")
    plot_individual_panels(results_tx)
    plot_individual_lollipops(results_gene)
    print("Individual graphs saved in the 'individual_graphs' folder!")

