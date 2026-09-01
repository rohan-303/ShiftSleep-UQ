# Reproducibility policy

- **Seeds:** Every stochastic run records all seeds; seed lists are frozen before confirmatory evaluation.
- **Environment:** Use isolated Python environments, lock dependencies before execution, and record interpreter, package versions, OS, CPU, GPU, CUDA, and driver.
- **Data:** Raw files are immutable. Record source, release, access date, terms, filename, checksum where legally permissible, and transformations. Processed data receive separate version/provenance records.
- **Experiments:** Config-driven; no hidden defaults. Store config, config hash, Git revision/worktree state, run ID, hardware manifest, and status.
- **Logging:** Capture commands, warnings, failures, timing, resource usage, and data/split manifests.
- **Checkpoints:** Record checkpoint identity and selection criterion; never select on test performance.
- **Determinism:** Enable deterministic behavior where supported, document unavoidable nondeterminism, and do not imply bitwise reproducibility without checking it.
- **Outputs:** Results tables and figures are generated from machine-readable outputs, never manually typed numbers. Preserve invalid/failed runs and distinguish executed, reproduced, and validated claims.
- **Network/data boundary:** Documentation-only steps do not download datasets or models.
