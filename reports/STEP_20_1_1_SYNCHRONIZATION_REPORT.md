# ShiftSleep-UQ Step 20.1.1 Synchronization Report

## 1. Status
Step 20.1.1 completed as a documentation-only synchronization closeout. No scientific artifact, protocol, experiment, manuscript, or submission state was changed.

## 2. Synchronization Gate
`STEP20_1_SYNCHRONIZED`.

## 3. Starting HEAD
`e1ae2798c14a6863bfc9e6a0578823d58593bd8d` (`research: freeze post-review scientific remediation protocol`).

## 4. Starting origin/main
`e1ae2798c14a6863bfc9e6a0578823d58593bd8d`.

## 5. Protocol Commit Verification
The required protocol commit exists locally and on `origin/main`. Its message is `research: freeze post-review scientific remediation protocol`. The commit contains `configs/postreview_remediation_protocol_v1.yaml`.

## 6. Protocol SHA-256 Verification
Recomputed SHA-256:

`9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`

The value exactly matches the frozen expected hash. No `STEP20_1_PROTOCOL_HASH_DRIFT` occurred.

## 7. Scientific Gate Verification
The corrected Step 20.1 report retains:

- `SCIENTIFIC_REMEDIATION_PROTOCOL_FROZEN`;
- `SUBMISSION_SUSPENDED_FOR_SCIENTIFIC_REMEDIATION`.

No wording change reopened or altered the scientific protocol.

## 8. Key Decision Verification
The corrected report preserves the required decisions:

- Figure 2 numeric-as-categorical defect: `NOT_CONFIRMED`;
- Figure 2 conformal field-binding defect: `CONFIRMED`;
- APS classification: `APS_PRIMARY_AXIS_REQUIRES_REFRAMING`;
- Table 2/Table 3 estimator decision: `DIFFERENT_VALID_ESTIMANDS`;
- selected backbone: `SeqSleepNet_class`;
- sleep-window rule: first scored non-Wake epoch through last scored non-Wake epoch, plus exactly 30 minutes of context before and after, applied identically to both datasets;
- R2: `NOT_EXECUTED`;
- R3: `NOT_EXECUTED`;
- Step 20.2: `NOT_EXECUTED`;
- Step 21: `NOT_EXECUTED`.

## 9. Tracked Diff Audit
Before the follow-up documentation commit, the only modified tracked file was:

`reports/STEP_20_1_POSTREVIEW_SCIENTIFIC_REMEDIATION_PROTOCOL_REPORT.md`

`git diff e1ae279..HEAD` contained no changes because the report correction was a working-tree modification, not a scientific commit. The working-tree diff showed only the three documentation lines recording the pushed protocol commit, push status, and intentional historical untracked files. No changes touched the remediation YAML, experiment code, B0/B1 results, checkpoints, prediction bundles, partitions, calibration, APS objects, statistical artifacts, canonical manuscript, or JBHI package.

## 10. Historical Untracked Files
The intentionally preserved untracked files are:

- `reports/STEP_18_MANUSCRIPT_DRAFT_REPORT.md`;
- `reports/step18_citation_audit.csv`;
- `reports/step18_manuscript_claim_audit.csv`;
- `reports/step18_section_evidence_map.md`.

They are historical Step 18 documentation, are not required for Step 20.2 execution, were not staged, and were not deleted. A direct content scan found no API-key, password, token, secret, private-key, or bearer-authorization strings. They contain no required new scientific state for Step 20.2.

## 11. Corrected Step 20.1 Report
The report correction accurately records:

- protocol commit `e1ae2798c14a6863bfc9e6a0578823d58593bd8d`;
- protocol hash `9c63e078aadea8f16052b707d2987de921ae577bf2d501272cd881457b2c83fc`;
- successful push to `origin/main`;
- the four intentionally preserved historical Step 18 untracked files.

## 12. Follow-Up Commit
Created without amending or rewriting the pushed protocol commit:

`cf5b827` — `docs: finalize Step 20.1 remediation report`

Only `reports/STEP_20_1_POSTREVIEW_SCIENTIFIC_REMEDIATION_PROTOCOL_REPORT.md` was staged.

## 13. Push Status
The follow-up documentation commit was pushed normally with:

`git push origin main`

No force push, reset, amend, or history rewrite was used.

## 14. Final HEAD
At the final synchronization verification immediately before creation of this report:

`cf5b827`

This commit is the descendant of the unchanged protocol commit `e1ae2798c14a6863bfc9e6a0578823d58593bd8d`.

## 15. Final origin/main
At the same final synchronization verification:

`cf5b827`

## 16. Remote Equality
Local `main` and `origin/main` matched at `cf5b827` after the documentation push. The protocol commit remains in history unchanged, and the follow-up commit is its descendant.

## 17. Final Git Status
Tracked worktree state after the documentation push was clean before this synchronization report was created. The only remaining untracked files are the four explicitly documented historical Step 18 reports. No files were staged from that group.

Final state classification:

`TRACKED_WORKTREE_CLEAN_WITH_DOCUMENTED_HISTORICAL_UNTRACKED_FILES`

The synchronization report itself is a new documentation artifact and is to be committed as a descendant without including the historical untracked files.

## 18. Explicitly Not Done

- no model training;
- no inference;
- no R1 execution;
- no R2 execution;
- no R3 execution;
- no conformal refit;
- no statistical recomputation;
- no manuscript submission;
- no Step 20.2;
- no Step 21;
- no amendment or rewrite of the pushed protocol commit;
- no force push.

## 19. Recommended Next Step
# Step 20.2 — Execute the Frozen Post-Review Remediation Experiments

Do NOT execute Step 20.2 in Step 20.1.1.
