# Step 11.1 B0 Ranking Bootstrap Code-Path Map

## Bootstrap entry and draw construction

- Draw generator: `src/shiftsleep_uq/step11_1_statistics.py:bootstrap_subject_draws`.
- RNG: `np.random.default_rng(seed).integers(0, subject_count, size=(reps, subject_count))`.
- Historical reconstruction helper: `reconstruct_cluster_indices` in the same module.
- Historical v1.1 production worker: `scripts/step11_1_statistical_qa.py`, lines 70–87.
- Historical v1.1 production call: `weighted_metric_replicates(d, metric, draws, ...)`.
- Historical artifact writer: `np.savez_compressed(ROOT/'artifacts/statistics/b0/bootstrap_replicates_v1_1.npz', **arrays)` in `scripts/step11_1_statistical_qa.py`.
- Multi-seed aggregation: `np.nanmean(np.stack(reps_by_seed), axis=0)` in `scripts/step11_1_statistical_qa.py`, line 83.

## Metric map

| Metric | Authoritative point function | Step 11.1 bootstrap function | Weighting/reconstruction path | Artifact serialization |
|---|---|---|---|---|
| macro-F1 | `evaluation_step11.py:macro_f1` | `step11_1_statistics.py:_metric` → `weighted_metric_replicates` | Per-subject confusion sufficient statistics are multiplied by subject multiplicity; equivalent to duplicated clusters. | `arrays[f'{ex}_{c}_macro-F1']` → `bootstrap_replicates_v1_1.npz` |
| NLL | `evaluation_step11.py:nll` | `_metric` → `weighted_metric_replicates` | Per-epoch NLL sums are aggregated by subject and multiplied by multiplicity; equivalent for additive means. | `arrays[f'{ex}_{c}_NLL']` |
| Brier | `evaluation_step11.py:brier` | `_metric` → `weighted_metric_replicates` | Per-epoch Brier sums are aggregated by subject and multiplied by multiplicity; equivalent for additive means. | `arrays[f'{ex}_{c}_Brier']` |
| ERROR_AUROC | `evaluation_step11.py:_rank_auc` | `_metric` → `weighted_metric_replicates` | Historical path sorts epoch uncertainty stably and uses weighted midpoint ranks; the new engine uses exact weighted pair/rank accounting. It agrees with literal duplication for integer multiplicities. | `arrays[f'{ex}_{c}_ERROR_AUROC']` |
| ERROR_AUPRC | `evaluation_step11.py:auprc` | `_metric` → `weighted_metric_replicates` | Historical path uses one weighted threshold contribution per original epoch (`tp/weighted cumulative count`); it does not emit the sequential precision/recall points created by repeated observations. | `arrays[f'{ex}_{c}_ERROR_AUPRC']` |
| AURC | `evaluation_step11.py:aurc` | `_metric` → `weighted_metric_replicates` | Historical path computes one weighted prefix-risk contribution per original epoch; it does not emit the distinct intermediate retained-set risks created by repeated observations. | `arrays[f'{ex}_{c}_AURC']` |

## Exact comparison path used in Step 15.2.2

- PATH H: `weighted_metric_replicates` from the historical Step 11.1 module.
- PATH L: `reconstruct_cluster_indices` semantics, followed by `evaluation_step11._metric` on physically expanded epoch arrays.
- PATH E: `statistics.weighted_bootstrap.prepare` + `ranking`, with integer subject multiplicities.
- PATH A: stored arrays loaded from `artifacts/statistics/b0/bootstrap_replicates_v1_1.npz`.

The matrix and counterexample artifacts record all four paths without modifying the historical artifact.
