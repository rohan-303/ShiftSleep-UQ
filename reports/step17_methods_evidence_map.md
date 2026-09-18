# Methods Evidence Map

- Datasets/cohorts: frozen cohort manifests, `reports/subject_partitions_v2.csv`, Table 1.
- Preprocessing/partitions: frozen configs and partition manifests; no Step 17 changes.
- B0 architecture/training: frozen B0 reports and checkpoint manifests.
- B1 intervention: `reports/b1_training_summary_v1.csv`, frozen B1 protocol.
- Calibration/conformal: frozen B1 artifacts; Step 16 mask-specific diagnostics are secondary.
- Shift conditions: C0–C5 definitions in Table 1.
- Metrics: frozen evaluation implementation and primary result tables.
- Bootstrap: subject-level duplicate-preserving 2,000-replicate engine, seed 2028.
- B0 v1.2 repair: Step 15.2.3 repair and engine-gate artifacts.
- Step 16 diagnostics: residual matrix, source-mask comparison, oracle diagnostic table, method gate.
