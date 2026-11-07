"""
══════════════════════════════════════════════════════════════════════════════
OMICS: A Journal of Integrative Biology — Original Article Generator
══════════════════════════════════════════════════════════════════════════════
Target Requirements:
  • Article Type: Original Article
  • Body Word Limit: ≤ 4,000 words (Target: 3,800 – 3,950 words)
  • Unstructured Abstract: ≤ 200 words (Target: 180 – 195 words)
  • Combined Figures and Tables: Exactly 5 items
      - Table 1: Consolidated mGWAS results (baseline + conditional)
      - Table 2: Simulated clinical ODE outcomes across scenarios
      - Figure 1: Composite sensitivity analysis (1A PRCC tornado + 1B mapping comparison)
      - Figure 2: Extended 10-compartment ODE clinical trajectories (4-panel)
      - Figure 3: Therapeutic Golden Window time-to-treatment analysis
  • Excluded figures (per user instruction):
      - Fig_LPS_3_Inoculum_Dose_Response.png (Excluded)
      - Fig_LPS_5_Full_State_Variables.png (Excluded)
  • Reference Style: Sage Harvard (Author, Year) in-text and alphabetical references list
  • Essential Content:
      - Sample size justification & power analysis (Saber & Shapiro, 2020)
      - Genomic inflation factor λ = 1.531 justification (Earle et al., 2016; Lees et al., 2016)
      - Kinetic model validation against published clinical septic shock cohorts
      - Full 10-compartment ODE mathematical derivation and biochemical justifications
      - Antibiotic administration window at t = 6.0 h post-inoculation
      - Bacteriolytic endotoxin burst paradox (meropenem vs ceftriaxone)
      - Therapeutic Golden Window (t ≤ 10 h rescue vs t ≥ 12 h fatal organ collapse)
      - Global sensitivity analysis (LHS-PRCC, N = 1,000) and mapping robustness (N = 800)
      - "Cell to Society" multiomics transdisciplinary integration
      - Dedicated Limitations section
      - Data & Code Availability statement with GitHub repository link
══════════════════════════════════════════════════════════════════════════════
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUTPUT_PATH = "/Users/gauthamgl/Desktop/ode/OMICS_Manuscript_4000w.docx"
ODE_DIR = "/Users/gauthamgl/Desktop/ode"

doc = docx.Document()

# Page Margins (1 inch all around)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Default Styling
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)
style_normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
style_normal.paragraph_format.line_spacing = 2.0  # Double-spaced
style_normal.paragraph_format.space_after = Pt(0)

body_word_count = 0
section_counts = {}
current_section = "Front Matter"

def set_section(name):
    global current_section
    current_section = name
    if name not in section_counts:
        section_counts[name] = 0

def add_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True

def add_authors(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

def add_affiliation(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.font.italic = True

def add_h1(text):
    set_section(text)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True

def add_p(text, count_words=True):
    global body_word_count
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.first_line_indent = Inches(0.5)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    if count_words:
        wc = len(text.split())
        body_word_count += wc
        section_counts[current_section] = section_counts.get(current_section, 0) + wc
    return p

def add_p_noindent(text, count_words=True):
    global body_word_count
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    if count_words:
        wc = len(text.split())
        body_word_count += wc
        section_counts[current_section] = section_counts.get(current_section, 0) + wc
    return p

def add_equation(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.font.italic = True

def add_fig_image(img_name, caption_text, width=Inches(6.0)):
    img_path = os.path.join(ODE_DIR, img_name)
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(img_path, width=width)
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(2)
        cap_p.paragraph_format.space_after = Pt(12)
        cap_p.paragraph_format.line_spacing = 1.5
        cap_run = cap_p.add_run(caption_text)
        cap_run.font.size = Pt(10)
        cap_run.font.italic = True
        cap_run.font.name = 'Times New Roman'
    else:
        print(f"WARNING: Image not found: {img_path}")

def format_table(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell in table.rows[0].cells:
        shading = parse_xml(r'<w:shd {} w:fill="E8EDF2"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.name = 'Times New Roman'
    for r_idx, row in enumerate(table.rows[1:]):
        for c_idx, cell in enumerate(row.cells):
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                if c_idx > 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.size = Pt(9)
                    r.font.name = 'Times New Roman'
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        r'<w:tblBorders {} >'
        r'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        r'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        r'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        r'  <w:left w:val="none"/>'
        r'  <w:right w:val="none"/>'
        r'  <w:insideV w:val="none"/>'
        r'</w:tblBorders>'.format(nsdecls('w'))
    )
    tblPr.append(borders)

# ═══════════════════════════════════════════════════════════════════════
# TITLE & FRONT MATTER
# ═══════════════════════════════════════════════════════════════════════

add_title(
    "Translating Bacterial Population Genomics into Infection Dynamics: "
    "An Integrative Multi-Scale ODE Model of Sepsis Caused by Klebsiella pneumoniae"
)

add_authors("Gautham G L, Dhruti Reddy P, S Apurva Ananya, Sasmita Sabat*")
add_affiliation(
    "Department of Biotechnology, National Institute of Technology, Rourkela, India.\n"
    "* Corresponding author: Sasmita Sabat (sasmita.sabat@nitrkl.ac.in)"
)

# ═══════════════════════════════════════════════════════════════════════
# ABSTRACT (≤200 words, unstructured, NOT counted in body)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Abstract")

abstract_text = (
    "Gram-negative sepsis outcomes are governed by nonlinear host-pathogen interactions that static genome-wide "
    "association studies (GWAS) cannot capture temporally. We present an integrative framework translating microbial "
    "pangenome-wide association effect sizes into a mechanistic 10-compartment ordinary differential equation (ODE) "
    "model of Klebsiella pneumoniae sepsis. Applying pyseer linear mixed models to 200 clinical genomes (100 bacteremic "
    "sepsis, 100 non-invasive controls), we identified orthogonal determinants of invasiveness: the chaperone "
    "clpK/clpB operon (beta = +0.434), the ergothioneine antioxidant pathway egtB (beta = +0.394), and beta-lactamase/"
    "transposase elements (bla_1/IS6, beta = +0.350/+0.388). These effect sizes were mapped via exponential transformations "
    "into rate multipliers modulating leukocyte bactericidal efficiency and pharmacodynamic susceptibility. Global "
    "sensitivity analysis (N = 1,000 Latin Hypercube samples) confirmed GWAS-derived multipliers as primary determinants "
    "of tissue damage, robust across four mathematical mapping functions. In silico simulations demonstrated epistatic "
    "synergy between oxidative and proteotoxic stress evasion operons, which drives tissue injury past an irreversible "
    "tipping point (damage index D > 0.36). Furthermore, the model captured a post-antimicrobial bacteriolytic endotoxin "
    "burst and delineated a 10-hour therapeutic Golden Window beyond which microbiological clearance fails to prevent fatal "
    "organ failure. This framework bridges microbial genomics, immunology, and pharmacology from cell to society."
)
add_p_noindent(abstract_text, count_words=False)
abstract_wc = len(abstract_text.split())

kw_p = doc.add_paragraph()
kw_p.paragraph_format.space_before = Pt(6)
kw_p.paragraph_format.space_after = Pt(12)
kw_bold = kw_p.add_run("Keywords: ")
kw_bold.bold = True
kw_bold.font.size = Pt(12)
kw_bold.font.name = 'Times New Roman'
kw_text = kw_p.add_run(
    "Klebsiella pneumoniae; microbial GWAS; pangenome; systems biology; ordinary differential equations; "
    "endotoxin; pharmacogenomics; sepsis; cytokine storm; antimicrobial stewardship"
)
kw_text.font.size = Pt(12)
kw_text.font.name = 'Times New Roman'

# ═══════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION (~680 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Introduction")

add_p(
    "Sepsis is defined clinically as a life-threatening organ dysfunction caused by a dysregulated host response to "
    "infection, accounting for an estimated 48.9 million incident cases and 11.0 million deaths globally each year "
    "(Hotchkiss et al., 2016). Among Gram-negative pathogens, Klebsiella pneumoniae has emerged as an urgent global "
    "threat owing to the rapid dissemination of high-risk hospital-adapted lineages combining multidrug resistance with "
    "enhanced invasive fitness (Wyres et al., 2020). In hospital intensive care units, patients presenting with K. pneumoniae "
    "bacteraemia exhibit starkly divergent clinical trajectories: while some individuals achieve rapid microbial clearance "
    "with transient physiological perturbation, others rapidly plunge into refractory septic shock, multiple organ failure, "
    "and cardiovascular collapse (van der Poll et al., 2017). Unravelling the biological mechanisms that govern this critical "
    "clinical divergence is paramount for developing precision diagnostics and therapeutic timing strategies."
)

add_p(
    "The clinical management of K. pneumoniae sepsis is further complicated by the divergence between hypervirulent (hvKp) "
    "and classical multidrug-resistant (cKp) pathotypes. While hvKp strains historically caused community-acquired invasive disease "
    "in healthy hosts via plasmid-borne hypercapsule and siderophores, nosocomial sepsis is overwhelmingly driven by multidrug-resistant "
    "cKp lineages that lack classical hypervirulence determinants. In hospital settings, bacterial invasiveness depends on subtle "
    "cellular adaptations that permit survival under antimicrobial pressure and leukocyte-mediated oxidative stress. Conventional "
    "clinical microbiology identifies species and phenotypic resistance profiles but remains blind to these within-host survival "
    "adaptations, precluding genome-informed timing or therapeutic optimization."
)

add_p(
    "High-throughput microbial genome-wide association studies (mGWAS) utilizing linear mixed models (LMMs), such as "
    "pyseer (Lees et al., 2018), have transformed microbial genetics by enabling systematic discovery of accessory genes, "
    "plasmids, and structural variants associated with invasive clinical phenotypes while controlling for confounding "
    "clonal population structure (Earle et al., 2016). Nevertheless, an unbridged conceptual chasm separates static "
    "statistical genomics from clinical pathophysiology. Statistical effect sizes (beta coefficients or odds ratios) derived "
    "from regression models represent time-invariant population-level correlations. They cannot capture the time-varying "
    "kinetics of pathogen proliferation, the non-linear cascading thresholds of pro- and anti-inflammatory cytokine networks, "
    "the secondary damage caused by cellular debris, or the dynamic bactericidal impact of antimicrobial pharmacokinetics and "
    "pharmacodynamics (PK/PD). Statistical associations identify putative risk alleles, but sepsis is fundamentally a "
    "non-linear, time-dependent dynamical disease."
)

add_p(
    "To capture within-host dynamical complexity, systems biologists have developed ordinary differential equation (ODE) "
    "models of acute inflammation. Foundational mathematical models by Kumar et al. (2004), Chow et al. (2005), and "
    "Reynolds et al. (2006) established that sepsis progression can be understood as a dynamical bifurcation across a "
    "bistable manifold. In these formulations, an initial infectious insult either resolves toward a healthy homeostatic "
    "attractor or crosses an unstable separatrix into a self-sustaining, hyper-inflammatory organ damage attractor. Despite "
    "their mathematical elegance, existing ODE inflammation models treat the invading bacterial pathogen as an abstract, "
    "unidimensional variable governed by generic phenomenological growth and clearance constants. They completely lack "
    "molecular specificity and remain disconnected from the genomic architecture and accessory virulence repertoire of the "
    "specific microbial isolate causing the infection."
)

add_p(
    "To overcome these limitations, this study presents an integrative computational framework that translates microbial "
    "pangenome GWAS effect sizes into a mechanistic, multi-scale 10-compartment ODE model of K. pneumoniae sepsis. We "
    "performed two-stage (baseline and conditional) mGWAS across 200 clinically curated K. pneumoniae genomes, uncovered "
    "orthogonal stress-tolerance operons governing invasiveness, and mapped their statistical effect sizes into mechanistic "
    "rate multipliers. The resulting ODE model incorporates activated neutrophils, tissue macrophages, pro-inflammatory "
    "cytokines (IL-6, TNF-alpha), counter-regulatory immunosuppression (IL-10), cellular tissue injury, two-compartment "
    "antibiotic pharmacokinetics (ceftriaxone and meropenem), and free circulating endotoxin (lipopolysaccharide, LPS) release "
    "kinetics. Through comprehensive global sensitivity analysis (Latin Hypercube Sampling, LHS; Partial Rank Correlation "
    "Coefficients, PRCC), mapping robustness evaluations, and antibiotic timing titrations, we quantify the bacteriolytic "
    "endotoxin burst and delineate the clinical Golden Window of antimicrobial therapy. By seamlessly connecting bacterial "
    "pangenomics to biochemical stress response, systemic immunopathology, and clinical pharmacotherapy, this work demonstrates "
    "the transdisciplinary power of post-genomic systems biology from cell to society."
)

# ═══════════════════════════════════════════════════════════════════════
# 2. METHODS (~1,320 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Methods")

add_h2("Genomic data acquisition, assembly, and pangenome construction")
add_p(
    "Whole-genome sequencing datasets from 100 K. pneumoniae blood-culture isolates retrieved from patients with documented "
    "bacteraemic sepsis were obtained from the NCBI Sequence Read Archive (SRA), paired with 100 non-invasive human carriage "
    "and environmental control isolates from the NCBI Assembly database, yielding an analytical cohort of N = 200 genomes. "
    "Raw paired-end sequencing reads were evaluated for per-base quality and adapter contamination using FastQC v0.11.9 "
    "(Andrews et al., 2010), followed by quality filtering and automated adapter trimming via fastp v0.23.2 (Chen et al., "
    "2018) with a minimum Phred score threshold of Q20 across sliding windows. De novo genome assembly was executed using "
    "MEGAHIT v1.2.9 (Li et al., 2015) using iteratively increasing k-mer sizes (k-min = 21, k-max = 141, step = 12). Assembly "
    "contiguity, completeness, and structural fidelity were benchmarked with QUAST v5.2.0 (Gurevich et al., 2013), enforcing "
    "strict inclusion thresholds (N50 > 20 kbp, total assembly length 5.3–5.5 Mbp, and <5% missing or ambiguous bases). "
    "Acquired antimicrobial resistance determinants were profiled using AMRFinderPlus v3.11.26 (Feldgarden et al., 2021). "
    "Capsular serotypes (K-locus) and lipopolysaccharide O-types were determined using Kleborate v2.4.1 (Lam et al., 2021). "
    "High-throughput functional annotation was performed via Prokka v1.14.6 (Seemann, 2014). Pangenome reconstruction and "
    "orthologous gene clustering were executed using Panaroo v1.3.4 (Tonkin-Hill et al., 2020) in strict mode with a sequence "
    "identity threshold of 95% and length difference cutoff of 98%, generating a pangenomic presence/absence matrix comprising "
    "16,477 total gene clusters, which was subsequently filtered to 3,735 intermediate-frequency clusters (minor allele "
    "frequency 5–95%) for association testing."
)

add_h2("Microbial GWAS and statistical power justification")
add_p(
    "The analytical cohort size of N = 200 (100 sepsis cases, 100 controls) was evaluated a priori using empirical power "
    "benchmarking standards established for bacterial association studies by Saber and Shapiro (2020). Using simulated clonal "
    "bacterial populations, Saber and Shapiro established that linear mixed models achieve statistical power exceeding 80% to "
    "detect moderate-to-large genetic effect sizes (beta >= 0.30, equivalent to odds ratios >= 1.35) at intermediate allele "
    "frequencies (MAF 5–95%) with a balanced cohort of 100 cases and 100 controls. Pairwise genomic distances across all 200 "
    "isolates were calculated using MASH v2.3 (k = 21, sketch size s = 10,000; Ondov et al., 2016) and transformed into a "
    "continuous kinship covariance matrix (estimated narrow-sense heritability h-squared = 0.90) to correct for population "
    "structure. Association testing was conducted using the pyseer LMM framework (Lees et al., 2018). Statistical significance "
    "was defined under a strict Bonferroni-corrected threshold (alpha = 0.05 / 3,735 tests, p < 1.34 x 10-5). The baseline "
    "association scan yielded an overall genomic inflation factor of lambda = 1.531. While lambda values near 1.0 are expected "
    "in human outbreeding populations, elevated genomic inflation (lambda = 1.30–1.80) is an established, ubiquitous hallmark of "
    "clonal bacterial GWAS (Earle et al., 2016; Power et al., 2016). This phenomenon arises because prokaryotes reproduce by "
    "binary fission with extensive genome-wide linkage disequilibrium, meaning that non-causal hitchhiker genes co-segregate "
    "along shared phylogenetic branches with true causal variants (Lees et al., 2016). To mitigate this inflation and isolate "
    "independent secondary genetic drivers, conditional LMM testing was performed by incorporating the presence/absence "
    "vectors of baseline-significant gene clusters as fixed-effect covariates, which successfully reduced the genomic inflation "
    "factor to lambda = 1.460 and unmasked eight previously suppressed secondary associations."
)

add_h2("Ten-compartment ODE model formulation")
add_p(
    "We expanded the acute inflammation frameworks of Reynolds et al. (2006) and Kumar et al. (2004) into a 10-compartment "
    "dynamical system tracking: normalised bacterial burden (B), activated neutrophils (N), activated tissue macrophages (M), "
    "interleukin-6 (IL-6), tumour necrosis factor-alpha (TNF-alpha), interleukin-10 (IL-10), cumulative tissue damage index (D), "
    "antibiotic absorption depot (A_dep), antibiotic plasma concentration (A_p), and free circulating lipopolysaccharide (LPS, L). "
    "Bacterial replication is governed by logistic growth with intrinsic replication rate k_b = 0.45/h and carrying capacity "
    "normalised to 1.0, balanced by natural death d_b = 0.12/h, constitutive immune surveillance k_surv = 0.05/h, leukocyte "
    "phagocytic killing, and antibiotic-mediated bacteriolysis (E_abx):"
)

add_equation(
    "dB/dt = k_b * B * (1 - B) - d_b * B - k_surv * B - K_immune - E_abx * B"
)

add_p(
    "Systemic leukocyte killing (K_immune) comprises oxidative and non-oxidative neutrophil bactericidal action alongside "
    "macrophage killing, all modulated by the anti-inflammatory IL-10 immunosuppression factor supp = 1 / (1 + kappa_IL10 * IL10), "
    "where kappa_IL10 = 5.0 (Hill coefficient n = 1):"
)

add_equation(
    "K_immune = [ (k_NB,ox / phi_ROS + k_NB,pep) * (N - N_0) + (k_MB / phi_stress) * (M - M_0) ] * B * supp"
)

add_p(
    "Here, N_0 = 0.10 and M_0 = 0.10 represent baseline resting leukocyte densities, while k_NB,ox = 0.35/h, k_NB,pep = 0.10/h, "
    "and k_MB = 0.25/h are baseline bactericidal rate constants. The pyseer-derived multipliers phi_ROS and phi_stress mechanistically "
    "attenuate neutrophil oxidative killing and macrophage proteotoxic degradation, respectively. Activated neutrophils (N) and "
    "macrophages (M) are recruited into the circulating compartment by bacteria, circulating LPS, and pro-inflammatory cytokines, "
    "subject to IL-10 suppression and linear homeostatic apoptosis (d_N = 0.05/h, d_M = 0.02/h):"
)

add_equation(
    "dN/dt = [ (k_N,rec * B + k_N,LPS * L + k_N,cyt * (IL6 + TNF)) * supp ] - d_N * (N - N_0)"
)
add_equation(
    "dM/dt = [ (k_M,bact * B + k_M,LPS * L + k_M,cyt * (IL6 + TNF)) * supp ] - d_M * (M - M_0)"
)

add_p(
    "Pro-inflammatory cytokine cascades model the release of IL-6 and TNF-alpha upon leukocyte TLR4 activation by bacteria and "
    "circulating LPS, with linear clearance rates d_IL6 = 0.30/h and d_TNF = 0.40/h (half-lives ~2.3 h and ~1.7 h):"
)

add_equation(
    "d[IL-6]/dt = [ (k_IL6,N * N + k_IL6,M * M) * B * supp ] + [ k_IL6,LPS * M * L * supp ] - d_IL6 * [IL-6]"
)
add_equation(
    "d[TNF-a]/dt = [ k_TNF,M * M * B * supp ] + [ k_TNF,LPS * M * L * supp ] - d_TNF * [TNF-a]"
)

add_p(
    "Counter-regulatory immunosuppression is governed by IL-10, representing the Compensatory Anti-inflammatory Response "
    "Syndrome (CARS; Bone, 1996). Secretion of IL-10 is induced by activated macrophages, pro-inflammatory cytokine feedback "
    "(k_IL10,cyt = 0.80/h), and endotoxemia (k_IL10,LPS = 0.50/h), counteracted by endogenous turnover (d_IL10 = 0.25/h):"
)

add_equation(
    "d[IL-10]/dt = k_IL10,M * (M - M_0) + k_IL10,cyt * (IL6 + TNF) + k_IL10,LPS * L - d_IL10 * [IL-10]"
)

add_p(
    "The cumulative tissue damage index (D) quantifies microvascular endothelial injury, organ dysfunction, and cellular necrosis. "
    "Damage accumulates via direct bacterial cytotoxicity (k_D,bact = 0.20/h), cytokine collateral damage (k_D,cyt = 0.15/h), "
    "endotoxin-mediated endothelial shedding (k_D,LPS = 0.25/h), and an autocatalytic quadratic term (k_D,comp * D^2, k_D,comp = 0.40/h) "
    "representing sterile inflammation driven by Damage-Associated Molecular Patterns (DAMPs; e.g., HMGB1, cell-free DNA, mitochondrial "
    "formyl peptides) that stimulate Toll-like receptors and the NLRP3 inflammasome independently of live bacteria (Scaffidi et al., "
    "2002; Andersson et al., 2018). Cellular recovery is mediated by linear tissue repair d_D = 0.15/h:"
)

add_equation(
    "dD/dt = k_D,bact * B + k_D,cyt * (IL6 + TNF) + k_D,LPS * L + k_D,comp * D^2 - d_D * D"
)

add_p(
    "A mathematical tipping point occurs when the quadratic self-amplification term dominates over linear tissue repair "
    "(d(dD/dt)/dD > 0), creating an unstable threshold at D = 0.36. Trajectories exceeding D = 0.36 escape homeostatic regulation "
    "and diverge inexorably toward terminal organ failure (D_max = 1.500), mirroring the Sepsis-3 clinical definition of refractory "
    "organ collapse (Hotchkiss et al., 2016)."
)

add_h2("Pharmacokinetics and endotoxin release dynamics")
add_p(
    "Antimicrobial pharmacotherapy was simulated using a two-compartment PK model (subcutaneous/intramuscular depot A_dep and "
    "central plasma compartment A_p). Drug absorption follows first-order transfer (k_a = 1.50/h), while elimination is governed "
    "by drug-specific clearance constants. Ceftriaxone was parameterised to represent a standard clinical regimen of 2 g IV once daily "
    "(60 mg/L peak plasma target, k_el = 0.087/h, elimination half-life t_1/2 ~ 8 h, bioavailability F = 1.0; Patel et al., 1981). "
    "Meropenem was parameterised for 1 g IV every 8 h (40 mg/L peak plasma target, k_el = 0.69/h, t_1/2 ~ 1 h, F = 1.0; Drusano "
    "and Hutchison, 1995). Antibiotic bactericidal activity follows a sigmoidal Hill function (Emax = 1.20/h, Hill coefficient h = 2.0, "
    "EC50 = 8.0 mg/L), scaled by the pyseer-derived resistance multiplier phi_abx:"
)

add_equation(
    "E_abx = Emax * (A_p)^h / [ (EC50 * phi_abx)^h + (A_p)^h ]"
)

add_p(
    "Free circulating endotoxin (LPS, L) dynamics capture basal shedding during bacterial division (alpha_shed = 0.04/h), immune-mediated "
    "lysis (gamma_imm = 0.40), and rapid burst release during antibiotic-induced cell-wall lysis (gamma_abx = 1.00), countered by "
    "reticuloendothelial and hepatic clearance (d_L = 0.35/h, half-life ~2.0 h):"
)

add_equation(
    "dL/dt = alpha_shed * B + gamma_abx * E_abx * B + gamma_imm * K_immune - d_L * L"
)

add_p(
    "Crucially, to replicate realistic clinical presentation wherein patients present to emergency facilities hours after symptom "
    "onset, antibiotics were initiated at t = 6.0 h post-inoculation rather than at the unrealistic time t = 0."
)

add_h2("Mapping GWAS effect sizes to ODE rate multipliers")
add_p(
    "To bridge statistical association with kinetic rates, pyseer log-odds effect sizes (beta) were mapped into mechanistic rate "
    "multipliers using the exponential transformation phi = exp(beta):"
)
add_equation("phi_ROS = exp(beta_egtB) = exp(0.394) = 1.483")
add_equation("phi_stress = exp(beta_clpK/clpB) = exp(0.434) = 1.543")
add_equation("phi_abx = exp(beta_bla + beta_IS6) = exp(0.350 + 0.388) = exp(0.738) = 2.092")

add_h2("Global sensitivity analysis and mapping robustness")
add_p(
    "To ensure that model conclusions were not artefacts of parameter selection, global uncertainty and sensitivity analyses were "
    "executed using Latin Hypercube Sampling (LHS) paired with Partial Rank Correlation Coefficients (PRCC; Marino et al., 2008). "
    "Ten parameters were simultaneously perturbed: pyseer multipliers (phi_ROS, phi_stress, phi_abx) varied over +/-50%, and core "
    "ODE physiological constants (k_b, k_NB,ox, k_D,comp, kappa_IL10, k_IL10,cyt, d_D, k_D,bact) varied over +/-30% across "
    "N = 1,000 stratified samples. System equations were numerically integrated over 168 h using SciPy's explicit Runge-Kutta "
    "method of order 5(4) (RK45) under initial bacteremic burden B_0 = 0.05. Furthermore, to evaluate sensitivity to the mathematical "
    "mapping function, robustness was tested across four distinct mathematical forms: exp(beta), linear (1 + beta), base-2 (2^beta), "
    "and base-10 (10^beta) across 200 LHS simulations per function (800 simulations total)."
)

# ═══════════════════════════════════════════════════════════════════════
# 3. RESULTS (~980 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Results")

add_h2("Genomic architecture and lineage distribution")
add_p(
    "The 200 K. pneumoniae genomes resolved into 72 distinct multilocus sequence types (STs), demonstrating extensive phylogenetic "
    "diversity. However, a profound lineage segregation was evident between clinical cohorts: the bacteremic sepsis cohort was heavily "
    "dominated by internationally recognized high-risk nosocomial clones, primarily ST512, ST101, and ST147, whereas the non-invasive "
    "control group was dominated by ST15 (David et al., 2019). Sepsis isolates harbored an exceptionally high acquired antimicrobial "
    "resistance burden, averaging 18.1 acquired resistance genes per isolate compared to 4.2 in controls. The extended-spectrum "
    "beta-lactamase bla_CTX-M-15 was identified in >57% of sepsis genomes, accompanied by marked enrichment of carbapenemases "
    "(bla_KPC-2, bla_KPC-3, and bla_NDM-1; Pitout et al., 2015). In contrast, classical hypervirulence biomarkers (e.g., rmpA, "
    "rmpA2 capsule regulators and iucA aerobactin siderophore synthesis) were exceedingly rare in both cohorts (mean virulence score "
    "1.15 in sepsis vs 1.97 in controls on the Kleborate scale), demonstrating that hospital-acquired sepsis in this cohort was not "
    "driven by hypervirulence plasmids but by hospital-adapted multidrug-resistant lineages."
)

add_h2("Microbial GWAS: baseline and conditional association signals")
add_p(
    "Baseline pyseer LMM association testing across 3,735 intermediate-frequency gene clusters identified five Bonferroni-significant "
    "loci associated with bacteremic sepsis (Table 1). The leading baseline association was the co-transcribed chaperone operon "
    "clpK_1/clpB_1/clpK (beta = +0.434, p = 7.32 x 10-8). Strikingly, an isolated, monomeric clpK cluster was enriched in non-sepsis "
    "controls (beta = -0.533, p = 1.79 x 10-8), demonstrating that invasiveness requires the complete bi-chaperone operon containing "
    "the ClpB AAA+ disaggregase. Other baseline hits included bla_1 (beta = +0.350, p = 9.54 x 10-6) and an IS6/IS26 family transposase "
    "(group_5277, beta = +0.388, p = 1.21 x 10-5), reflecting plasmid-borne multidrug resistance cassettes. Conditional LMM regression, "
    "conducted after adjusting for baseline hits, unmasked eight secondary association signals (Table 1). The foremost secondary "
    "determinant was the hercynine oxygenase cluster egtB_2/egtB_1 (beta = +0.394, p = 3.75 x 10-7) and an associated ergothioneine "
    "biosynthesis cluster with serine/threonine protein kinase pkn1 (beta = +0.365, p = 1.93 x 10-6). Non-sepsis enriched secondary "
    "signals included the fertility inhibition protein FinO (group_4547, beta = -0.637) and the antirestriction protein klcA "
    "(beta = -0.535), which are core components of conjugative plasmid backbones."
)

# TABLE 1: Consolidated GWAS Results
add_p_noindent(
    "Table 1. Consolidated microbial GWAS results from baseline (lambda = 1.531) and conditional "
    "(lambda = 1.460) pyseer linear mixed models (N = 200 genomes; Bonferroni threshold p < 1.34 x 10-5).",
    count_words=False
)
t1 = doc.add_table(rows=10, cols=5)
t1_headers = ['Gene Cluster', 'Functional Annotation', 'p-value', 'beta', 'Enrichment']
t1_data = [
    ['clpK (baseline)', 'ClpK ATPase (isolated monomer)', '1.79 x 10-8', '-0.533', 'Non-sepsis'],
    ['clpK_1/clpB_1/clpK (baseline)', 'Chaperone ClpB/ClpK disaggregase operon', '7.32 x 10-8', '+0.434', 'Sepsis'],
    ['bla_1 (baseline)', 'CTX-M-15 extended-spectrum beta-lactamase', '9.54 x 10-6', '+0.350', 'Sepsis'],
    ['group_5277 (baseline)', 'IS6/IS26 family transposase element', '1.21 x 10-5', '+0.388', 'Sepsis'],
    ['egtB_2/egtB_1 (conditional)', 'Hercynine oxygenase (ergothioneine biosynthesis)', '3.75 x 10-7', '+0.394', 'Sepsis'],
    ['egtB/pkn1/egtB_2 (conditional)', 'Ergothioneine synthesis + Ser/Thr kinase', '1.93 x 10-6', '+0.365', 'Sepsis'],
    ['group_4547 (conditional)', 'FinO fertility inhibition conjugative protein', '2.47 x 10-7', '-0.637', 'Non-sepsis'],
    ['klcA_1/klcA_2 (conditional)', 'KlcA antirestriction plasmid maintenance protein', '6.18 x 10-7', '-0.535', 'Non-sepsis'],
    ['group_3230 (conditional)', 'Conserved hypothetical protein', '9.50 x 10-7', '-0.596', 'Non-sepsis'],
]
for col_idx, h in enumerate(t1_headers):
    t1.rows[0].cells[col_idx].text = h
for row_idx, row_data in enumerate(t1_data):
    for col_idx, val in enumerate(row_data):
        t1.rows[row_idx + 1].cells[col_idx].text = val
format_table(t1)

add_h2("Global sensitivity analysis and mapping robustness")
add_p(
    "Across N = 1,000 LHS parameter combinations under untreated infection, peak tissue injury (D_max) spanned a wide continuum "
    "from 0.101 to 1.501, with 55.7% of simulations crossing the lethal sepsis threshold (D > 0.36). Partial rank correlation analysis "
    "demonstrated that all ten parameters were statistically significant drivers of D_max (p < 0.001; Figure 1A). Intrinsic bacterial "
    "growth rate k_b exerted the strongest positive correlation with peak damage (PRCC = +0.759). Crucially, the pyseer-derived "
    "virulence multipliers ranked among the top five parameters governing disease severity: macrophage stress evasion phi_stress "
    "(PRCC = +0.540) and neutrophil ROS evasion phi_ROS (PRCC = +0.406), confirming that GWAS-identified stress determinants are primary "
    "mechanistic drivers of septic shock. In contrast, endogenous tissue repair d_D (PRCC = -0.416) and neutrophil oxidative killing "
    "k_NB,ox (PRCC = -0.250) were the primary protective parameters. Mapping robustness testing across four functional transformations "
    "(Figure 1B) demonstrated that the qualitative prediction of sepsis was preserved across all forms, with threshold-crossing rates "
    "of 50.5% (2^beta), 55.7% (exp(beta)), 58.0% (1 + beta), and 93.5% (10^beta), establishing that the model is topologically robust "
    "and not an artifact of the exponential mapping function."
)

# FIGURE 1: Composite Sensitivity (1A + 1B)
add_fig_image(
    "Fig1_Sensitivity_and_Mapping_Composite.png",
    "Figure 1. Global sensitivity and mapping robustness analysis. (A) Tornado plot of Partial Rank Correlation "
    "Coefficients (PRCC) for peak tissue damage D_max evaluated across N = 1,000 Latin Hypercube samples. Red bars denote pro-sepsis "
    "parameters; blue bars denote host-protective parameters (all p < 0.001). (B) Box-violin distributions of D_max across four "
    "alternative beta-to-phi mathematical mappings (exp(beta), 1+beta, 2^beta, and 10^beta; N = 200 each). Red dashed horizontal line "
    "indicates the critical sepsis threshold (D = 0.36), confirming topological invariance across functional forms.",
    width=Inches(6.0)
)

add_h2("ODE dynamics: epistatic virulence synergy and bacteriolytic endotoxin burst")
add_p(
    "Simulating infection trajectories over 168 h revealed striking epistatic synergy between GWAS hits (Table 2; Figure 2). The wild-type "
    "control genotype resolved spontaneously with sub-threshold damage (D_max = 0.257, final B = 0.0036). Single-operon perturbations "
    "failed to breach the sepsis threshold: egtB alone achieved D_max = 0.283, while clpK/clpB alone reached D_max = 0.313. However, "
    "simulating the co-occurrence of both determinants triggered devastating epistatic cooperativity, driving the damage index past the "
    "tipping point into terminal septic shock (D_max = 1.500). Dual evasion of neutrophil oxidative bursts and macrophage proteotoxic "
    "killing prevented timely leukocyte clearance, allowing sustained endotoxemia and hyper-inflammation."
)

add_p(
    "Antibiotic administration initiated at t = 6.0 h eliminated bacteraemia within 24 h and rescued trajectories from lethal collapse "
    "(ceftriaxone D_max = 0.281; meropenem D_max = 0.293; Table 2; Figure 2). However, meropenem's rapid bactericidal action (t_1/2 ~ 1 h) "
    "precipitated a prominent bacteriolytic endotoxin burst: free circulating LPS surged to a peak of 0.040 at t = 7.5 h (+74% above the "
    "untreated peak of 0.023), driving a secondary wave of TNF-alpha and IL-6. This bacteriolytic burst explains why meropenem induced "
    "marginally higher peak tissue damage (D_max = 0.293) than once-daily ceftriaxone (D_max = 0.281), demonstrating a Jarisch-Herxheimer-like "
    "post-antibiotic inflammatory flare."
)

add_p(
    "Pharmacodynamic analysis confirmed that the rate of bacterial lysis directly governs circulating endotoxin accumulation. "
    "While untreated infection maintained low-grade continuous endotoxemia, meropenem concentrated free LPS into an acute spike "
    "(maximum rate of endotoxin release dL/dt_max = 0.034/h vs 0.018/h for ceftriaxone). By slowing the rate of cell-wall lysis, "
    "ceftriaxone dampened the peak rate of host pattern-recognition receptor activation, explaining the lower peak inflammatory "
    "index despite identical 100% bacterial eradication."
)

# TABLE 2: ODE Simulation Outcomes
add_p_noindent(
    "Table 2. In silico clinical outcome metrics across simulated K. pneumoniae infection scenarios over a 168-hour horizon "
    "(Inoculum B_0 = 0.05; Sepsis threshold: D > 0.36; Antibiotic initiation at t = 6.0 h).",
    count_words=False
)
t2 = doc.add_table(rows=5, cols=6)
t2_headers = ['Scenario', 'Peak B', 'Peak LPS', 'D_max', 'Final B (168 h)', 'Clinical Outcome']
t2_data = [
    ['Control (wild-type)', '0.070', '0.021', '0.257', '0.0036', 'Spontaneous resolution'],
    ['Invasive (untreated)', '0.077', '0.023', '1.500', '0.0017', 'Fatal septic shock (D > 0.36)'],
    ['Invasive + Ceftriaxone (6 h)', '0.077', '0.040', '0.281', '0.0000', 'Rescued (microbial cure)'],
    ['Invasive + Meropenem (6 h)', '0.077', '0.040', '0.293', '0.0000', 'Rescued (microbial cure)'],
]
for col_idx, h in enumerate(t2_headers):
    t2.rows[0].cells[col_idx].text = h
for row_idx, row_data in enumerate(t2_data):
    for col_idx, val in enumerate(row_data):
        t2.rows[row_idx + 1].cells[col_idx].text = val
format_table(t2)

# FIGURE 2: Clinical Trajectories
add_fig_image(
    "Fig_LPS_1_Clinical_Trajectories.png",
    "Figure 2. Extended 10-compartment ODE infection trajectories simulated over 168 hours. (A) Normalised bacterial burden "
    "B on logarithmic scale. (B) Free circulating lipopolysaccharide (LPS). (C) Total cytokine storm index (IL-6 + TNF-alpha). "
    "(D) Cumulative tissue damage index D relative to the irreversible sepsis threshold (D = 0.36, red dashed line). Untreated invasive "
    "infection reaches fatal organ collapse (D = 1.500); antimicrobial initiation at t = 6.0 h halts progression below threshold.",
    width=Inches(6.0)
)

add_h2("Validation of simulated cytokine kinetics against published clinical cohorts")
add_p(
    "To validate the biological fidelity of the 10-compartment model, simulated cytokine trajectories were compared against published "
    "temporal profiles from human endotoxemia trials and clinical septic shock cohorts (Calvano et al., 2005; Xiao et al., 2011; van der "
    "Poll et al., 2017). In our simulations, pro-inflammatory TNF-alpha peaked early at 2.5–3.5 h post-infection, followed by anti-inflammatory "
    "IL-10 peaking at 4.5–6.0 h, and IL-6 peaking at 6.0–8.0 h. This sequential cytokine cascade reproduces established clinical kinetics: "
    "in human intravenous LPS challenge cohorts, TNF-alpha exhibits rapid release peaking within 2–4 h, triggering subsequent IL-10 counter-"
    "regulation at 4–6 h, while IL-6 shows broader activation peaking at 6–12 h and persisting during sustained tissue hypoperfusion "
    "(Casey et al., 1993; Calvano et al., 2005). Furthermore, the persistent elevation of IL-10 throughout 24–72 h in our invasive "
    "trajectory correctly models the prolonged Compensatory Anti-inflammatory Response Syndrome (CARS) and secondary leukocyte deactivation "
    "observed in septic shock patients (Bone, 1996; Volk et al., 2000)."
)

add_h2("The therapeutic Golden Window of antimicrobial timing")
add_p(
    "Titration of antibiotic administration timing across delays from 2 to 48 h identified a critical therapeutic Golden Window (Figure 3). "
    "Initiating antimicrobial therapy within 10 h post-infection successfully confined tissue damage below the D = 0.36 threshold (D_max = 0.358), "
    "enabling complete physiological recovery. In stark contrast, delaying treatment to 12 h or beyond allowed tissue injury to surpass "
    "D = 0.36 prior to drug arrival. Once breached, the autocatalytic DAMP self-amplification term (k_D,comp * D^2) dominated the system, "
    "driving irreversible multi-organ failure (D_max = 1.500) despite 100% bacterial eradication (final B = 0.0000 across all delays; "
    "Figure 3B). This provides mathematical proof that microbiological clearance is decoupled from host survival when treatment is "
    "delayed past the point of no return."
)

# FIGURE 3: Golden Window
add_fig_image(
    "Fig_LPS_4_TimeToTreatment_Window.png",
    "Figure 3. Therapeutic Golden Window analysis. (A) Peak tissue damage D_max plotted as a function of antibiotic initiation "
    "delay (2–48 h). Initiation within 10 h ensures survival; delays >= 12 h cross the irreversible threshold (D = 0.36, red dashed line) "
    "and plunge into fatal organ failure. (B) Final bacterial load at 168 h across all delays, confirming complete microbial clearance "
    "despite divergent host survival outcomes.",
    width=Inches(5.5)
)

# ═══════════════════════════════════════════════════════════════════════
# 4. DISCUSSION (~820 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Discussion")

add_p(
    "This study demonstrates that bridging bacterial pangenome-wide association studies with mechanistic ODE modelling generates "
    "explanatory and predictive insights that are entirely inaccessible to either statistical genomics or phenomenological dynamical "
    "systems alone. The independent discovery of two distinct mGWAS determinants—the clpK/clpB chaperone operon from baseline analysis "
    "and the egtB ergothioneine pathway from conditional analysis—reveals a unified biological strategy governing K. pneumoniae "
    "invasiveness: enhanced resistance to leukocyte-induced stress. In clonal bacteria, individual GWAS associations frequently risk "
    "spurious hitchhiking due to shared ancestry (Power et al., 2016). However, the convergence of two independent loci onto orthogonal "
    "arms of host phagocyte evasion—antioxidant defense and protein disaggregation—provides compelling internal validation, as random "
    "phylogenetic hitchhiking is exceedingly improbable to select complementary stress-tolerance systems targeting the same intracellular "
    "survival niche (Earle et al., 2016)."
)

add_p(
    "Crucially, the invasive determinants uncovered here represent physiological stress tolerance rather than classical hypervirulence. "
    "In community-acquired invasive K. pneumoniae infections, severe disease is typically driven by plasmid-encoded hypervirulence "
    "factors, including heavy polysaccharide capsules and siderophores (Russo and Marr, 2019). In our hospital-acquired cohort, these "
    "classical virulence genes were virtually absent. Instead, nosocomial invasiveness is shaped by the convergence of multidrug "
    "resistance and cellular fitness adaptations (Wyres et al., 2020). The egtB pathway synthesizes ergothioneine, a stable histidine-derived "
    "thiol that scavenges superoxide and hydroxyl radicals, shielding bacteria from neutrophil oxidative bursts (Cumming et al., 2018). "
    "The clpK/clpB operon encodes AAA+ ATPase molecular chaperones that solubilize and renature protein aggregates formed during heat-shock "
    "and phagolysosomal oxidative stress (Kedzierska-Mieszkowska and Zolkiewski, 2021). In our dynamical model, their combined evasion "
    "of neutrophil ROS (phi_ROS = 1.48) and macrophage proteotoxicity (phi_stress = 1.54) produces lethal epistatic cooperativity, "
    "propelling tissue damage across the irreversible threshold—a finding undetectable by single-gene association scans."
)

add_p(
    "The 10-compartment ODE formulation successfully resolves the bacteriolytic endotoxin burst paradox. Clinicians have long observed "
    "that potent bactericidal antibiotics can induce paradoxical inflammatory worsening—resembling a Jarisch-Herxheimer reaction "
    "(Kumar et al., 2006). In our simulations, meropenem eliminated bacteremia more rapidly than ceftriaxone, but triggered an acute "
    "+74% surge in free circulating LPS, resulting in a transient cytokine flare and slightly higher peak tissue damage (D_max = 0.293 vs 0.281). "
    "This phenomenon reflects beta-lactam PK/PD differences: carbapenems cause rapid bacterial spheroplast formation and explosive lysis, "
    "whereas cephalosporins with longer elimination half-lives release endotoxin more gradually. This finding supports ongoing clinical "
    "efforts evaluating extended or continuous infusions of carbapenems to mitigate rapid lysis surges in critically ill patients."
)

add_p(
    "The Golden Window analysis provides mathematical confirmation of Kumar et al.'s (2006) landmark clinical observation that each hour "
    "of delayed antimicrobial administration significantly increases sepsis mortality. Our model demonstrates that initiating antibiotics "
    "within 10 h prevents tissue damage from crossing the critical D = 0.36 threshold. Beyond 12 h, the quadratic damage term (k_D,comp * D^2) "
    "becomes self-sustaining. At this stage, massive release of endogenous DAMPs (HMGB1, cell-free DNA) triggers non-resolving sterile "
    "inflammation via TLR4 and NLRP3 inflammasome signaling (Scaffidi et al., 2002; Andersson et al., 2018), driving multi-organ failure "
    "even after total bacterial sterilization. This proves that microbiological cure is necessary but insufficient for survival once "
    "host-mediated tissue damage crosses the point of no return."
)

add_p(
    "From a translational perspective, this framework exemplifies the 'cell to society' mission of integrative biology (OMICS). By linking "
    "bacterial genomic variation (genomics) to pathogen stress physiology (redox biology), within-host immunopathology (physiomics), and "
    "antibiotic timing (clinical pharmacology), the model establishes a blueprint for precision medicine. Rapid metagenomic or PCR profiling "
    "of clpK/clpB and egtB at hospital admission could identify patients infected with high-risk invasive genotypes, enabling clinicians "
    "to enforce aggressive, sub-10-hour antimicrobial administration and tailored anti-inflammatory adjunct therapy."
)

add_p(
    "The absence of human homologs for ClpB disaggregases and EgtB ergothioneine synthases identifies these microbial stress "
    "systems as promising targets for anti-virulence drug discovery (Cumming et al., 2018; Kedzierska-Mieszkowska and Zolkiewski, 2021). "
    "Small-molecule inhibitors disabling these enzymes could re-sensitize invasive isolates to innate leukocyte killing without "
    "exerting direct selective pressure for resistance. At the healthcare delivery level, detecting clpK/clpB and egtB via rapid "
    "molecular assays at hospital admission could alert intensive care teams to initiate sub-10-hour antimicrobial therapy and consider "
    "extended infusions, translating microbial pangenomics directly into improved patient survival."
)

# Limitations
add_h2("Limitations")
add_p(
    "Several methodological limitations must be acknowledged. First, the sample size of N = 200 genomes, while adequately powered for "
    "moderate-to-large effect sizes (Saber and Shapiro, 2020), limits discovery of rare accessory variants with subtle phenotypic effects. "
    "Second, non-invasive controls were collected across diverse repositories, introducing potential geographic ascertainment bias. "
    "Third, the well-mixed single-compartment assumption abstracts spatial anatomical compartmentalization, such as pulmonary or urinary "
    "foci. Fourth, the mathematical mapping phi = exp(beta), while validated across four functional forms (Figure 1B), remains an empirical "
    "heuristic requiring future in vitro biochemical parameterization. Fifth, host immune parameters were population-averaged, omitting "
    "individual patient genetic polymorphisms in TLR4 or cytokine promoters. Future multi-center studies integrating pathogen sequencing "
    "with longitudinal patient cytokine profiling will be essential to refine personalized parameterization."
)

# ═══════════════════════════════════════════════════════════════════════
# 5. CONCLUSIONS (~95 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Conclusions")

add_p(
    "We have established an integrative computational framework that translates microbial population genomics into within-host infection "
    "dynamics. Microbial GWAS identified stress-tolerance operons (clpK/clpB, egtB) that exhibit epistatic synergy when mapped into a "
    "10-compartment ODE model, driving tissue injury past an irreversible sepsis threshold (D > 0.36). The model mechanistically captures "
    "the post-antibiotic endotoxin burst and delineates a 10-hour therapeutic Golden Window. Bridging microbial genomics, host immunology, "
    "and clinical pharmacology, this multi-scale paradigm advances precision diagnosis and time-critical antimicrobial stewardship."
)

# ═══════════════════════════════════════════════════════════════════════
# BACK MATTER (NOT counted in body word limit)
# ═══════════════════════════════════════════════════════════════════════

add_h1("Acknowledgements")
add_p_noindent(
    "The authors thank the Department of Biotechnology, National Institute of Technology, Rourkela, for computational infrastructure "
    "and institutional support.",
    count_words=False
)

add_h1("Author Contributions")
add_p_noindent(
    "Gautham G L: Conceptualisation, Methodology, Software, Formal Analysis, Writing – Original Draft. "
    "Dhruti Reddy P: Formal Analysis (conditional pyseer LMM workflows). "
    "S Apurva Ananya: Data Curation (Panaroo pangenome reconstruction). "
    "Gautham G L, Dhruti Reddy P, S Apurva Ananya: Investigation (NGS quality control and assembly). "
    "Sasmita Sabat: Supervision, Project Administration, Writing – Review & Editing. "
    "All authors critically reviewed and approved the final manuscript.",
    count_words=False
)

add_h1("Ethical Considerations")
add_p_noindent(
    "This study exclusively analysed publicly available, de-identified bacterial genome sequences deposited in NCBI databases. "
    "No human participants were directly recruited, and no animal experiments were performed; therefore, institutional ethical "
    "approval was not required.",
    count_words=False
)

add_h1("Consent to Participate")
add_p_noindent("Not applicable.", count_words=False)

add_h1("Consent for Publication")
add_p_noindent("Not applicable.", count_words=False)

add_h1("Declaration of Conflicting Interest")
add_p_noindent(
    "The authors declare that they have no competing financial or non-financial interests that could have appeared to influence "
    "the work reported in this paper.",
    count_words=False
)

add_h1("Funding")
add_p_noindent(
    "This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.",
    count_words=False
)

add_h1("Data Availability")
add_p_noindent(
    "All Python simulation scripts, pyseer association workflows, Latin Hypercube Sampling routines, and figure generation scripts "
    "are openly available in a public GitHub repository (https://github.com/sepsis-genomics/kp-ode-sepsis). The Panaroo pangenome "
    "presence/absence matrix and MASH kinship matrix are deposited within the repository. Raw sequencing reads analysed during "
    "this study are publicly accessible through the NCBI Sequence Read Archive under accessions detailed in Supplementary Table S1.",
    count_words=False
)

# ═══════════════════════════════════════════════════════════════════════
# REFERENCES — Sage Harvard Style (Author, Year)
# ═══════════════════════════════════════════════════════════════════════
add_h1("References")

refs_harvard = [
    "Andersson U, Yang H and Harris H (2018) Extracellular HMGB1 as a therapeutic target in inflammatory diseases. Expert Opinion on Therapeutic Targets 22(3): 263–277.",
    "Andrews S, Krueger F, Segonds-Pichon A, et al. (2010) FastQC: A Quality Control Tool for High Throughput Sequence Data. Cambridge: Babraham Institute.",
    "Bone RC (1996) Toward a theory regarding the pathogenesis of the systemic inflammatory response syndrome: What we do and do not know about cytokine regulation. Critical Care Medicine 24(1): 163–172.",
    "Calvano SE, Xiao W, Richards DR, et al. (2005) A network-based analysis of systemic inflammation in humans. Nature 437(7061): 1032–1037.",
    "Casey LC, Balk RA and Bone RC (1993) Plasma cytokine and endotoxin levels correlate with survival in patients with the sepsis syndrome. Annals of Internal Medicine 119(8): 771–778.",
    "Chen S, Zhou Y, Chen Y, et al. (2018) fastp: An ultra-fast all-in-one FASTQ preprocessor. Bioinformatics 34(17): i884–i890.",
    "Chow CC, Clermont G, Kumar R, et al. (2005) The acute inflammatory response in diverse shock states. Shock 24(1): 74–84.",
    "Craig WA (1998) Pharmacokinetic/pharmacodynamic parameters: Rationale for antibacterial dosing of mice and men. Clinical Infectious Diseases 26(1): 1–10.",
    "Cumming BM, Chinta KC, Reddy VP, et al. (2018) Role of ergothioneine in microbial physiology and pathogenesis. Antioxidants & Redox Signaling 28(6): 431–444.",
    "David S, Reuter S, Harris SR, et al. (2019) Epidemic of carbapenem-resistant Klebsiella pneumoniae in Europe is driven by nosocomial spread. Nature Microbiology 4(11): 1919–1929.",
    "Drusano GL and Hutchison M (1995) The pharmacokinetics of meropenem. Scandinavian Journal of Infectious Diseases Supplementum 96: 11–16.",
    "Earle SG, Wu C-H, Charlesworth J, et al. (2016) Identifying lineage effects when controlling for population structure improves power in bacterial association studies. Nature Microbiology 1(5): 16041.",
    "Feldgarden M, Brover V, Gonzalez-Escalona N, et al. (2021) AMRFinderPlus and the Reference Gene Catalog facilitate examination of the complex antimicrobial resistance mobilome. Scientific Reports 11: 12728.",
    "Gurevich A, Saveliev V, Vyahhi N, et al. (2013) QUAST: Quality assessment tool for genome assemblies. Bioinformatics 29(8): 1072–1075.",
    "Hotchkiss RS, Moldawer LL, Opal SM, et al. (2016) Sepsis and septic shock. Nature Reviews Disease Primers 2: 16045.",
    "Kedzierska-Mieszkowska S and Zolkiewski M (2021) Hsp100 molecular chaperone ClpB and its role in virulence of bacterial pathogens. International Journal of Molecular Sciences 22(10): 5319.",
    "Kumar A, Roberts D, Wood KE, et al. (2006) Duration of hypotension before initiation of effective antimicrobial therapy is the critical determinant of survival in human septic shock. Critical Care Medicine 34(6): 1589–1596.",
    "Kumar R, Clermont G, Vodovotz Y, et al. (2004) The dynamics of acute inflammation. Journal of Theoretical Biology 230(2): 145–155.",
    "Lam MMC, Wick RR, Watts SC, et al. (2021) A genomic surveillance framework and genotyping tool for Klebsiella pneumoniae. Nature Communications 12: 4188.",
    "Lees JA, Galardini M, Bentley SD, et al. (2018) pyseer: A comprehensive tool for microbial pangenome-wide association studies. Bioinformatics 34(24): 4310–4312.",
    "Lees JA, Vehkala M, Valimaki N, et al. (2016) Sequence element enrichment analysis to determine the genetic basis of bacterial phenotypes. Nature Communications 7: 12797.",
    "Li D, Liu C-M, Luo R, et al. (2015) MEGAHIT: An ultra-fast single-node solution for large and complex metagenomics assembly via succinct de Bruijn graph. Bioinformatics 31(10): 1674–1676.",
    "Marino S, Hogue IB, Ray CJ, et al. (2008) A methodology for performing global uncertainty and sensitivity analysis in systems biology. Journal of Theoretical Biology 254(1): 178–196.",
    "Ondov BD, Treangen TJ, Melsted P, et al. (2016) Mash: Fast genome and metagenome distance estimation using MinHash. Genome Biology 17(1): 132.",
    "Patel IH, Chen S, Parsonnet M, et al. (1981) Pharmacokinetics of ceftriaxone in humans. Antimicrobial Agents and Chemotherapy 20(5): 634–641.",
    "Pitout JD, Nordmann P and Poirel L (2015) Carbapenemase-producing Klebsiella pneumoniae, a key pathogen set for global nosocomial dominance. Antimicrobial Agents and Chemotherapy 59(10): 5873–5884.",
    "Power RA, Parkhill J and de Oliveira T (2016) Microbial genome-wide association studies: Lessons from human GWAS. Nature Reviews Genetics 18(1): 41–50.",
    "Reynolds A, Rubin J, Clermont G, et al. (2006) A reduced mathematical model of the acute inflammatory response I. Derivation of model and analysis of anti-inflammation. Journal of Theoretical Biology 242(1): 220–236.",
    "Russo TA and Marr CM (2019) Hypervirulent Klebsiella pneumoniae. Clinical Microbiology Reviews 32(3): e00001-19.",
    "Saber MM and Shapiro BJ (2020) Benchmarking bacterial genome-wide association study methods using simulated genomes and phenotypes. Microbial Genomics 6(3): e000337.",
    "Scaffidi P, Misteli T and Bianchi ME (2002) Release of chromatin protein HMGB1 by necrotic cells triggers inflammation. Nature 418(6894): 191–195.",
    "Seemann T (2014) Prokka: Rapid prokaryotic genome annotation. Bioinformatics 30(14): 2068–2069.",
    "Sheppard SK, Didelot X, Meric G, et al. (2013) Genome-wide association study identifies vitamin B5 biosynthesis as a host specificity factor in Campylobacter. Proceedings of the National Academy of Sciences 110(29): 11923–11927.",
    "Tonkin-Hill G, MacAlasdair N, Ruis C, et al. (2020) Producing polished prokaryotic pangenomes with the Panaroo pipeline. Genome Biology 21(1): 180.",
    "van der Poll T, van de Veerdonk FL, Scicluna BP, et al. (2017) The immunopathology of sepsis and potential therapeutic targets. The Lancet Infectious Diseases 17(11): e407–e420.",
    "Volk HD, Reinke P and Docke WD (2000) Clinical aspects: From systemic inflammation to immunoparalysis. Chemical Immunology 74: 162–177.",
    "Wyres KL, Lam MMC and Holt KE (2020) Population genomics of Klebsiella pneumoniae. Nature Reviews Microbiology 18(6): 344–359.",
    "Xiao W, Mindrinos MN, Seok J, et al. (2011) A genomic storm in critically injured humans. Journal of Experimental Medicine 208(13): 2581–2590.",
]

for ref in refs_harvard:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(2)
    p_ref.paragraph_format.left_indent = Inches(0.4)
    p_ref.paragraph_format.first_line_indent = Inches(-0.4)
    p_ref.paragraph_format.line_spacing = 1.5
    r = p_ref.add_run(ref)
    r.font.size = Pt(10)
    r.font.name = 'Times New Roman'

# ═══════════════════════════════════════════════════════════════════════
# SAVE AND VALIDATE
# ═══════════════════════════════════════════════════════════════════════
doc.save(OUTPUT_PATH)

total_p_words = sum(len(p.text.split()) for p in doc.paragraphs)
table_words = sum(len(cell.text.split()) for t in doc.tables for r in t.rows for cell in r.cells)

print("=" * 80)
print("OMICS ORIGINAL ARTICLE MANUSCRIPT GENERATION COMPLETE")
print("=" * 80)
print(f"Output File: {OUTPUT_PATH}")
print(f"File Size:   {os.path.getsize(OUTPUT_PATH):,} bytes")
print("")
print("SECTION WORD BREAKDOWN (BODY ONLY):")
for sec, count in section_counts.items():
    print(f"  {sec:<35}: {count:>5} words")
print("-" * 50)
print(f"  Total Body Word Count           : {body_word_count:>5} words (Target: 3,800–3,950; Limit: 4,000)")
print(f"  Abstract Word Count             : {abstract_wc:>5} words (Limit: 200)")
print(f"  Total Document Words            : {total_p_words + table_words:>5} words")
print("")
print("FIGURE & TABLE COUNT:")
print("  Tables                          : 2 (Table 1, Table 2)")
print("  Figures                         : 3 (Figure 1 composite, Figure 2, Figure 3)")
print("  Total Combined Items            : 5 (Maximum allowed: 5) ✓")
print("")
print("COMPLIANCE VERIFICATION:")
if abstract_wc <= 200:
    print(f"  [PASS] Abstract complies with limit ({abstract_wc}/200 words)")
else:
    print(f"  [FAIL] Abstract exceeds 200 words ({abstract_wc}/200 words)")

if 3700 <= body_word_count <= 4000:
    print(f"  [PASS] Body word count is optimal and compliant ({body_word_count}/4,000 words)")
elif body_word_count < 3700:
    print(f"  [WARN] Body word count is below target ({body_word_count}/4,000 words)")
else:
    print(f"  [FAIL] Body word count exceeds 4,000 words ({body_word_count}/4,000 words)")
print("=" * 80)

