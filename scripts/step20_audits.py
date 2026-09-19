from pathlib import Path
import csv,hashlib,json,re,shutil
ROOT=Path(r'C:/Users/rohan/ShiftSleep-UQ');R=ROOT/'reports';P=ROOT/'paper/submissions/ieee_jbhi'
def sha(p):
 h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()
# preserve non-primary figures as optional supplementary assets
S=P/'supplementary_figures';S.mkdir(exist_ok=True)
for n in ['fig5_prediction_reliability_decoupling.pdf','fig7_conformal_transfer.pdf','fig8_stage_recall_changes.pdf']:
 src=P/'figures'/n
 if src.exists(): shutil.copy2(src,S/n)
# clean build intermediates from submission package
if (P/'build').exists(): shutil.rmtree(P/'build')
if (P/'supplement_master.tex').exists(): (P/'supplement_master.tex').unlink()
# scientific equivalence checks
can=(ROOT/'paper/main.tex').read_text(); ven=(P/'main.tex').read_text()
checks=[
 ('title', 'ShiftSleep-UQ: Calibration and Selective Reliability', 'PRESENT'),
 ('D1 C4 effect','+0.03673','PRESENT'),('D1 C5 effect','+0.18587','PRESENT'),('D2 C4 effect','+0.05992','PRESENT'),('D2 C5 effect','+0.00063','PRESENT'),
 ('D2 C5 CI low','-0.01255','PRESENT'),('D2 C5 CI high','+0.01451','PRESENT'),('D1 C4 NLL','-0.02724','PRESENT'),('D2 C5 NLL','+0.16300','PRESENT'),
 ('target-free firewall','target-free','PRESENT'),('oracle status','diagnostic rather than deployable','PRESENT'),('no SHHS','no SHHS','PRESENT'),('method gate','reliability-method gate remains not authorized','PRESENT')]
