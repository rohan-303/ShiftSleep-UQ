# Dataset and channel-harmonization audit

**Status: PARTIAL GATE.** No dataset was downloaded. This audit uses official landing/documentation pages only; exact signal inventories for ISRUC and SHHS remain unresolved.

## Harmonization matrix

| Dataset/domain | EEG candidate | EEG reference | EOG candidate | EMG candidate | sampling | scoring | compatibility |
|---|---|---|---|---|---|---|---|
| Sleep-EDF SC | Fpz-Cz, Pz-Oz | bipolar placements stated by official page | horizontal EOG | submental chin EMG envelope | EEG/EOG 100 Hz; EMG 1 Hz | R&K | Level A clear; Level B limited; Level C not equivalent to raw EMG datasets |
| Sleep-EDF ST | EEG channels on PSG page; exact lead detail beyond common page NOT_VERIFIED | NOT_VERIFIED | EOG | chin EMG | EEG/EOG/EMG 100 Hz | R&K | separate domain candidate; exact lead/reference audit required |
| SHHS | official montage/sampling manuals exist; exact leads not frozen | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | cannot freeze until manual/channel extraction |
| ISRUC | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | excluded from primary until official access/audit |
| CAP | at least 3 EEG, including F3/F4, C3/C4, O1/O2 referred A1/A2 | A1/A2 references stated | 2 EOG | submentalis + bilateral anterior tibial EMG | NOT_VERIFIED on page | R&K plus CAP/Terzano annotations | Level A possible; Level B conditional; Level C not recommended |

## Levels

- **Level A: modality-family harmonization.** Assign dataset-specific signals to EEG/EOG/EMG families while preserving lead/reference/device metadata and treating them as part of domain shift. Scientifically feasible, but performance may reflect montage differences.
- **Level B: approximate anatomical harmonization.** Restrict to signals with reasonably comparable anatomical roles and explicitly record references. Preferred if the source audit supports it; still does not erase acquisition differences.
- **Level C: exact channel harmonization.** Require highly similar leads, references, sampling, and signal representation. Strongest comparability but likely excludes useful datasets and is not currently supportable across all candidates.

**Provisional decision:** do not freeze channel names yet. The defensible next gate is Level A for exploratory feasibility, followed by a narrower Level B primary track if official manuals establish comparable signals. Level C should be a sensitivity track only if enough data survive. Dataset/device/montage differences are scientifically defensible components of dataset shift, but must be disclosed rather than treated as nuisance-free domain invariance.

## Synthetic versus structural missingness

Synthetic missingness masks an available original modality at evaluation time. Structural mismatch means a signal was never acquired, is unavailable, or is not harmonizable. The benchmark must report these separately; synthetic masking tests robustness to deployment loss, while structural mismatch tests cross-dataset acquisition differences and cannot be interpreted as a controlled modality ablation.

## Sources
[1] https://physionet.org/content/sleep-edfx/1.0.0/
[2] https://physionet.org/content/capslpdb/1.0.0/
[3] https://sleepdata.org/datasets/shhs
