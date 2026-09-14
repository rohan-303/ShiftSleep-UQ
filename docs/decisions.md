# Architecture and research decision log

Append-only. Dates use the local project date recorded at creation; later changes require a new decision entry.

## D001 — Benchmark-first rather than architecture-first
**Date:** 2026-09-01. Establish the leakage-safe protocol and benchmark before proposing model architecture.

## D002 — Reliability under compound shift is primary
**Date:** 2026-09-01. The primary scientific concern is uncertainty/reliability under dataset plus missing-modality shift, not accuracy alone.

## D003 — Candidate modality families
**Date:** 2026-09-01. EEG/EOG/EMG are candidate shared modality families pending data audit.

## D004 — Provisional five-class harmonization
**Date:** 2026-09-01. Wake/N1/N2/N3/REM is provisional pending annotation audit.

## D005 — Target-free calibration is main setting
**Date:** 2026-09-01. Source-only/target-free calibration is the strict deployment setting.

## D006 — Oracle target calibration is separated upper bound
**Date:** 2026-09-01. Target calibration is allowed only when explicitly labeled ORACLE / UPPER BOUND.

## D007 — New method is conditional
**Date:** 2026-09-01. Introduce at most one lightweight calibration method only if baseline evidence identifies a specific failure mode.

## D008 — Adopt exact source-supported ISRUC montage families
**Date:** 2026-09-02. Step 7.7 adopts an exact allowlist of `C3-A2` + `LOC-A2` and `C3-M2` + `E1-M2` as distinct ISRUC source-supported channel families. Exact derivations remain metadata; no electrode or numerical equivalence is claimed. Future ISRUC reliability results must be montage-stratified. This protocol amendment was made before modeling and without model or target results.

## D009 — Independent source-test population for known-domain C0–C2
**Date:** 2026-09-14. Step 8.1 amends the pre-model source roles to TRAIN 60%, DEV 15%, CALIBRATION 10%, and TEST 15%. C0–C2 use the untouched SOURCE TEST population; C3–C5 continue to use complete held-out TARGET populations. TEST cannot influence fitting, normalization, selection, temperature scaling, conformal calibration, or thresholds. Cohorts, C0–C5 meanings, metrics, seeds, oracle protocol, and montage contract are unchanged.