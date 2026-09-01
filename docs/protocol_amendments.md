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
