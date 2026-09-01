# ShiftSleep-UQ Agent Instructions

- Never fabricate results, dataset metadata, citations, or performance numbers.
- Never silently modify a frozen experimental protocol; record changes in `docs/decisions.md`.
- Never use test labels for model selection, threshold tuning, calibration selection, or checkpoint selection.
- Preserve raw data and treat it as immutable; record provenance and checksums where legally permissible.
- All experiments must be config-driven and reproducible.
- Every major research step produces a report under `reports/`.
- Log assumptions, unresolved semantics, and decisions explicitly.
- Tests and integrity checks must accompany implementation.
- Stop and report rather than guessing about ambiguous dataset, channel, label, or licensing semantics.
- Do not download datasets or train models during documentation-only milestones.
