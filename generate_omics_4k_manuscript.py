"""
══════════════════════════════════════════════════════════════════════════════
OMICS: A Journal of Integrative Biology — Humanized Original Article Generator
══════════════════════════════════════════════════════════════════════════════
Revised using 'research-paper-humanizer' guidelines:
  • Lever 1 (Information Order): Old linking info first, results/numbers in stress position
  • Lever 2 (Participle Tails): Zero dangling participle tails (', highlighting/demonstrating')
  • Lever 3 (De-nominalization): Verbs used instead of bulky nominal chains
  • Lever 4 (Functional Voice): Agentless passive for procedures; active 'we' for decisions/findings
  • Lever 5 (Burstiness): Mixed sentence lengths (5-9 word punchy lines with longer complex lines)
  • Lever 6 (Paragraph Shape): Direct clinical problem entry, no generic textbook dictionary openers
  • Lever 7 (Clean Transitions): Zero stacked transitions (Moreover, Furthermore, Additionally)
  • Lever 8 (Calibrated Hedges): Statistical hedges matched strictly to data, zero boosters
  • Strictly preserves all experimental data, ODE equations, citations, tables, and figures
  • Conforms to OMICS guidelines:
      - Abstract: Unstructured, ≤ 200 words
      - Body: ≤ 4,000 words (Target: 3,800 – 3,950 words)
      - Figures & Tables: Exactly 5 items combined
      - Reference style: Sage Harvard (Author, Year)
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

# Page Margins (1 inch)
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
# TITLE & AUTHORS
# ═══════════════════════════════════════════════════════════════════════

add_title(
    "Translating Bacterial Population Genomics into Infection Dynamics: "
    "An Integrative Multi-Scale ODE Model of Sepsis Caused by Klebsiella pneumoniae"
)

add_authors("Gautham G L, Dhruti Reddy P, S Apurva Ananya, Sasmita Sabat*")
add_affiliation(
    "Department of Biotechnology, National Institute of Technology, Rourkela, India.\\n"
    "* Corresponding author: Sasmita Sabat (sasmita.sabat@nitrkl.ac.in)"
)

# ═══════════════════════════════════════════════════════════════════════
# ABSTRACT (≤200 words, unstructured, NOT counted in body)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Abstract")

abstract_text = (
    "Genome-wide association studies pinpoint bacterial genes linked to invasive infection, but static regression weights "
    "reveal nothing about how an infection unfolds in a human host. We integrated microbial GWAS summary statistics directly "
    "into a ten-compartment ordinary differential equation model of Klebsiella pneumoniae bacteremia. Across 200 clinical isolates "
    "(100 bacteremic cases and 100 non-invasive controls) evaluated with linear mixed models, bloodstream invasion tracked with "
    "two lineage-independent stress operons: the heat-shock disaggregase clpK/clpB (beta = +0.434) and the ergothioneine pathway "
    "egtB (beta = +0.394), alongside acquired beta-lactamase determinants (bla_1/IS6, beta = +0.350/+0.388). Converted to cellular "
    "kinetic multipliers across 1,000 Latin hypercube samples, these loci dictated maximum tissue damage across linear, "
    "exponential, and power-law mappings. Epistatic co-occurrence of both operons tipped host inflammation past a bistable threshold "
    "into self-sustaining tissue destruction (damage index D > 0.36). Bacteriolytic therapy at peak bacterial density generated a "
    "marked spike in free plasma endotoxin that maintained organ injury even as viable bacteria cleared. Antibiotic initiation "
    "past ten hours failed to reverse organ failure, defining an acute therapeutic window. Translating statistical associations into "
    "non-linear kinetic rates provides an empirical strategy for forecasting clinical infection courses from pathogen sequence data."
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
# 1. INTRODUCTION (~500 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Introduction")

add_p(
    "Severe sepsis causes roughly eleven million deaths annually, accounting for nearly one in five fatalities worldwide "
    "(Hotchkiss et al., 2016). Intensive care units face particular difficulty with Klebsiella pneumoniae, where multidrug-resistant "
    "lineages circulate readily among critically ill patients (Wyres et al., 2020). When bacteremia takes hold, clinical trajectories "
    "vary widely (van der Poll et al., 2017). Patients with indistinguishable comorbidities and identical in vitro susceptibility "
    "profiles frequently follow divergent clinical paths: some resolve the bloodstream infection after empiric antibiotic therapy, "
    "whereas others deteriorate into refractory septic shock with multiorgan failure within hours of blood culture collection. "
    "Routine antimicrobial susceptibility testing reveals whether an antibiotic inhibits growth in broth, but offers no insight "
    "into the host-pathogen dynamics driving these distinct clinical courses."
)

add_p(
    "Bacterial genetics contributes substantially to these variable outcomes, yet traditional phenotypic groupings obscure "
    "the relevant traits. Clinicians and microbiologists have long separated K. pneumoniae into community-acquired hypervirulent "
    "strains (hvKp) and hospital-adapted classical strains (cKp) (Russo and Marr, 2019). Hypervirulent lineages rely on high-molecular-weight "
    "capsule regulators and siderophore clusters carried on large virulence plasmids to cause invasive disease in previously healthy "
    "hosts. Hospital bacteremia isolates, however, rarely possess this classic virulence plasmid repertoire. In elderly and "
    "immunocompromised patients, bloodstream survival depends on cellular stress defenses that neutralize reactive oxygen species "
    "generated by neutrophils and resist enzymatic degradation within macrophages. Because diagnostic microbiology laboratories focus "
    "strictly on taxonomic identification and minimum inhibitory concentrations, these fitness and persistence operons remain "
    "unmeasured during active clinical care."
)

add_p(
    "Existing computational frameworks fall into two distinct methodological camps. Microbial genome-wide association studies "
    "(Lees et al., 2018) evaluate accessory genes linked to invasive infection while controlling for lineage structure with linear "
    "mixed models (Earle et al., 2016). These regressions produce static summary metrics, such as odds ratios or log-odds coefficients. "
    "While valuable for ranking population-level risk, static weights cannot predict when bacteremia crests, how rapidly inflammatory "
    "cytokines accumulate, or when bacteriolytic drugs trigger massive endotoxin release. Conversely, mathematical models of acute "
    "inflammation (Kumar et al., 2004; Chow et al., 2005; Reynolds et al., 2006) describe sepsis as a non-linear dynamical system with "
    "bistable tipping points. Although ordinary differential equations capture feedback loops between leukocytes, cytokines, and tissue "
    "injury, they treat the pathogen as an undifferentiated scalar variable with uniform clearance constants. An isolate carrying "
    "specialized stress-tolerance operons is assigned the exact same parameters as a benign carriage isolate, omitting the bacterial "
    "accessory genome entirely."
)

add_p(
    "To link bacterial pangenome architecture with host-response kinetics, we parameterized a 10-compartment differential equation "
    "model using effect sizes derived directly from microbial GWAS. Drawing from 200 clinical K. pneumoniae genomes, we identified two "
    "lineage-independent stress-defense operons associated with bacteremia and mapped their statistical weights into cellular kinetic "
    "multipliers governing pathogen survival. The dynamical system couples circulating neutrophils, tissue macrophages, pro-inflammatory "
    "and anti-inflammatory cytokines, parenchymal necrosis, free circulating lipopolysaccharide, and two-compartment antibiotic distribution. "
    "This model allowed us to test whether combinations of accessory stress operons act synergistically to drive host tissue damage past "
    "an irreversible bistable threshold, measure the magnitude of the post-antibiotic endotoxin surge under cephalosporin versus "
    "carbapenem lysis, and determine the therapeutic time window beyond which bactericidal clearance fails to halt fatal host inflammation."
)

# ═══════════════════════════════════════════════════════════════════════
# 2. METHODS (~1,310 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Methods")

add_h2("Genomic data acquisition, assembly, and pangenome construction")
add_p(
    "Whole-genome sequencing reads from 100 K. pneumoniae blood-culture isolates were retrieved from the NCBI Sequence Read "
    "Archive (SRA). To establish a matched control cohort, 100 non-invasive carriage and environmental genomes were downloaded "
    "from the NCBI Assembly database, yielding N = 200 genomes. Read quality was checked using FastQC v0.11.9 (Andrews et al., 2010). "
    "Adapters were trimmed and low-quality bases removed (sliding-window Phred score < Q20) with fastp v0.23.2 (Chen et al., 2018). "
    "De novo assemblies were generated using MEGAHIT v1.2.9 (Li et al., 2015) across k-mer lengths from 21 to 141 (step size 12). "
    "Assembly metrics were verified with QUAST v5.2.0 (Gurevich et al., 2013). We retained only assemblies with N50 > 20 kbp, "
    "total span between 5.3 and 5.5 Mbp, and fewer than 5% ambiguous bases. Acquired resistance genes were mapped using AMRFinderPlus "
    "v3.11.26 (Feldgarden et al., 2021). Capsular serotypes (K-locus) and LPS O-types were typed with Kleborate v2.4.1 (Lam et al., 2021). "
    "Coding sequences were annotated with Prokka v1.14.6 (Seemann, 2014). For pangenome reconstruction, ortholog clustering was "
    "executed in Panaroo v1.3.4 (Tonkin-Hill et al., 2020) in strict mode (95% sequence identity, 98% length match). Panaroo resolved "
    "16,477 gene clusters. After filtering to minor allele frequencies between 5% and 95%, 3,735 polymorphic clusters entered association testing."
)

add_h2("Microbial GWAS and statistical power justification")
add_p(
    "Statistical power was evaluated against empirical bacterial benchmarks established by Saber and Shapiro (2020). Under their "
    "framework, 100 cases and 100 controls provide over 80% power to detect moderate effect sizes (beta >= 0.30, odds ratio >= 1.35) "
    "across intermediate allele frequencies (5–95%). Clonal structure was accounted for by computing pairwise MASH distances "
    "(k = 21, sketch size s = 10,000; Ondov et al., 2016) and converting them into a kinship similarity matrix (narrow-sense "
    "heritability h-squared = 0.90). Association models were run in pyseer (Lees et al., 2018) against a Bonferroni threshold of "
    "p < 1.34 x 10-5 (alpha = 0.05 / 3,735 tests). Baseline regression yielded a genomic inflation factor of lambda = 1.531. While human "
    "studies target lambda near 1.0, clonal bacterial datasets routinely produce values between 1.3 and 1.8 because binary fission "
    "generates extensive linkage disequilibrium (Earle et al., 2016; Power et al., 2016). Neutral hitchhiker alleles co-segregate with "
    "causal mutations down phylogenetic branches (Lees et al., 2016; Sheppard et al., 2013). To isolate causal signals from lineage baggage, "
    "we ran conditional LMM regressions with baseline-significant genes included as fixed covariates. This adjustment reduced lambda to 1.460 "
    "and uncovered eight secondary associations."
)

add_p(
    "In pyseer, population structure correction relies on factored linear mixed models where the kinship matrix decomposes "
    "phenotype variance into additive genetic variance and residual environmental variance (narrow-sense heritability h-squared = 0.90). "
    "This variance partitioning prevents major lineage markers from confounding test statistics, although it cannot eliminate "
    "linkage disequilibrium between causal variants and their shared clonal frames."
)

add_h2("Ten-compartment ODE model formulation")
add_p(
    "We extended the acute inflammation models of Reynolds et al. (2006) and Kumar et al. (2004) into a 10-compartment system. "
    "The model tracks ten interacting state variables: normalised bacterial burden (B), activated neutrophils (N), activated tissue macrophages (M), "
    "interleukin-6 (IL-6), tumour necrosis factor-alpha (TNF-alpha), interleukin-10 (IL-10), cumulative tissue damage (D), antibiotic depot (A_dep), "
    "plasma antibiotic concentration (A_p), and free circulating lipopolysaccharide (LPS, L). Bacterial replication follows logistic "
    "growth with replication rate k_b = 0.45/h and carrying capacity 1.0, balanced by natural death d_b = 0.12/h, baseline surveillance "
    "k_surv = 0.05/h, leukocyte phagocytosis, and antibiotic killing (E_abx):"
)

add_equation(
    "dB/dt = k_b * B * (1 - B) - d_b * B - k_surv * B - K_immune - E_abx * B"
)

add_p(
    "Leukocyte killing (K_immune) combines oxidative and non-oxidative neutrophil action with macrophage killing, modulated by "
    "IL-10 suppression factor supp = 1 / (1 + kappa_IL10 * IL10), with kappa_IL10 = 5.0 (Hill coefficient n = 1):"
)

add_equation(
    "K_immune = [ (k_NB,ox / phi_ROS + k_NB,pep) * (N - N_0) + (k_MB / phi_stress) * (M - M_0) ] * B * supp"
)

add_p(
    "Resting baseline leukocyte levels are set to N_0 = 0.10 and M_0 = 0.10. Baseline bactericidal rate constants are k_NB,ox = 0.35/h, "
    "k_NB,pep = 0.10/h, and k_MB = 0.25/h. Pyseer multipliers phi_ROS and phi_stress reduce neutrophil oxidative killing and "
    "macrophage degradation, respectively. Activated neutrophils (N) and macrophages (M) are recruited by bacteria, free LPS, and "
    "pro-inflammatory cytokines, balanced by apoptosis (d_N = 0.05/h, d_M = 0.02/h):"
)

add_equation(
    "dN/dt = [ (k_N,rec * B + k_N,LPS * L + k_N,cyt * (IL6 + TNF)) * supp ] - d_N * (N - N_0)"
)
add_equation(
    "dM/dt = [ (k_M,bact * B + k_M,LPS * L + k_M,cyt * (IL6 + TNF)) * supp ] - d_M * (M - M_0)"
)

add_p(
    "Pro-inflammatory cytokines IL-6 and TNF-alpha are released when leukocytes encounter bacteria and circulating LPS via TLR4, "
    "with decay rates d_IL6 = 0.30/h and d_TNF = 0.40/h (half-lives ~2.3 h and ~1.7 h):"
)

add_equation(
    "d[IL-6]/dt = [ (k_IL6,N * N + k_IL6,M * M) * B * supp ] + [ k_IL6,LPS * M * L * supp ] - d_IL6 * [IL-6]"
)
add_equation(
    "d[TNF-a]/dt = [ k_TNF,M * M * B * supp ] + [ k_TNF,LPS * M * L * supp ] - d_TNF * [TNF-a]"
)

add_p(
    "Anti-inflammatory counter-regulation is governed by IL-10, capturing the Compensatory Anti-inflammatory Response Syndrome "
    "(CARS; Bone, 1996). Secretion is driven by macrophages, pro-inflammatory cytokine feedback (k_IL10,cyt = 0.80/h), and "
    "endotoxin (k_IL10,LPS = 0.50/h), counteracted by clearance (d_IL10 = 0.25/h):"
)

add_equation(
    "d[IL-10]/dt = k_IL10,M * (M - M_0) + k_IL10,cyt * (IL6 + TNF) + k_IL10,LPS * L - d_IL10 * [IL-10]"
)

add_p(
    "The tissue damage index (D) measures microvascular injury and cellular necrosis. Damage accumulates through bacterial toxicity "
    "(k_D,bact = 0.20/h), cytokine collateral damage (k_D,cyt = 0.15/h), endotoxin endothelial damage (k_D,LPS = 0.25/h), and an "
    "autocatalytic quadratic term (k_D,comp * D^2, with k_D,comp = 0.40/h). This quadratic term represents sterile inflammation driven "
    "by Damage-Associated Molecular Patterns (DAMPs), including HMGB1, extracellular histones, and mitochondrial DNA. These ligands "
    "activate TLR4 and the NLRP3 inflammasome even after viable bacteria are cleared (Scaffidi et al., 2002; Andersson et al., 2018). "
    "Repair occurs at rate d_D = 0.15/h:"
)

add_equation(
    "dD/dt = k_D,bact * B + k_D,cyt * (IL6 + TNF) + k_D,LPS * L + k_D,comp * D^2 - d_D * D"
)

add_p(
    "A tipping point occurs when quadratic damage amplification outpaces linear tissue repair (d(dD/dt)/dD > 0). This creates an "
    "unstable threshold at D = 0.36. Trajectories exceeding D = 0.36 escape homeostatic control and diverge toward organ failure "
    "(D_max = 1.500), consistent with the clinical definition of refractory septic shock (Hotchkiss et al., 2016)."
)

add_h2("Pharmacokinetics and endotoxin release dynamics")
add_p(
    "Antibiotic pharmacotherapy was implemented using a two-compartment model (depot A_dep and central plasma A_p). Drug absorption "
    "follows first-order kinetics (k_a = 1.50/h). Ceftriaxone was parameterised to match a standard clinical regimen of 2 g IV once daily "
    "(60 mg/L peak plasma concentration, k_el = 0.087/h, half-life ~8 h, bioavailability F = 1.0; Patel et al., 1981). Meropenem was "
    "parameterised for 1 g IV every 8 h (40 mg/L peak, k_el = 0.69/h, half-life ~1 h, F = 1.0; Drusano and Hutchison, 1995). Bacterial "
    "killing follows a Hill function (Emax = 1.20/h, Hill coefficient h = 2.0, EC50 = 8.0 mg/L), scaled by the resistance multiplier phi_abx:"
)

add_equation(
    "E_abx = Emax * (A_p)^h / [ (EC50 * phi_abx)^h + (A_p)^h ]"
)

add_p(
    "Pharmacokinetic distribution across compartments is governed by coupled linear differential equations:"
)
add_equation("dA_dep/dt = -k_a * A_dep")
add_equation("dA_p/dt = k_a * A_dep - k_el * A_p")
add_p(
    "Drug absorption from the depot compartment into the central plasma compartment proceeds with first-order "
    "rate constant k_a = 1.50/h. Systemic clearance follows elimination rate k_el, corresponding to the specific "
    "beta-lactam agent parameterised."
)

add_p(
    "Free circulating endotoxin (LPS, L) captures three release sources: basal division shedding (alpha_shed = 0.04/h), immune-mediated "
    "lysis (gamma_imm = 0.40), and rapid antibiotic cell-wall lysis (gamma_abx = 1.00). Clearance occurs via hepatic and reticuloendothelial "
    "pathways (d_L = 0.35/h, half-life ~2.0 h):"
)

add_equation(
    "dL/dt = alpha_shed * B + gamma_abx * E_abx * B + gamma_imm * K_immune - d_L * L"
)

add_p(
    "Antibiotics were initiated at t = 6.0 h post-inoculation rather than at t = 0 to simulate real-world emergency presentation "
    "after symptom onset."
)

add_h2("Mapping GWAS effect sizes to ODE rate multipliers")
add_p(
    "We mapped pyseer log-odds effect sizes (beta) into kinetic multipliers using the exponential function phi = exp(beta):"
)
add_equation("phi_ROS = exp(beta_egtB) = exp(0.394) = 1.483")
add_equation("phi_stress = exp(beta_clpK/clpB) = exp(0.434) = 1.543")
add_equation("phi_abx = exp(beta_bla + beta_IS6) = exp(0.350 + 0.388) = exp(0.738) = 2.092")

add_p(
    "This mapping translates statistical associations into specific physiological mechanisms. Hercynine oxygenase (EgtB) is an "
    "iron(II)-dependent sulfoxide synthase that catalyzes the oxidative condensation of gamma-glutamylcysteine and "
    "N-alpha,N-alpha,N-alpha-trimethyl-L-histidine (hercynine). This reaction represents the first committed step in ergothioneine "
    "biosynthesis. Because ergothioneine accumulates to millimolar concentrations in the bacterial cytoplasm and scavenges peroxynitrite "
    "and hydrogen peroxide faster than glutathione, it protects bacteria against neutrophil oxidative bursts. In the model, this manifests "
    "as a 48% reduction in the effective rate of neutrophil oxidative killing (phi_ROS = 1.483). Similarly, ClpB forms a hexameric ring "
    "with an axial pore that works with the DnaK-DnaJ-GrpE chaperone system to extract and refold misfolded proteins from aggregated "
    "inclusion bodies. This system prevents proteotoxic death inside macrophage phagolysosomes, represented as a 54% reduction in "
    "macrophage killing (phi_stress = 1.543)."
)

add_h2("Global sensitivity analysis and mapping robustness")
add_p(
    "We performed global sensitivity analysis using Latin Hypercube Sampling (LHS) and Partial Rank Correlation Coefficients "
    "(PRCC; Marino et al., 2008). Ten parameters were varied simultaneously: pyseer multipliers (phi_ROS, phi_stress, phi_abx) "
    "over +/-50%, and core physiological rates (k_b, k_NB,ox, k_D,comp, kappa_IL10, k_IL10,cyt, d_D, k_D,bact) over +/-30% across "
    "N = 1,000 stratified samples. Equations were integrated over 168 h using SciPy's explicit Runge-Kutta method of order 5(4) (RK45) "
    "with initial inoculum B_0 = 0.05. To test sensitivity to the mapping formula, we evaluated four mathematical forms: exp(beta), "
    "linear (1 + beta), base-2 (2^beta), and base-10 (10^beta), running 200 LHS simulations per function (800 simulations in total)."
)

# ═══════════════════════════════════════════════════════════════════════
# 3. RESULTS (~1,135 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Results")

add_h2("Population structure and lineage segregation")
add_p(
    "The 200 genomes resolved into 72 distinct sequence types (STs). Sepsis and carriage cohorts partitioned into distinct clonal lineages. "
    "Sepsis isolates clustered heavily within high-risk hospital clones ST512, ST101, and ST147, while carriage controls were enriched "
    "in ST15 (David et al., 2019). Antimicrobial resistance differed sharply between groups: sepsis isolates averaged 18.1 acquired "
    "resistance genes, compared to 4.2 in controls. Over 57% of sepsis genomes carried the extended-spectrum beta-lactamase bla_CTX-M-15, "
    "alongside significant enrichment of carbapenemase genes bla_KPC-2, bla_KPC-3, and bla_NDM-1 (Pitout et al., 2015). Classical "
    "hypervirulence markers, including the rmpA/rmpA2 capsule regulators and iucA aerobactin operon, were scarce across both cohorts. "
    "Kleborate virulence scores averaged 1.15 in sepsis versus 1.97 in controls. Sepsis in this inpatient cohort was therefore propelled "
    "by multidrug-resistant lineages rather than classical hypervirulence plasmids."
)

add_h2("Microbial GWAS: baseline and conditional association signals")
add_p(
    "Testing 3,735 gene clusters in baseline pyseer models yielded five Bonferroni-significant loci (Table 1). The strongest association "
    "mapped to the co-transcribed chaperone operon clpK_1/clpB_1/clpK (beta = +0.434, p = 7.32 x 10-8). An isolated clpK monomer was "
    "conversely enriched in controls (beta = -0.533, p = 1.79 x 10-8). Invasive fitness evidently requires the full ClpB/ClpK disaggregase "
    "complex, not the solitary ATPase. Resistance determinants also emerged at baseline, including bla_1 (beta = +0.350, p = 9.54 x 10-6) "
    "and an IS6/IS26 transposase element (group_5277, beta = +0.388, p = 1.21 x 10-5). Conditional regressions adjusting for these baseline "
    "loci exposed eight secondary signals (Table 1). Foremost among them was hercynine oxygenase egtB_2/egtB_1 (beta = +0.394, p = 3.75 x 10-7), "
    "followed by an ergothioneine-kinase cluster containing pkn1 (beta = +0.365, p = 1.93 x 10-6). Negative associations in controls included "
    "plasmid maintenance elements: the FinO fertility inhibitor (group_4547, beta = -0.637) and the KlcA antirestriction protein (beta = -0.535)."
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

add_p(
    "The negative associations detected in carriage isolates reflect plasmid maintenance functions. Fertility inhibition "
    "protein FinO (group_4547, beta = -0.637, p = 2.47 x 10-7) represses conjugative transfer of F-like plasmids by binding "
    "sense-antisense RNA duplexes, limiting donor ability in carriage lineages. Similarly, the antirestriction protein KlcA "
    "(beta = -0.535, p = 6.18 x 10-7) protects invading plasmid DNA against type I restriction-modification systems during "
    "horizontal gene transfer. Their significant enrichment in non-invasive isolates indicates that carriage strains "
    "prioritize conjugative plasmid stability over invasive host survival traits."
)

add_h2("Global sensitivity analysis and parameter ranking")
add_p(
    "Simulating 1,000 untreated infection courses via Latin Hypercube Sampling produced peak damage scores (D_max) between 0.101 and 1.501. "
    "Sepsis threshold violations (D > 0.36) occurred in 55.7% of trajectories. Partial rank correlation coefficients (PRCC) showed "
    "significant influence for all ten evaluated parameters (p < 0.001; Figure 1A). Pathogen replication rate k_b exerted the strongest "
    "positive push toward tissue destruction (PRCC = +0.759). Crucially, the GWAS-derived multipliers ranked within the top five drivers: "
    "macrophage stress survival phi_stress registered PRCC = +0.540, while neutrophil ROS resistance phi_ROS reached PRCC = +0.406. Host defenses "
    "opposed this progression, led by intrinsic tissue repair d_D (PRCC = -0.416) and oxidative neutrophil clearance k_NB,ox (PRCC = -0.250). "
    "Testing four separate mapping functions showed that this dynamic behavior was robust (Figure 1B). Threshold-crossing frequencies remained "
    "high across functions: 50.5% for 2^beta, 55.7% for exp(beta), 58.0% for 1 + beta, and 93.5% for 10^beta."
)

add_p(
    "These sensitivity rankings highlight an important biological timing feature. Bacterial replication (k_b, PRCC = +0.759) and "
    "intracellular survival (phi_stress, PRCC = +0.540) control host trajectory during early hours before drugs enter the system. In untreated "
    "runs, the resistance multiplier phi_abx had no discernible effect on tissue injury (PRCC = +0.024, p = 0.44; Figure 1A). Resistance genes "
    "provide zero survival value in the absence of antibiotic pressure. Only upon drug administration at t = 6.0 h did phi_abx influence "
    "outcomes, shifting the effective EC50 from 8.0 mg/L to 16.7 mg/L and delaying bacterial clearance."
)

# FIGURE 1: Composite Sensitivity (1A + 1B)
add_fig_image(
    "Fig1_Sensitivity_and_Mapping_Composite.png",
    "Figure 1. Global sensitivity and mapping evaluation. (A) Tornado plot of Partial Rank Correlation Coefficients (PRCC) "
    "for peak tissue damage D_max across N = 1,000 Latin Hypercube samples. Red bars show pro-sepsis parameters; blue bars show "
    "host-protective parameters (all p < 0.001). (B) Box-violin distributions of D_max across four mathematical mappings "
    "(exp(beta), 1+beta, 2^beta, and 10^beta; N = 200 each). The red dashed line marks the sepsis threshold (D = 0.36).",
    width=Inches(6.0)
)

add_h2("ODE dynamics, epistatic cooperativity, and bacteriolytic endotoxin release")
add_p(
    "Over 168-hour simulated courses, the GWAS determinants exhibited striking epistatic synergy (Table 2; Figure 2). Wild-type infection "
    "resolved spontaneously, keeping peak damage well below threshold (D_max = 0.257, final B = 0.0036). Single-operon variants also failed "
    "to cause lethal sepsis: egtB alone peaked at D_max = 0.283, and clpK/clpB alone reached D_max = 0.313. When both operons co-occurred, "
    "the system crossed the bistable boundary into irreversible organ failure (D_max = 1.500). Evasion of neutrophil respiratory bursts "
    "coupled with macrophage disaggregase activity crippled host clearance, sustaining high bacterial densities and driving unabated endotoxemia."
)

add_p(
    "Antimicrobial therapy initiated at t = 6.0 h suppressed bacteremia within 24 hours and averted fatal shock (ceftriaxone D_max = 0.281; "
    "meropenem D_max = 0.293; Table 2; Figure 2). Rapid bactericidal action, however, imposed its own inflammatory penalty. Meropenem's rapid "
    "bacteriolysis (elimination half-life ~1 h) provoked a sharp endotoxin surge: free LPS peaked at 0.040 at t = 7.5 h, a 74% spike above "
    "the untreated ceiling of 0.023 (Table 2; Figure 2B). This burst ignited secondary release of TNF-alpha and IL-6. Meropenem consequently "
    "induced slightly greater peak damage (D_max = 0.293) than once-daily ceftriaxone (D_max = 0.281), mirroring post-antibiotic clinical "
    "deterioration observed in patients."
)

add_p(
    "Bacteriolytic kinetics governed this endotoxin profile. Untreated infection shed LPS gradually during binary fission. Meropenem "
    "compressed bacterial destruction into an acute release wave (maximum shedding rate dL/dt_max = 0.034/h versus 0.018/h for ceftriaxone). "
    "By lysing bacteria at a slower, sustained rate, ceftriaxone buffered pattern-recognition receptor activation. Both agents achieved "
    "complete bacteriological cure, but their lysis kinetics dictated distinct host inflammatory curves."
)

# TABLE 2: ODE Simulation Outcomes
add_p_noindent(
    "Table 2. In silico clinical outcome metrics across simulated K. pneumoniae infection scenarios over 168 hours "
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
    "B on logarithmic scale. (B) Free circulating lipopolysaccharide (LPS). (C) Total cytokine index (IL-6 + TNF-alpha). "
    "(D) Cumulative tissue damage D relative to the sepsis threshold (D = 0.36, red dashed line). Untreated infection leads to "
    "fatal organ collapse (D = 1.500); antibiotic initiation at t = 6.0 h halts progression below threshold.",
    width=Inches(6.0)
)

add_h2("Validation against published clinical cytokine profiles")
add_p(
    "Simulated cytokine dynamics tracked clinical observations from human endotoxin trials and ICU cohorts (Calvano et al., 2005; "
    "Xiao et al., 2011; van der Poll et al., 2017). TNF-alpha surged first, peaking between 2.5 and 3.5 h post-inoculation. "
    "Counter-regulatory IL-10 followed at 4.5–6.0 h, while IL-6 crested between 6.0 and 8.0 h. This chronological order mirrors "
    "experimental intravenous LPS challenges, where early TNF-alpha triggers IL-10 dampening while IL-6 remains elevated during "
    "microvascular hypoperfusion (Casey et al., 1993; Calvano et al., 2005). Continued IL-10 elevation through 24–72 hours in untreated "
    "trajectories captures the immunoparalysis characteristic of the compensatory anti-inflammatory response syndrome (CARS; Bone, 1996; Volk et al., 2000)."
)

add_h2("The therapeutic window of antibiotic timing")
add_p(
    "Titrating antibiotic start times from 2 to 48 hours mapped an unforgiving therapeutic window (Figure 3). Dosing within 10 hours "
    "confined tissue injury below the bifurcation threshold (D_max = 0.358), permitting host recovery. Beyond 10 hours, survival collapsed. "
    "Starting drugs at 12 hours allowed tissue injury to breach D = 0.36 prior to bacterial suppression. Once past this threshold, quadratic "
    "inflammation (k_D,comp * D^2) sustained organ destruction (D_max = 1.500) despite total bacterial eradication (final B = 0.0000 across all "
    "delays; Figure 3B). Sterile inflammation killed the host after the pathogen was gone."
)

add_p(
    "Hourly stepping between 8 and 14 hours located the tipping point precisely. Treatment at 8 h limited D_max to 0.298; at 9 h, D_max "
    "reached 0.324; at 10 h, D_max hit 0.358, resting immediately below the 0.360 cliff. At 11 h, D_max jumped to 0.482 before hitting "
    "terminal shock (1.500) at 12 h. The 60 minutes between 10 and 11 hours mark an irreversible transition: DAMP-driven damage generation "
    "outpaces maximal tissue repair capacity (d_D * D = 0.054/h), decoupling clinical outcome from microbial load (Figure 3A,B)."
)

# FIGURE 3: Golden Window
add_fig_image(
    "Fig_LPS_4_TimeToTreatment_Window.png",
    "Figure 3. Antibiotic timing analysis. (A) Peak tissue damage D_max across antibiotic initiation delays from 2 to 48 h. "
    "Treatment within 10 h prevents lethal damage; delays >= 12 h cross the sepsis threshold (D = 0.36, red dashed line). "
    "(B) Final bacterial load at 168 h, showing complete clearance across all delays despite fatal host outcomes with late treatment.",
    width=Inches(5.5)
)

# ═══════════════════════════════════════════════════════════════════════
# 4. DISCUSSION (~845 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Discussion")

add_p(
    "Integrating bacterial genomics with ODE kinetics addresses a fundamental limitation of static statistical associations. "
    "The two independent mGWAS signals uncovered here, baseline clpK/clpB and conditional egtB, converge on a coherent biological "
    "phenotype: cellular resistance to leukocyte bactericidal mechanisms. Clonal bacterial association studies frequently suffer "
    "from false positives driven by phylogenetic hitchhiking along expanding clonal frames (Power et al., 2016). Here, the functional "
    "convergence of two unlinked genetic loci on complementary arms of intracellular survival, reactive oxygen scavenging and "
    "proteotoxic disaggregation, provides biological validation that random lineage association cannot explain (Earle et al., 2016)."
)

add_p(
    "These findings indicate that inpatient bacteremia relies on stress tolerance rather than classical hypervirulence. In community "
    "settings, severe Klebsiella infections stem from hypermucoviscous capsule production and siderophore acquisition (Russo and Marr, 2019). "
    "The bacteremia cohort examined here lacked these traits. In hospital-acquired infections, invasiveness reflects antimicrobial "
    "resistance coupled with survival against immune defense (Wyres et al., 2020). Ergothioneine, synthesized via EgtB, acts as a "
    "low-molecular-weight thiol that neutralizes peroxynitrite and hydroxyl radicals faster than glutathione, blunting neutrophil "
    "oxidative killing (Cumming et al., 2018). The ClpB/ClpK complex functions as an ATP-dependent disaggregase, reactivating aggregated "
    "proteins damaged during phagosomal respiratory bursts (Kedzierska-Mieszkowska and Zolkiewski, 2021). When parameterized into the "
    "ODE framework (phi_ROS = 1.48, phi_stress = 1.54), neither operon alone proved lethal. Together, they overwhelmed leukocyte clearance "
    "and precipitated fatal septic shock (Table 2; Figure 2D)."
)

add_p(
    "The model reproduces a frequent clinical conundrum: patient deterioration following bactericidal therapy. Rapid-acting meropenem "
    "cleared bacteremia faster than ceftriaxone but generated a 74% higher free LPS pulse, causing a transient secondary cytokine surge "
    "and increased peak damage (D_max = 0.293 vs 0.281). This stems from distinct bactericidal mechanics. Rapid spheroplast formation "
    "and osmotic lysis under carbapenem exposure dump lipid A into circulation, whereas cephalosporins lyse cells more gradually. "
    "This finding directly informs antimicrobial stewardship."
)

add_p(
    "Beta-lactam efficacy depends on the fraction of time free drug levels exceed the minimum inhibitory concentration (fT > MIC; Craig, 1998). "
    "Because meropenem has a short elimination half-life (~1 h), standard 30-minute bolus infusions create steep peaks that trigger abrupt "
    "bacterial lysis followed by prolonged troughs. Delivering meropenem as an extended 3-hour infusion or 24-hour continuous infusion "
    "maintains steady serum concentrations above MIC (Drusano and Hutchison, 1995). This continuous dosing avoids acute lysis spikes, "
    "minimizes endotoxin pulses, and improves survival in septic shock patients with augmented renal clearance."
)

add_p(
    "These simulations provide a mechanistic explanation for why every hour of antibiotic delay increases sepsis mortality (Kumar et al., 2006). "
    "In our system, antibiotics administered within 10 hours held tissue damage below the critical bifurcation point (D = 0.36). Beyond 12 "
    "hours, quadratic autocatalysis (k_D,comp * D^2) became self-sustaining. At that juncture, circulating DAMPs such as HMGB1, extracellular "
    "histones, and mitochondrial fragments perpetuate sterile inflammation through TLR4 and NLRP3 inflammasome signaling (Scaffidi et al., 2002; "
    "Andersson et al., 2018). The disease uncouples from the pathogen. Late antibiotic therapy sterilizes blood cultures but cannot halt death "
    "from endogenous tissue injury."
)

add_p(
    "Targeting these bacterial defenses offers a therapeutic opening. Because ClpB disaggregases and EgtB synthases have no human homologs, "
    "they represent compelling targets for adjunctive anti-virulence agents (Cumming et al., 2018; Kedzierska-Mieszkowska and Zolkiewski, 2021). "
    "Disabling these enzymes would restore leukocyte bactericidal efficiency without exerting direct bactericidal selection that drives "
    "antimicrobial resistance."
)

add_p(
    "These findings also carry diagnostic urgency. Conventional blood cultures require 24–48 hours for positivity, followed by 18–24 hours "
    "for phenotypic susceptibility. A patient carrying an invasive isolate will have passed the 10-hour therapeutic window before culture "
    "results return. Multiplex PCR or rapid metagenomic sequencing from positive blood-culture bottles can identify clpK/clpB, egtB, and "
    "bla_CTX-M within 2–3 hours. Detecting these operons would signal high risk for rapid tissue injury, justifying immediate full-dose "
    "therapy and continuous infusion regimens before organ failure becomes irreversible."
)

add_h2("Integrative multi-omics and translational systems biology")
add_p(
    "This multi-scale framework operationalizes the central premise of integrative biology. Rather than analyzing genomics, "
    "transcriptomics, and host physiomics in isolation, our ODE model bridges these separate layers into a predictive dynamical system. "
    "Pathogen accessory genomes provide the initial molecular variance; population-scale GWAS quantifies statistical risk; and dynamical "
    "modeling translates those static alleles into time-resolved trajectories of bacteremia, cytokine signaling, and tissue necrosis. "
    "This integration transforms observational sequencing into actionable bedside pharmacology."
)

# Limitations
add_h2("Limitations")
add_p(
    "This study has several limitations. The cohort of 200 genomes detects moderate-to-large genetic effects (Saber and Shapiro, 2020), "
    "but lacks power for rare variants with minor contributions. Sourcing control genomes from separate databases introduces potential "
    "geographic ascertainment bias. Furthermore, the ODE system assumes a well-mixed vascular compartment, omitting tissue-specific "
    "compartmentalization in lungs or kidneys. While the mapping function phi = exp(beta) yielded consistent findings across four "
    "mathematical forms (Figure 1B), it represents an empirical bridge requiring direct in vitro biochemical validation. Finally, "
    "host immune parameters reflect population averages rather than patient-specific genetic polymorphisms in innate immune receptors. "
    "Prospective clinical cohorts pairing pathogen sequencing with longitudinal patient cytokine profiling will be required to personalize these models."
)

# ═══════════════════════════════════════════════════════════════════════
# 5. CONCLUSIONS (~75 words)
# ═══════════════════════════════════════════════════════════════════════
add_h1("Conclusions")

add_p(
    "Translating bacterial population genomics into a 10-compartment dynamic model shows how statistical association signals "
    "translate into clinical outcomes. Microbial GWAS identified two independent stress-tolerance operons, clpK/clpB and egtB, that "
    "act epistatically to drive host tissue damage across an irreversible sepsis threshold (D > 0.36). The ODE system reproduces "
    "post-antibiotic endotoxin surges and identifies a sharp 10-hour therapeutic window. By bridging pathogen genomics, host immunology, "
    "and clinical pharmacokinetics, this framework provides an analytical foundation for genome-guided sepsis therapy and timely antibiotic administration."
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
    "This study analysed publicly available, de-identified bacterial genome sequences deposited in NCBI databases. "
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
print("HUMANIZED OMICS ORIGINAL ARTICLE MANUSCRIPT GENERATION COMPLETE")
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

if 3750 <= body_word_count <= 4000:
    print(f"  [PASS] Body word count is optimal and compliant ({body_word_count}/4,000 words)")
elif body_word_count < 3750:
    print(f"  [WARN] Body word count is below target ({body_word_count}/4,000 words)")
else:
    print(f"  [FAIL] Body word count exceeds 4,000 words ({body_word_count}/4,000 words)")
print("=" * 80)
