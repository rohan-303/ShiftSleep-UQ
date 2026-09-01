# Label contract proposal

Not implemented and not frozen. Sleep-EDF and CAP official documentation report R&K macrostructure. Candidate canonical labels are Wake, N1, N2, N3, REM.

| Original label | Proposed canonical | Decision | Rationale |
|---|---|---|---|
| W / Wake | Wake | INCLUDE | Explicit provider scoring label |
| R / REM | REM | INCLUDE | Explicit provider scoring label |
| 1 / S1 / Stage 1 | N1 | INCLUDE | R&K stage terminology |
| 2 / S2 / Stage 2 | N2 | INCLUDE | R&K stage terminology |
| 3 / S3 / Stage 3 | N3 | REVIEW/PROPOSE | Standard R&K-to-AASM aggregation needs authoritative citation in Step 5 |
| 4 / S4 / Stage 4 | N3 | REVIEW/PROPOSE | Stage 3+4 aggregation is conventional but must be source-supported before freeze |
| M / MT / Movement Time | none | EXCLUDE pending policy | Not a sleep stage; preserve counts and exclusions in audit |
| ? / UNKNOWN | none | EXCLUDE | Provider marks not scored; never silently map |
| artifact | none | REVIEW | Dataset-specific annotation semantics not verified |
| unscored | none | EXCLUDE | No target label |
| scorer disagreement | none | REVIEW | Requires source annotation/disagreement evidence; do not resolve silently |

CAP additionally includes CAP phase-A annotations and body-position/event fields; these are not sleep-stage classes. R&K stage labels must be kept distinct from CAP-specific labels. The final mapping, exclusion policy, and treatment of missing epochs must be frozen only after direct annotation-file inspection and an authoritative Stage 3+4 precedent.
