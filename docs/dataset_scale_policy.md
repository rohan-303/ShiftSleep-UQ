# Dataset Scale Policy

SHHS is large and will not be assumed to require training on every participant. Any future use must choose among all-record use, a deterministic subject-level subset, dataset-balanced subject sampling, or a documented combination. The choice must be frozen before split generation, use no sleep-stage outcomes, no test performance, and no target labels, and be reproducible from participant identifiers and a recorded seed/hash rule. No final subject IDs or arbitrary sample count are selected in Step 5. All visits for one participant remain grouped.
