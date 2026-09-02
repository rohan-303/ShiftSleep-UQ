# ISRUC-S1 channel-schema evidence

## Scope and evidence date

This record supports ShiftSleep-UQ Step 7.6. It distinguishes documented nominal schema from the exact raw headers observed in the 35 complete original-provider Subgroup-1 recordings I001–I035. Accessed 2026-09-02. No acquisition or contract change was performed.

## Documented nominal schema

1. **Original dataset paper.** Khalighi et al., *ISRUC-Sleep: A comprehensive public dataset for sleep researchers*, Computer Methods and Programs in Biomedicine 124 (2016), 180–192. PubMed record PMID 26589468: <https://pubmed.ncbi.nlm.nih.gov/26589468/>. The paper is the primary dataset reference. The PubMed landing page was available for the bibliographic record, although its abstract page required cookies in this environment.

2. **Peer-reviewed explicit Subgroup-1 description.** The open peer-reviewed article *Automatic and Accurate Sleep Stage Classification via a Convolutional Deep Neural Network and Nanomembrane Electrodes* (Biosensors, 2022), Methods §2.1, states that 100 Subgroup-1 subjects were used; each recording contained six EEG channels `C3-A2`, `C4-A1`, `F3-A2`, `O1-A2`, `O2-A1`, `F4-A1`, two EOG channels `LOC-A2`, `ROC-A1`, and three EMG channels. It states a recording rate of 200 Hz. Source: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8946692/>.

3. **Dataset-structure/channel reference implementation.** TorchEEG's ISRUC dataset documentation identifies Group 1 as 100 subjects, gives the official-style `Subgroup_1/<subject>/<subject>.rec` and `<subject>_1.txt` structure, and lists the nominal labels including `C3-A2`, `C4-A1`, `F3-A2`, `F4-A1`, `LOC-A2`, `O1-A2`, `O2-A1`, and `ROC-A1`. Its default example also exposes M1/M2 labels (`F3-M2`, `C3-M2`, etc.), which is treated here as corroborating implementation evidence of representation variation, not as permission to map montages. Source: <https://torcheeg.readthedocs.io/en/stable/generated/torcheeg.datasets.ISRUCDataset.html>.

### Interpretation boundary

The peer-reviewed description establishes the nominal/documented schema and rate. It does not, by itself, prove that every exported REC header must use the exact A1/A2 strings. Therefore the observed M1/M2 headers are not silently relabeled and remain a scientific-contract review issue.

## Observed raw schema

The independent parser read the EDF/REC fixed header directly: fixed header 256 bytes; `ns` at bytes 252–255; signal-label fields as `16 × ns` bytes immediately after the fixed header; followed by the remaining EDF per-signal fields. Across I001–I035:

- 35/35 REC bodies passed the independently computed byte-length check.
- 672 signal fields were inspected.
- All label fields were ASCII, had only legal trailing ASCII-space padding, and had no NULs, tabs, non-ASCII bytes, embedded controls, or Unicode/hyphen variants.
- 17 subjects contain exact `C3-A2` and exact `LOC-A2`.
- 18 subjects contain neither exact label; all 18 contain explicit M1/M2-style montage labels, including `C3-M2` and `LOC`-side `E1-M2`/`E2-M1` EOG-style channels rather than `LOC-A2`.
- The project parser and pyedflib agree with the independent raw parser for all 35 subjects and all 672 fields.

Exact inventories, raw bytes, header calibration fields, schema fingerprints, and identity checks are recorded in the Step 7.6 CSV artifacts listed in the report.

## Conclusion

The apparent exclusions are not caused by EDF label padding, encoding, field-offset parsing, pyedflib disagreement, or corrupted REC bodies. They are real source-header label/montage variants in this acquired cohort. Because the documented nominal schema and observed source variants are not identical, the exact-channel contract must not be broadened in Step 7.6. Gate: `CHANNEL_CONTRACT_REVIEW_REQUIRED`.
