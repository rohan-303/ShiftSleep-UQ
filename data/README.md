# Data storage contract

Raw and derived PSG material is local-only under `data/raw/`, `data/interim/`, and `data/processed/`; these paths are ignored by Git. `data/external/` is reserved for legally redistributable metadata only. `reports/` contains safe machine-readable inventories and provenance, not signal samples or restricted participant data.

Source files are immutable: never edit, rename, re-encode, filter, resample, normalize, or overwrite downloaded provider files. Record official URL, dataset/version, filename, byte size, SHA-256, acquisition date, and access/license category in `reports/acquisition_manifest.csv`. Compare provider checksums whenever available and preserve MISMATCH/NO_OFFICIAL_CHECKSUM outcomes.

Do not commit or redistribute raw PSG, restricted annotations, credentials, cookies, tokens, or access keys. Raw data remain subject to each provider's license and access terms. `raw` means provider material, `interim` means non-final inspection derivatives, `processed` means future model-ready data, and `manifests`/`reports` mean provenance-preserving metadata without signal samples. No preprocessing is authorized by Step 4.
