# Modality-family contract proposal

This is a proposal, not a frozen Step 5 contract. No resampling, filtering, re-referencing, or signal transformation is authorized.

| Dataset/substudy | EEG | EOG | EMG | Classification |
|---|---|---|---|---|
| Sleep-EDF SC | Fpz-Cz, Pz-Oz; 100 Hz; references encoded in bipolar labels | horizontal EOG; 100 Hz | submental 1-Hz processed RMS envelope | EEG/EOG COMPATIBLE_WITH_SHIFT; EMG QUESTIONABLE |
| Sleep-EDF ST | Fpz-Cz, Pz-Oz; 100 Hz | horizontal EOG; 100 Hz | submental 100 Hz; representation differs from SC | EEG/EOG COMPATIBLE_WITH_SHIFT; EMG QUESTIONABLE |
| CAP | heterogeneous F3/F4, C3/C4, O1/O2 referenced to A1/A2 plus bipolar EEG; EOG and EMG labels vary; frequencies vary | ROC-LOC/LOC-ROC observed in inspected headers | EMG1-EMG2 submentalis and tibial channels where present; frequencies vary | EEG/EOG/EMG QUESTIONABLE pending complete audit |
| SHHS | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |
| ISRUC S1/S2/S3 | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED | NOT_VERIFIED |

## Proposed primary interpretation
The defensible candidate is modality-family EEG+EOG, with structural channel mismatch retained as domain shift. EMG is secondary or a separately analyzed missing-modality stress condition because SC is a 1-Hz processed envelope and ST is 100-Hz EMG. CAP is not exact-channel compatible with Sleep-EDF and should remain external until its full schema is audited.

`COMPATIBLE_WITH_SHIFT` means the physiological family is comparable but montage/reference/device differences are intentionally retained as domain shift; it does not excuse fundamentally different representations. All unverified pairs remain NOT_VERIFIED.
