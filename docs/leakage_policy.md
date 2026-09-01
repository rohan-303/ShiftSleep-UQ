# Leakage policy and checklist

Every future experiment must pass this checklist and retain the evidence in its report.

- [ ] Subject IDs are canonicalized and disjoint across train/dev/test.
- [ ] No epoch-level random splitting is used.
- [ ] Repeated recordings, duplicates, and overlapping cohorts are audited.
- [ ] Preprocessing, normalization, feature selection, representation fitting, and imputation are fit on TRAIN only (or TRAIN/DEV only when explicitly specified), never test.
- [ ] No test performance is used for checkpoint, hyperparameter, threshold, architecture, or calibration selection.
- [ ] Strict target-free calibration uses no target labels; any target-label calibration is labeled ORACLE / UPPER BOUND.
- [ ] Dataset overlap and duplicate recordings are checked where applicable.
- [ ] Demographic leakage or demographic invariance claims are not made without supported metadata and analysis.
- [ ] Seeds, split manifests, code revision, environment, and configs are recorded.
- [ ] Test access is logged only after protocol freeze.

Fail closed on an unresolvable identity collision, ambiguous subject mapping, or unexplained target-label access.

## Step 4 source-supported additions (2026-09-01)

* Sleep-EDF SC subject identity is derived from the official `SC4<ss><N>...` filename convention; all nights for one SC subject remain together.
* Sleep-EDF ST subject identity is derived from the official `ST7<ss><N>...` filename convention; both treatment/placebo nights remain together.
* Sleep-EDF-derived subsets cannot be treated as independent domains without release-lineage verification.
* CAP pathology-coded filenames are not accepted as subject IDs.
* SHHS visit grouping and ISRUC grouping remain unresolved until official access/schema evidence is available.
