# Benchmark specification (draft)

**Status: PROVISIONAL — must be frozen only after source, annotation, channel, duplicate, and licensing audits.**

## Axes
- within-domain vs unseen-domain;
- full vs missing modality;
- single vs compound shift;
- explicit modality masks;
- dataset leave-one-domain-out evaluation;
- subject-independent train/dev/test splits;
- source-only vs oracle calibration.

## Deployment levels
- **S0:** known domain + full modalities.
- **S1:** known domain + missing modality.
- **S2:** unseen dataset/domain + full modalities.
- **S3:** unseen dataset/domain + one missing modality.
- **S4:** unseen dataset/domain + multiple missing modalities.

## Candidate shared families
EEG, EOG, and EMG are candidate families only. Exact channel equivalence, montage, sampling-rate compatibility, signal availability, and masking semantics are unresolved.

## Candidate datasets
Sleep-EDF Expanded, ISRUC-Sleep, SHHS, and CAP Sleep Database or another appropriately harmonizable external dataset. Names are candidates, not verified inclusion decisions.

## Label space
Wake, N1, N2, N3, REM is provisional. R&K versus AASM conventions, S3/S4 mappings, unknown/artifact labels, epoch duration, and annotation adjudication require audit.

## Calibration regimes
A. **SOURCE-ONLY / TARGET-FREE:** calibration uses only source TRAIN/DEV information; strict main setting.
B. **CROSS-SOURCE CALIBRATION:** strategy developed across multiple source domains without held-out-target labels.
C. **ORACLE TARGET CALIBRATION:** labeled target sample permitted only as explicitly named upper bound.

## Unresolved gates
Channel harmonization, label mapping, dataset overlap/duplicate recordings, subject metadata availability, legal terms, target-free calibration design, missingness mechanism, and exact split cardinalities remain TODO/VERIFY.
