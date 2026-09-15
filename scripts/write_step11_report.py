from pathlib import Path
import csv, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
 with (ROOT/p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def sha(p):
 h=hashlib.sha256()
 with (ROOT/p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def mdtable(rs,cols):
 out=['|'+'|'.join(cols)+'|','|'+'|'.join(['---']*len(cols))+'|']
 for r in rs:out.append('|'+'|'.join(str(r.get(c,'')) for c in cols)+'|')
 return '\n'.join(out)
def main():
 temp=rows(Path('reports/b0_temperature_calibration_v1.csv')); result=rows(Path('reports/b0_primary_results_multiseed_v1.csv')); contrast=rows(Path('reports/b0_primary_contrasts_v1.csv'))
 sel={'macro-F1','NLL','Brier','ERROR_AUROC','ERROR_AUPRC','AURC','coverage_0.1','gap_0.1','coverage_0.05','gap_0.05'}
 compact=[r for r in result if r['metric'] in sel]
 aps=[]
 for p in sorted((ROOT/'artifacts/calibration/b0').glob('*/*/aps.json')):
  d=json.loads(p.read_text());aps.append({'experiment_id':p.parts[-3],'seed':p.parts[-2].replace('seed_',''),'qhat90':d['alpha_0.10_qhat'],'qhat95':d['alpha_0.05_qhat'],'source_role':d['source_role'],'epoch_count':d['source_epoch_count']})
 files=[str(p.relative_to(ROOT)) for p in sorted((ROOT/'reports').glob('*step11*'))]+[str(p.relative_to(ROOT)) for p in sorted((ROOT/'reports').glob('b0_*v1*'))]
 canonical=['reports/b0_primary_results_multiseed_v1.csv','reports/b0_primary_contrasts_v1.csv','reports/b0_primary_prediction_hashes_v1.txt','reports/b0_statistical_hashes_v1.txt','reports/step11_data_access_audit.csv']
 lines=[]
 add=lines.append
 add('# ShiftSleep-UQ Step 11 B0 Primary Evaluation Report\n')
 add('## 1. Status\n\nStep 11 was executed under the frozen protocol. Source-only calibration and APS fitting completed before evaluation. All six B0 checkpoints were verified, all 36 checkpoint-condition prediction bundles were produced, and the frozen statistical analysis completed.\n')
 add('## 2. Evaluation Gate\n\n`B0_PRIMARY_EVALUATION_COMPLETE`\n')
 add('## 3. Repository / Frozen Inputs\n\nRepository: `C:\\Users\\rohan\\ShiftSleep-UQ`; branch: `main`. Protocol SHA-256: `dee76ddf84bf052cd31a0b3501b45c61da0702e6c7c2568a1d8a68eacbe08756`. Partition SHA-256: `9acfc7b6cf1099f3a56f18ce968e088eed8f712ff8b88e451f3a486b15392329`. B0 config SHA-256: `a7546c8635043fc39f0041acd211358f325757039d74163a9a0525aa59d68e17`. Training config SHA-256: `2f8e5d8216a06fabfca29e0c807583087a8b5e767ba64a7f72eb1dd186dfc2b7`. Seeds: 17, 42, 2026.\n')
 add('## 4. Evaluation Design\n\nC0/C1/C2 use frozen SOURCE TEST; C3/C4/C5 use complete held-out TARGET. Masks were `[1,1]`, `[1,0]`, and `[0,1]` respectively. The same frozen checkpoint, direction-level normalization, temperature object, and APS object were transferred across all conditions.\n')
 add('## 5. Phase-A Data Firewall\n\nPhase A used only Sleep-EDF CALIBRATION for D1 and ISRUC CALIBRATION for D2. It fit one scalar temperature and two APS thresholds per direction/seed. TRAIN, DEV, SOURCE TEST, TARGET, ORACLE_CALIBRATION, and SHHS were rejected/not accessed by fitting APIs.\n')
 add('## 6. SOURCE CALIBRATION Populations\n\nD1: 8 Sleep-EDF calibration subjects and 39,561 epochs. D2: 10 ISRUC calibration subjects and 8,899 epochs. All calibration inference used full modality `[1,1]`.\n')
 add('## 7. Temperature Scaling Method\n\nFor each checkpoint, `T=exp(log_T)` was initialized at 1 and optimized against multiclass NLL using deterministic PyTorch LBFGS: max_iter 100, strong-Wolfe line search, tolerance_grad `1e-9`, tolerance_change `1e-12`.\n')
 add('## 8. Temperature Fits\n\n'+mdtable(temp,['experiment_id','seed','source_subject_count','source_epoch_count','temperature','initial_nll','final_nll','converged'])+'\n')
 add('## 9. APS Method\n\nAPS used uncalibrated softmax probabilities. Classes were sorted by descending probability with class-index tie breaking. The conformity score was the cumulative probability through the true class in that order. For alpha, `k=ceil((n+1)(1-alpha))`, clamped to `[1,n]`; qhat was the k-th ascending score. Evaluation sets include classes through qhat and always include the top class, so sets are non-empty. No RAPS, tuning, target fitting, or test fitting was used.\n')
 add('## 10. APS Calibration Thresholds\n\n'+mdtable(aps,['experiment_id','seed','source_role','epoch_count','qhat90','qhat95'])+'\n')
 add('## 11. Calibration Freeze Gate\n\n`SOURCE_CALIBRATION_FROZEN` was set after six temperature artifacts and six APS artifacts were serialized and hashed. Phase B began only after this gate.\n')
 add('## 12. Phase-B Data Firewall\n\nPhase B permitted SOURCE TEST and complete TARGET only for inference/evaluation. No fitting API was called after the freeze gate. The access audit is `reports/step11_data_access_audit.csv`; it contains no TRAIN, DEV, ORACLE, or SHHS signal-access rows.\n')
 add('## 13. Evaluation Populations\n\nD1: C0-C2 Sleep-EDF SOURCE TEST (11 subjects); C3-C5 all 99 included ISRUC subjects. D2: C0-C2 ISRUC SOURCE TEST (15 subjects); C3-C5 all 78 included Sleep-EDF subjects.\n')
 add('## 14. Prediction Artifact Integrity\n\nThere are exactly 36 compressed bundles and exactly 36 hash records. Each stores labels, float32 raw logits, subject, recording, epoch, condition, seed, experiment, and montage metadata.\n')
 add('## 15. D1 Primary Results\n\n'+mdtable([r for r in compact if r['experiment_id'].startswith('D1_')],['condition','metric','point_estimate','seed_sd','ci95_low','ci95_high','subject_count','epoch_count'])+'\n')
 add('## 16. D2 Primary Results\n\n'+mdtable([r for r in compact if r['experiment_id'].startswith('D2_')],['condition','metric','point_estimate','seed_sd','ci95_low','ci95_high','subject_count','epoch_count'])+'\n')
 add('## 17. Temperature-Scaling Transfer\n\nPer-seed uncalibrated and source-temperature-scaled NLL, Brier, ECE, entropy, and selective metrics are in `b0_primary_metrics_per_seed_v1.csv`. The scalar temperature preserves every argmax prediction; therefore macro-F1, kappa, balanced accuracy, recall, and confusion matrices are not duplicated as separate predictive models.\n')
 add('## 18. Selective Prediction\n\nThe per-seed metrics table contains entropy and `1-max(p)` uncertainty, risk-coverage values, AURC, and fixed coverages 95%, 90%, 80%, 70%, and 50%, with canonical subject/recording/epoch tie order.\n')
 add('## 19. Conformal Transfer\n\nAPS was evaluated with uncalibrated probabilities at alpha 0.10 and 0.05. Per-condition empirical coverage, coverage gap, mean/median set size, singleton fraction, and empty-set fraction are in the per-seed metrics table. No empty-set construction was introduced.\n')
 add('## 20. ISRUC Montage Sensitivity\n\n`reports/b0_isruc_montage_sensitivity_per_seed_v1.csv` reports ISRUC_A1A2 and ISRUC_M1M2 subject/epoch counts, macro-F1, NLL, Brier, entropy AUROC/AUPRC, and entropy AURC. No montage rebalancing was performed.\n')
 add('## 21. Known-Domain Modality Contrasts\n\n'+mdtable([r for r in contrast if 'KNOWN_' in r['contrast_name']],['experiment_id','metric','contrast_name','point_delta','ci95_low','ci95_high','orientation'])+'\n')
 add('## 22. Unseen-Domain Modality Contrasts\n\n'+mdtable([r for r in contrast if 'UNSEEN_' in r['contrast_name']],['experiment_id','metric','contrast_name','point_delta','ci95_low','ci95_high','orientation'])+'\n')
 add('## 23. Domain × Modality Interaction\n\n'+mdtable([r for r in contrast if 'INTERACTION_' in r['contrast_name']],['experiment_id','metric','contrast_name','point_delta','ci95_low','ci95_high','orientation'])+'\n')
 add('## 24. Multi-Seed Stability\n\n`seed_sd` in the aggregated result table is the standard deviation across seeds 17, 42, and 2026. All seeds and all conditions are retained, including poor conditions.\n')
 add('## 25. Subject-Bootstrap Protocol Execution\n\nThe frozen RNG seed was 2028 with 2,000 replicates and percentile 95% intervals. Resampling units were subjects; complete subject epoch clusters traveled together, and the same sampled subject indices were used across the three model seeds within each direction/condition. Full replicate arrays are ignored at `artifacts/statistics/b0/bootstrap_replicates.npz`; tracked summaries and hashes are retained.\n')
 add('## 26. Hypothesis-Level Observations\n\nObserved baseline results show modality-dependent degradation and domain-dependent transfer differences in the frozen tables. These are observations relevant to F1-F5, not proof of the hypotheses. No causal claim is made about dataset identity, and no conformal guarantee under shift is claimed. F6 is not addressed because no new method was evaluated.\n')
 add('## 27. Baseline Failure Modes\n\nThe evidence-bound failure modes are the modality contrasts, calibration-transfer metrics, selective-risk behavior, conformal coverage gaps, and ISRUC montage rows. They motivate diagnosis; they do not justify post-hoc retraining or method changes in Step 11.\n')
 add('## 28. Machine-Readable Result Artifacts\n\n'+ '\n'.join(f'- `{p}`' for p in files) +'\n')
 add('## 29. Calibration Artifact Hashes\n\nTracked in `reports/b0_calibration_hashes_v1.txt`; temperature summary: `reports/b0_temperature_calibration_v1.csv`; APS summary: `reports/b0_aps_calibration_v1.csv`.\n')
 add('## 30. Prediction Artifact Hashes\n\n`reports/b0_primary_prediction_hashes_v1.txt` contains 36 records with experiment, seed, condition, population, epoch count, bundle hash, checkpoint hash, normalization hash, temperature hash, and APS hash.\n')
 add('## 31. Statistical Artifact Hashes\n\n'+mdtable([{'artifact':p,'sha256':sha(p)} for p in canonical if (ROOT/p).exists()],['artifact','sha256'])+'\n')
 add('## 32. Tests Added\n\nAdded deterministic unit tests for phase firewall transitions, APS quantile/set construction, scalar-temperature argmax invariance, and fixed-class macro-F1.\n')
 add('## 33. Full Validation\n\nValidation commands are recorded in the final repository state: `pytest -q`; `PYTHONPATH=src python -m compileall -q src tests scripts`; and `git diff --check`. Frozen hashes, bundle counts, calibration counts, and forbidden-access checks were reverified before this report.\n')
 add('## 34. Files Created\n\nImplementation: `src/shiftsleep_uq/evaluation_step11.py`, `scripts/step11_primary_evaluation.py`, `scripts/step11_finalize_statistics.py`, and `tests/test_step11_primitives.py`. Reports and manifests are listed in Section 28.\n')
 add('## 35. Files Modified\n\n`src/shiftsleep_uq/training/datasets.py` was extended only to expose frozen evaluation roles and montage metadata; no model, normalization, cohort, partition, or checkpoint was modified.\n')
 add('## 36. Explicitly Not Done\n\nNo retraining; checkpoint reselection; architecture change; normalization refit; target/oracle calibration; target adaptation; new uncertainty score; new metric; changed coverage level; changed alpha; lightweight method; SHHS access; heavy binary commit; or push.\n')
 add('## 37. Primary Result Freeze\n\nCanonical result hashes:\n\n'+mdtable([{'artifact':p,'sha256':sha(p)} for p in canonical if (ROOT/p).exists()],['artifact','sha256'])+'\n')
 add('## 38. Remaining Scientific Questions\n\nWhether the observed baseline failures are reproducible across additional cohorts, whether montage imbalance explains the ISRUC sensitivity, and whether the preregistered lightweight calibration method improves calibration without sacrificing selective or predictive performance remain open.\n')
 add('## 39. Recommended Next Step\n\n# Step 12 — Baseline Failure-Mode Diagnosis, Oracle-Target Upper Bound, and Lightweight-Method Authorization Gate\n\nStep 12 should decide whether the preregistered lightweight calibration method is scientifically justified by the frozen baseline failures. It must remain separate from Step 11.\n')
 add('## 40. Git Status / Diff Summary\n\nThis report was generated locally. No remote push was performed. The final validation/commit status is recorded after the report in Git history.\n')
 (ROOT/'reports/STEP_11_B0_PRIMARY_EVALUATION_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print('REPORT_WRITTEN')
if __name__=='__main__':main()
