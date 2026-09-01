# Dataset overlap and duplication policy

1. Dataset, release/version, substudy, subject, night/visit, recording, and derived-copy identities are separate fields.
2. Partitioning is always by canonical subject identity. All nights, treatment/placebo visits, and repeated visits for one participant remain in one partition.
3. Filename differences do not establish independence. Before a benchmark release, compare official manifests, subject tables, recording durations, annotation metadata, and provider release lineage.
4. Sleep-EDF SC and ST remain separate substudies. The older Sleep-EDF-20/small-subset names must not be treated as an independent domain if their files derive from Sleep-EDF.
5. A recording appearing in multiple local folders, converted formats, or benchmark subsets receives one canonical source identity and cannot enter separate partitions.
6. SHHS1 and SHHS2 visits are grouped by participant identifier; visit identity is retained for audit.
7. CAP filename pathology prefixes are not subject IDs. No cross-recording subject grouping is claimed until an official subject mapping is verified.
8. Any unresolved overlap blocks a DATA_READY decision for the affected configuration and is recorded as `UNRESOLVED`, not assumed independent.
