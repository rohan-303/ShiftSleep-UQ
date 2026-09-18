# Step 17 Limitations

- The benchmark uses two core datasets and two reciprocal directions.
- Exact modality and montage contracts constrain generality.
- B0/B1 are epoch-wise models without temporal context.
- B1 is a simple source-only modality-dropout intervention.
- Target-oracle results are diagnostic only.
- There is no SHHS core validation.
- Formal conformal coverage under arbitrary dataset shift is not established.
- The architecture is deliberately simple.
- Stage labels and harmonization remain dataset-dependent.
- Some residual behavior is direction-specific.
- D2 C5 predictive robustness remains unresolved.
