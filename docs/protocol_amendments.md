# Protocol Amendments

Step 5 records amendments without rewriting Steps 1–4.

| ID | DATE | OLD | NEW | EVIDENCE | REASON | AFFECTS_HYPOTHESIS? | AFFECTS_PAPER_CLAIM? |
|---|---|---|---|---|---|---|---|
| A-05-01 | 2026-09-01 | Primary EEG+EOG+EMG assumed | Primary EEG+EOG; EMG secondary compatible-subset only | Step 4 SC 1-Hz RMS versus ST 100-Hz; SHHS nominal 125/128-Hz EMG | Avoid false representation equivalence | Yes, modality factor is EEG/EOG in primary | Yes, primary benchmark scope |
| A-05-02 | 2026-09-01 | S0–S4, including multiple-primary-modality-missing S4 | C0–C5; no condition removes both EEG and EOG | Primary input must remain nonempty | Removes incoherent all-primary-modality absence | Yes | Yes |
| A-05-03 | 2026-09-01 | SC/ST candidate pooling | SC primary provisional; ST secondary medication/acquisition stress | Step 4 identity, repeated-night and schema audit | Prevent cohort/EMG confounding | Yes | Yes |
| A-05-04 | 2026-09-01 | ISRUC cohorts treated as one candidate | ISRUC-S1/S2/S3 separate roles; ISRUC deferred pending original semantics | Official ISRUC site and NEMAR v1.0.1 metadata | Preserve cohort and repeated-session identity | Yes | Yes |
| A-05-05 | 2026-09-01 | SHHS schema not verified | Public schema verified; raw access pending and conditional | Official NSRR pages and montage tables | Separate metadata verification from acquisition | No | Yes |
| A-05-06 | 2026-09-01 | Label mapping provisional | R&K 3+4 -> N3; non-stage labels excluded, never Wake | AASM transition evidence and audited annotations | Prevent label leakage/misclassification | Yes | Yes |
| A-05-07 | 2026-09-01 | Label-derived wake trimming available as possible primary practice | Preserve all valid scored epochs including Wake; trimming secondary only | Target-free design and Step 4 audit | Avoid target-label-dependent input selection | Yes | Yes |

The contract remains partial because source-specific ISRUC/SHHS annotation and required-channel semantics are not all closed.
