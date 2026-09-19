# Bootstrap estimand

For each condition and metric, the frozen paired procedure resamples subjects with replacement using the exact duplicate-preserving multiplicity draws. Each replicate computes the metric separately for seed 17, seed 42, and seed 2026, then averages the three seed-specific values. B1 minus B0 is formed within the same replicate before percentile limits are reported.

The resulting interval primarily represents subject-sampling uncertainty for the mean of three fixed trained-model seeds. It does not fully represent arbitrary future training randomness; seed variability is reported separately.
