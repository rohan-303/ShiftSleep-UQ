"""Rebuild the Step 6.1 ISRUC annotation/accounting smoke artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

from shiftsleep_uq.data.preprocess import process_one, read_isruc_events
from shiftsleep_uq.data.preprocessing import LABELS

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "data/processed/core_v1"
OLD_OUT = Path("C:/tmp/shiftsleep_uq_step61_old_outputs")
REPORTS = ROOT / "reports"
SUBJECTS = ["I003", "I004", "I005"]


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def array_sha256(x: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def raw_audit() -> list[dict]:
    rows = []
    for subject in SUBJECTS:
        path = RAW / f"isruc-nemar/v1.0.1/sub-{subject}_task-sleep_events.tsv"
        events = read_isruc_events(path)
        by_label = {}
        durations = {}
        for _, duration, label in events:
            by_label[label] = by_label.get(label, 0) + 1
            durations.setdefault(label, set()).add(f"{duration:g}")
        for label in sorted(by_label):
            rows.append({
                "dataset": "isruc_s1",
                "subject_id": subject,
                "recording_id": subject,
                "event_column_used": "trial_type",
                "raw_value": label,
                "count": by_label[label],
                "duration_unique_values": ";".join(sorted(durations[label], key=float)),
                "source_file_sha256": file_sha256(path),
            })
    return rows


def old_outputs() -> dict[str, dict[str, np.ndarray | str]]:
    saved = {}
    for subject in SUBJECTS:
        path = OLD_OUT / f"isruc_s1__{subject}__core_v1.npz"
        with np.load(path, allow_pickle=False) as z:
            saved[subject] = {
                "output_sha256": file_sha256(path),
                "eeg": z["eeg"].copy(),
                "eog": z["eog"].copy(),
                "labels": z["labels"].copy(),
                "source_epoch_indices": z["source_epoch_indices"].copy(),
            }
    return saved


def process_isruc(saved: dict) -> tuple[list[dict], list[dict]]:
    results = []
    comparisons = []
    for subject in SUBJECTS:
        output = OUT / f"isruc_s1__{subject}__core_v1.npz"
        if output.exists():
            output.unlink()
        result = process_one("isruc_s1", subject, RAW, OUT, RAW / "metadata")
        if result["status"] != "SUCCESS":
            raise RuntimeError(f"{subject} failed: {result}")
        with np.load(output, allow_pickle=False) as z:
            new_eeg, new_eog, new_labels = z["eeg"].copy(), z["eog"].copy(), z["labels"].copy()
            new_source_indices = z["source_epoch_indices"].copy()
        prior = saved[subject]
        common, old_pos, new_pos = np.intersect1d(
            prior["source_epoch_indices"], new_source_indices, return_indices=True
        )
        old_eeg = prior["eeg"][old_pos]
        new_eeg = new_eeg[new_pos]
        old_eog = prior["eog"][old_pos]
        new_eog = new_eog[new_pos]
        comparisons.append({
            "dataset": "isruc_s1", "subject": subject,
            "old_output_sha256": prior["output_sha256"],
            "new_output_sha256": result["output_sha256"],
            "common_source_epochs": len(common),
            "old_eeg_sha256": array_sha256(old_eeg),
            "new_eeg_sha256": array_sha256(new_eeg),
            "eeg_equal": str(np.array_equal(old_eeg, new_eeg)),
            "old_eog_sha256": array_sha256(old_eog),
            "new_eog_sha256": array_sha256(new_eog),
            "eog_equal": str(np.array_equal(old_eog, new_eog)),
            "old_labels_sha256": array_sha256(prior["labels"]),
            "new_labels_sha256": array_sha256(new_labels),
            "labels_equal": str(np.array_equal(prior["labels"], new_labels)),
        })
        results.append(result)
    return results, comparisons


def load_existing_manifest() -> list[dict]:
    with (REPORTS / "preprocessing_smoke_manifest.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rebuild_manifests(isruc_results: list[dict], extra_results: list[dict] | None = None) -> None:
    by_subject = {r["subject_id"]: r for r in isruc_results}
    manifest = [r for r in load_existing_manifest() if r.get("dataset") != "isruc_s1"]
    if extra_results:
        manifest = [r for r in manifest if r.get("recording_id") not in
                    {x["recording_id"] for x in extra_results}]
        manifest.extend(extra_results)
    manifest.extend(by_subject.values())
    fields = [
        "annotation_file", "annotation_sha256", "canonical_unit", "cohort", "contract_version",
        "dataset", "eeg_shape", "eog_shape", "excluded_epochs", "failure_code", "nan_inf",
        "output_path", "output_sha256", "preprocessing_version", "recording_id",
        "source_eeg_channel", "source_eeg_rate", "source_eog_channel", "source_eog_rate",
        "source_file", "source_sha256", "status", "subject_id", "target_eeg_rate",
        "target_eog_rate", "total_source_stage_epochs", "valid_canonical_epochs", "wake", "n1",
        "n2", "n3", "rem", "excluded_movement", "excluded_unknown", "excluded_unscored",
        "excluded_artifact", "excluded_incomplete", "excluded_alignment_error",
        "excluded_missing_signal_samples", "excluded_other",
    ]
    write_csv(REPORTS / "preprocessing_smoke_manifest.csv", fields, manifest)

    audit_rows = []
    for row in manifest:
        if row.get("status") != "SUCCESS":
            continue
        if row["dataset"] == "isruc_s1":
            counts = {label.lower(): int(row.get(label.lower(), 0) or 0) for label in LABELS}
        else:
            output = ROOT / row["output_path"].replace("\\", "/")
            with np.load(output, allow_pickle=False) as z:
                labels = z["labels"]
            counts = {label.lower(): int(np.count_nonzero(labels == i))
                      for i, label in enumerate(LABELS)}
            row.update({label.lower(): value for label, value in zip(LABELS, counts.values())})
        if row["dataset"] == "isruc_s1":
            exclusions = {k.removeprefix("excluded_"): int(row.get(k, 0) or 0)
                          for k in ["excluded_movement", "excluded_unknown", "excluded_unscored",
                                    "excluded_artifact", "excluded_incomplete", "excluded_alignment_error",
                                    "excluded_missing_signal_samples", "excluded_other"]}
        else:
            exclusions = {"movement": 0, "unknown": 0, "unscored": 0, "artifact": 0,
                          "incomplete": 0, "alignment_error": 0, "missing_signal_samples": 0,
                          "other": int(row.get("excluded_epochs", 0) or 0)}
        valid = sum(counts.values())
        excluded = sum(exclusions.values())
        source = int(row.get("total_source_stage_epochs", 0) or 0)
        audit_rows.append({
            "dataset": row["dataset"], "subject": row["subject_id"], "recording": row["recording_id"],
            "source_stage_epochs": source, **counts, "valid_canonical_epochs": valid,
            "excluded_unknown": exclusions["unknown"], "excluded_movement": exclusions["movement"],
            "excluded_unscored": exclusions["unscored"], "excluded_artifact": exclusions["artifact"],
            "excluded_incomplete": exclusions["incomplete"], "excluded_alignment": exclusions["alignment_error"],
            "excluded_missing_samples": exclusions["missing_signal_samples"], "excluded_other": exclusions["other"],
            "total_excluded": excluded, "accounted_epochs": valid + excluded,
            "accounting_delta": source - (valid + excluded),
            "status": "PASS" if source == valid + excluded else "FAIL",
        })
    fields = ["dataset", "subject", "recording", "source_stage_epochs", "wake", "n1", "n2", "n3", "rem",
              "valid_canonical_epochs", "excluded_unknown", "excluded_movement", "excluded_unscored",
              "excluded_artifact", "excluded_incomplete", "excluded_alignment", "excluded_missing_samples",
              "excluded_other", "total_excluded", "accounted_epochs", "accounting_delta", "status"]
    write_csv(REPORTS / "preprocessing_accounting_audit.csv", fields, audit_rows)

    epoch_fields = ["dataset", "subject_id", "Wake", "N1", "N2", "N3", "REM", "Movement", "unknown",
                    "unscored", "artifact", "incomplete", "alignment_error", "other"]
    epoch_rows = []
    for row in audit_rows:
        epoch_rows.append({"dataset": row["dataset"], "subject_id": row["subject"], "Wake": row["wake"],
                           "N1": row["n1"], "N2": row["n2"], "N3": row["n3"], "REM": row["rem"],
                           "Movement": row["excluded_movement"], "unknown": row["excluded_unknown"],
                           "unscored": row["excluded_unscored"], "artifact": row["excluded_artifact"],
                           "incomplete": row["excluded_incomplete"], "alignment_error": row["excluded_alignment"],
                           "other": row["excluded_other"]})
    write_csv(REPORTS / "preprocessing_epoch_audit.csv", epoch_fields, epoch_rows)


def determinism() -> list[dict]:
    records = [("sleep_edf_sc", "SC4001E0"), ("isruc_s1", "I003")]
    rows = []
    for dataset, subject in records:
        hashes = []
        for _ in range(2):
            output = OUT / f"{dataset}__{subject}__core_v1.npz"
            result = process_one(dataset, subject, RAW, OUT, RAW / "metadata")
            if result["status"] != "SUCCESS":
                raise RuntimeError(result)
            hashes.append(file_sha256(output))
        rows.append({"dataset": dataset, "recording": subject, "run_1_sha256": hashes[0],
                     "run_2_sha256": hashes[1], "identical": str(hashes[0] == hashes[1])})
    return rows


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    write_csv(REPORTS / "isruc_raw_annotation_audit.csv",
              ["dataset", "subject_id", "recording_id", "event_column_used", "raw_value", "count",
               "duration_unique_values", "source_file_sha256"], raw_audit())
    saved = old_outputs()
    isruc_results, comparisons = process_isruc(saved)
    sc4021 = process_one("sleep_edf_sc", "SC4021E0", RAW, OUT, RAW / "metadata")
    if sc4021["status"] != "SUCCESS":
        raise RuntimeError(f"SC4021E0 failed: {sc4021}")
    write_csv(REPORTS / "signal_annotation_repair_comparison.csv", list(comparisons[0]), comparisons)
    rebuild_manifests(isruc_results, [sc4021])
    det = determinism()
    write_csv(REPORTS / "determinism_hashes.csv", list(det[0]), det)
    print(json.dumps({"isruc_results": isruc_results, "signal_comparisons": comparisons,
                      "determinism": det}, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
