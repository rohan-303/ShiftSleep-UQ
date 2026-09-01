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