with (R/'step20_scientific_equivalence_audit.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['claim_or_field','canonical_evidence','venue_evidence','status'])
 for label,val,_ in checks:
  w.writerow([label,val,'present' if val.lower() in ven.lower() else 'absent','PASS' if val.lower() in ven.lower() else 'FAIL'])
# numerical equivalence: all important frozen literals retained
nums=['0.74800','0.66336','0.46627','0.59490','+0.03673','+0.18587','+0.05992','+0.00063','-0.02724','-0.02970','+0.00235','+0.16300','-0.05022','+0.00673','47','12','8','11','99','59','15','10','78']
with (R/'step20_numerical_equivalence_audit.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['value','canonical_present','venue_present','status'])
 for n in nums:
  variants={n,n[1:] if n.startswith('0') else n}
  ok=any(v in ven for v in variants)
  w.writerow([n,n in can,ok,'PASS' if ok else 'FAIL'])
# provenance
prov={
 'selected_venue':'IEEE Journal of Biomedical and Health Informatics',
 'venue_slug':'ieee_jbhi','canonical_main_sha256':sha(ROOT/'paper/main.pdf'),'venue_main_sha256':sha(P/'main.pdf'),'venue_supplement_sha256':sha(P/'supplement.pdf'),'canonical_supplement_sha256':sha(ROOT/'paper/supplement.pdf'),'references_sha256':sha(ROOT/'paper/references.bib'),'evidence_manifest_sha256':sha(R/'paper_evidence/paper_evidence_manifest_v1.json'),'venue_source_sha256':sha(P/'main.tex'),'official_guideline_urls':['https://www.embs.org/jbhi/for-authors/','https://www.embs.org/jbhi/prepare-and-submit-your-manuscript/','https://template-selector.ieee.org/secure/templateSelector/publicationType'],'guideline_access_date':'2026-09-19','venue_gate':'TARGET_VENUE_SELECTED','package_gate':'VENUE_PACKAGE_READY','submission_portal_action':False,'git_head':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
(R/'step20_submission_package_provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
# risk register
(R/'step20_target_venue_risk_register.md').write_text('''# IEEE JBHI target-venue risk register\n\n| Risk | Reviewer concern | Current defense | Action before submission |\n|---|---|---|---|\n| Benchmark versus method novelty | No new classifier or learned reliability method | Manuscript explicitly frames a controlled benchmark and reliability study; B0/B1 manipulation is isolated | Author confirms fit and cover letter |\n| Two-dataset generalization | Only Sleep-EDF and ISRUC are evaluated | Reciprocal directions, target-free primary evaluation, explicit scope limitation | None scientifically; retain limitation |\n| Simple architecture | Architecture is intentionally fixed and modest | This controls the causal comparison and avoids architecture confounding | Explain in cover letter |\n| No clinical deployment validation | No prospective cohort or clinical outcomes | Clinical claims are excluded; public-dataset evidence and limitations are explicit | Supply exact ethics wording |\n| No SHHS confirmation | External validity may be questioned | SHHS is explicitly listed as not evaluated | Retain non-claim |\n| Figure/page-count risk | JBHI limit is 14 pages including supplement | Derivative is 10 pages plus 2-page supplement; 5 primary figures; optional figures separated | Confirm portal interpretation |\n| Oracle interpretation | Target-label oracle could be mistaken for deployable calibration | Text labels oracle diagnostic only and target-free firewall | None |\n| Statistical-repair transparency | B0 v1.2 correction may need scrutiny | Versioned provenance, duplicate-preserving bootstrap description, audit files | Upload audit support if requested |\n| IEEE template availability | Official selector blocked non-interactive download | Official selector and requirements archived; portable two-column derivative compiled | Re-run selector/download in author environment |\n''')
(R/'step20_fallback_transfer_plan.md').write_text('''# Step 20 fallback transfer plan\n\n## Fallback 1: IEEE Transactions on Biomedical Engineering\nUse the same scientific master and preserve all B0/B1 numbers. Rewrite the abstract into the official structured Objective/Methods/Results/Conclusion/Significance format, reduce the conclusion to <=300 words, keep one review PDF under 10 MB, and revise the cover letter to foreground biomedical-engineering significance. Do not add an architecture or clinical experiment.\n\n## Fallback 2: Journal of Biomedical Informatics\nVerify the current Elsevier guide directly before transfer because ScienceDirect was inaccessible in this environment. Convert the IEEE-style derivative back to the current JBI template/style, preserve the benchmark and reliability framing, and move optional figures/tables according to the verified guide. Recheck reference style, declarations, data/code wording, and any word/page limit.\n\nThe current package does not build fallback packages.\n''')
# novelty threat
(R/'step20_novelty_threat_audit.md').write_text('''# Step 20 novelty-threat audit\n\n## Search scope\nA freshness check on 2025--2026 records queried Crossref for sleep-staging domain generalization, missing-modality sleep staging, uncertainty/calibration in sleep staging, and conformal sleep staging on 2026-09-19. This was a positioning check only; no experiment was performed.\n\n## Relevant records\n- “Cross-Sensor Domain Generalization for Non-Contact Sleep Staging,” IJCAI 2026, DOI `10.24963/ijcai.2026/473`: relevant to domain generalization and sleep staging, but it uses a non-contact cross-sensor setting and does not reproduce this paper’s reciprocal Sleep-EDF/ISRUC compound missing-modality reliability benchmark. It does not invalidate the narrower positioning.\n- “Cross-Validation and Normalization in EEG Sleep Staging: Impacts on Generalization, Calibration, and Clinical Validity,” 2026, DOI `10.29130/dubited.1773372`: relevant to calibration/generalization concerns, but not an overlapping B0/B1 compound-shift benchmark. It reinforces the manuscript’s caution about protocol and normalization.\n- “Trustworthy Sleep Staging from EEG: Deep Ensembles, MC Dropout, and Predictive Calibration,” 2025, DOI `10.1101/2025.08.23.671918`: a preprint record, not treated as a verified peer-reviewed addition. Its topic is adjacent, but it does not require a claim change.\n\n## Decision\nNo new citation was inserted because the verified bibliography already covers the manuscript’s relevant literature, and none of the screened records creates a direct claim collision. The manuscript remains conservative: it does not claim the first sleep domain-generalization study, the first uncertainty study, or a universal benchmark.\n''')
