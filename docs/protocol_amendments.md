# Step 5.1 Protocol Amendments

## A-05.1-01 — Freeze ISRUC-S1 primary channel pair

* OLD: ISRUC exact EEG/EOG semantics and primary channels unresolved.
* NEW: ISRUC-S1 primary EEG is `C3-A2`; primary EOG is `LOC-A2`; no fallback. A missing exact channel is a structural mismatch.
* EVIDENCE: Khalighi et al. (2016), DOI 10.1016/j.cmpb.2015.10.013; peer-reviewed PMC8946692 Section 2.1; NEMAR v1.0.1 representative S1 sidecar.
* IMPACT: permits accessible-core preprocessing engineering; retains montage/reference domain shift.

## A-05.1-02 — Freeze ISRUC scorer policy

* OLD: scorer stream unset; disagreement appeared as a primary exclusion.
* NEW: scorer 1 is primary ISRUC gold, predeclared before experiments. Scorer 2 is secondary for agreement, disagreement sensitivity, and uncertainty-vs-human-disagreement diagnostics. Valid scorer-1 epochs remain primary training/evaluation epochs when scorer 2 disagrees. Consensus-only analysis is secondary.
* EVIDENCE: NEMAR v1.0.1 README explicitly states scorer-1 Excel files generate events and scorer-2 labels are annotation extras; official ISRUC site documents two experts.
* IMPACT: preserves difficult valid epochs and prevents model-selected labels.

## A-05.1-03 — Correct disagreement exclusion

* OLD: `scorer_disagreement` was in the primary exclusion list.
* NEW: it is removed from primary exclusions. Only invalid/unscored/non-stage/alignment failures are primary exclusions.
* IMPACT: primary benchmark is not artificially simplified.

## A-05.1-04 — Add core/final freeze levels

* OLD: one partial contract gate conflated preprocessing readiness and final three-domain readiness.
* NEW: `CORE_PREPROCESSING_FROZEN` covers Sleep-EDF SC + ISRUC-S1; `FINAL_BENCHMARK_FROZEN` requires acquired and per-record-validated SHHS1.
* IMPACT: deterministic engineering may begin without weakening the three-domain paper goal.

## A-05.1-05 — Freeze intended SHHS1 schema, retain access gate

* OLD: SHHS candidates were unresolved and access was pending.
* NEW: intended SHHS1 channels are `C3-A2` EEG (nominal 125 Hz) and `EOG(L)-PG1` (nominal 50 Hz), with mandatory per-record validation; role remains planned primary pending authorized access.
* IMPACT: future inclusion does not require changing canonical modality/label contract.

## A-05.1-06 — Freeze modality-family, not electrode-equivalence, harmonization

* OLD: cross-dataset channel comparison remained provisional.
* NEW: EEG and EOG are harmonized as modality families while montage/reference differences remain explicit domain shift; no exact anatomical equivalence is claimed across Sleep-EDF, ISRUC, and SHHS.

## A-07.7-01 — ISRUC Source-Supported Montage-Family Harmonization

* DISCOVERED: Step 7.6 established before modeling that 17/35 body-valid original-provider ISRUC-S1 recordings use exact `C3-A2` + `LOC-A2`, while 18/35 use exact `C3-M2` + `E1-M2` with `E2-M1` as companion EOG context. Independent raw EDF parsing, pyedflib, and the project parser agreed on all inspected fields.
* OLD: ISRUC primary EEG was exact `C3-A2`; ISRUC primary EOG was exact `LOC-A2`; alternate M1/M2 records were structurally excluded.
* NEW: ISRUC EEG role is `LEFT_CENTRAL_EEG`, accepting only exact `C3-A2` or exact `C3-M2`; ISRUC EOG role is `LEFT_OCULAR_EOG`, accepting only exact `LOC-A2` or exact `E1-M2`.
* EVIDENCE: AAST Standard Polysomnography technical guideline (which identifies AASM technical specifications as its basis) describes central EEG derivations including `C3-M2`, EOG electrodes E1/E2 at the outer canthi, and M2/M1 reference conventions; ISRUC peer-reviewed schema descriptions identify `C3-A2` and `LOC-A2`; Step 7.6 raw headers show the two exact source families.
* DECISION: `ADOPT_SOURCE_SUPPORTED_CHANNEL_FAMILY`.
* LIMITS: same physiological role is supported; exact physical placement and numerical equivalence are not claimed. Exact source derivations remain mandatory metadata. No mathematical re-reference, renaming, aliasing, or fuzzy matching is allowed.
* STRATUM: `ISRUC_A1A2` and `ISRUC_M1M2` are mandatory acquisition-nuisance strata for future montage-stratified reliability sensitivity analyses.
* TARGET-FREE STATUS: discovered before modeling; no model accuracy, calibration, uncertainty, stage-distribution optimization, or target-domain fitting was used.
* IMPACT: data contract version changes from `1.1.0` to `1.2.0`; canonical labels, scorer-1 policy, 30-second epochs, target rates, units, resampling implementation, normalization prohibition, C0–C5 semantics, and target-free safeguards are unchanged.

## A-08.1-01 — Independent Source-Test Partition for Known-Domain Evaluation

* DISCOVERED: before modeling, predictions, calibration outputs, or performance results existed. The prior source roles could not provide an untouched in-domain evaluation population for paired C0–C2.
* OLD: source roles were TRAIN 70%, DEV 15%, CALIBRATION 15%, with no independent SOURCE TEST role.
* NEW: source roles are TRAIN 60%, DEV 15%, CALIBRATION 10%, TEST 15%, all subject-level. Sleep-EDF is unstratified; ISRUC is stratified only by frozen montage variant.
* COUNTS: Sleep-EDF is 47/12/8/11; ISRUC is 59/15/10/15, with ISRUC_A1A2 10/3/2/2 and ISRUC_M1M2 49/12/8/13.
* EVIDENCE: `configs/evaluation_protocol_v1_1.yaml`, `reports/subject_partitions_v2.csv`, and `reports/step08_1_subject_split_audit.csv`.
* DECISION: `ADOPT_INDEPENDENT_SOURCE_TEST_FOR_C0_C2`.
* FIREWALL: TEST is final C0–C2 evaluation only and cannot influence fitting, normalization, checkpoint/hyperparameter selection, temperature scaling, conformal quantiles, or thresholds.
* MAPPING: C0–C2 use paired SOURCE TEST; C3–C5 use paired complete TARGET populations.
* UNCHANGED: cohorts, target populations, C0–C5 meanings, metrics, seeds, oracle protocol, and montage contract.
* STATUS: protocol remains `EXPERIMENT_PROTOCOL_FROZEN` under version `1.1.0`; Step 9 is not executed.
