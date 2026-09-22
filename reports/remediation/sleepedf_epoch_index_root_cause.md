# Sleep-EDF epoch-index root cause (Step 20.2.2)

## Finding

The historical `data/processed/core_v1_1/sleep_edf_sc__*__core_v1.npz` files contain a `source_epoch_indices` array, but that field is not a physical original 30-second epoch index. In the frozen preprocessing implementation, `expand_annotations()` constructs each `EpochLabel` with `source_index=i`, where `i` is the annotation-event ordinal. `preprocess.py` then serializes `x.source_index` for every retained 30-second expansion. Consequently, one long annotation assigns the same event ordinal to many epochs; in the observed processed Sleep-EDF ledgers the serialized values are constant zero.

The same implementation does preserve `epoch_onsets_seconds` and uses those onset values to slice the raw signal. The canonical processed labels therefore retain the temporal sequence, but the intended physical epoch ledger was not serialized.

## Provenance-preserving repair

Step 20.2.2 reconstructs physical indices from the official PhysioNet Sleep-EDF hypnogram EDF+ annotations, using the repository's frozen `sleep_edf_pairing_audit.csv` recording-to-hypnogram mapping. For every scored annotation whose onset and duration are aligned to 30-second boundaries, the reconstruction expands the event into 30-second rows and assigns:

`source_epoch_index = round(annotation_onset_seconds / 30) + within_annotation_offset`

The reconstructed label sequence is required to equal the processed `labels` sequence exactly. The repaired derivative retains the original EEG, EOG, labels, epoch onsets, and metadata arrays byte-for-byte in value; only `source_epoch_indices` is replaced. Trailing annotation epochs beyond the processed signal-supported prefix are not added.

## Gate

The reconstruction is accepted only when every one of the 153 included recordings passes strict-increasing/unique/nonnegative index checks and exact processed-label prefix matching. The historical NPZ files remain untouched; repaired derivatives are written under `artifacts/remediation/ledger_repair/sleepedf_epoch_ledger_v2/`.
