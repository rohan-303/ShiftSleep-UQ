"""Generate Step 8 metadata-only source/oracle partitions and audit.

This script never reads signal arrays or labels. It consumes only frozen manifests.
"""
from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SPLIT_SEED = 2026
ORACLE_SEED = 2027
ROLES = ("TRAIN", "DEV", "CALIBRATION")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def stable_order(dataset: str, stratum: str, subject_ids: list[str], seed: int) -> list[str]:
    return sorted(
        subject_ids,
        key=lambda subject: hashlib.sha256(
            f"{seed}|{dataset}|{stratum}|{subject}".encode("utf-8")
        ).hexdigest(),
    )


def largest_remainder_counts(total: int, proportions: tuple[float, ...]) -> list[int]:
    raw = [total * proportion for proportion in proportions]
    counts = [int(value) for value in raw]
    remaining = total - sum(counts)
    order = sorted(
        range(len(raw)),
        key=lambda index: (-(raw[index] - counts[index]), index),
    )
    for index in order[:remaining]:
        counts[index] += 1
    return counts


def assign_roles(dataset: str, subject_to_stratum: dict[str, str], seed: int) -> dict[str, str]:
    assignments: dict[str, str] = {}
    strata = sorted(set(subject_to_stratum.values()))
    for stratum in strata:
        subjects = [s for s, value in subject_to_stratum.items() if value == stratum]
        ordered = stable_order(dataset, stratum, subjects, seed)
        counts = largest_remainder_counts(len(ordered), (0.70, 0.15, 0.15))
        cursor = 0
        for role, count in zip(ROLES, counts):
            for subject in ordered[cursor : cursor + count]:
                assignments[subject] = role
            cursor += count
    assert set(assignments) == set(subject_to_stratum)
    assert len(assignments) == len(set(assignments))
    return assignments


def assign_oracle(dataset: str, subject_to_stratum: dict[str, str]) -> dict[str, str]:
    assignments: dict[str, str] = {}
    for stratum in sorted(set(subject_to_stratum.values())):
        subjects = [s for s, value in subject_to_stratum.items() if value == stratum]
        ordered = stable_order(dataset, stratum, subjects, ORACLE_SEED)
        calibration_count = largest_remainder_counts(len(ordered), (0.20, 0.80))[0]
        for subject in ordered[:calibration_count]:
            assignments[subject] = "ORACLE_CALIBRATION"
        for subject in ordered[calibration_count:]:
            assignments[subject] = "ORACLE_EVALUATION"
    assert set(assignments) == set(subject_to_stratum)
    return assignments


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sleep_rows = [
        row
        for row in read_csv(REPORTS / "core_recording_manifest_v1_1.csv")
        if row["dataset"] == "sleep_edf_sc" and row["terminal_status"] == "INCLUDED"
    ]
    isruc_rows = [
        row
        for row in read_csv(REPORTS / "isruc_original_recording_manifest_v2.csv")
        if row["terminal_status"] == "INCLUDED"
    ]
    assert len({row["subject_id"] for row in sleep_rows}) == 78
    assert len({row["subject_id"] for row in isruc_rows}) == 99

    datasets = {
        "sleep_edf_sc": {
            "rows": sleep_rows,
            "strata": {row["subject_id"]: "ALL" for row in sleep_rows},
            "cohort_version": "core_cohort_v2",
        },
        "isruc_s1": {
            "rows": isruc_rows,
            "strata": {row["subject_id"]: row["montage_variant"] for row in isruc_rows},
            "cohort_version": "isruc_original_v3",
        },
    }

    partition_rows: list[dict[str, object]] = []
    oracle_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []
    for dataset, info in datasets.items():
        subject_to_stratum = info["strata"]
        roles = assign_roles(dataset, subject_to_stratum, SPLIT_SEED)
        oracle = assign_oracle(dataset, subject_to_stratum)
        by_subject: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in info["rows"]:
            by_subject[row["subject_id"]].append(row)

        for subject in sorted(subject_to_stratum):
            stratum = subject_to_stratum[subject]
            partition_rows.append(
                {
                    "dataset": dataset,
                    "subject_id": subject,
                    "source_role": roles[subject],
                    "montage_variant": stratum if dataset == "isruc_s1" else "",
                    "split_seed": SPLIT_SEED,
                    "cohort_version": info["cohort_version"],
                    "data_contract_version": "1.2.0",
                    "preprocessing_version": "0.1.0",
                }
            )
            oracle_rows.append(
                {
                    "dataset": dataset,
                    "subject_id": subject,
                    "oracle_role": oracle[subject],
                    "montage_variant": stratum if dataset == "isruc_s1" else "",
                    "oracle_split_seed": ORACLE_SEED,
                    "cohort_version": info["cohort_version"],
                    "data_contract_version": "1.2.0",
                    "preprocessing_version": "0.1.0",
                }
            )

        for role in ROLES:
            selected = [s for s in subject_to_stratum if roles[s] == role]
            selected_rows = [row for s in selected for row in by_subject[s]]
            montage_counts = defaultdict(int)
            for s in selected:
                if dataset == "isruc_s1":
                    montage_counts[subject_to_stratum[s]] += 1
            audit_rows.append(
                {
                    "dataset": dataset,
                    "source_role": role,
                    "subject_count": len(selected),
                    "recording_count": len(selected_rows),
                    "valid_epoch_count": sum(int(row.get("valid_canonical_epochs", row.get("valid_epochs", "0")) or 0) for row in selected_rows),
                    "ISRUC_A1A2_subject_count": montage_counts["ISRUC_A1A2"],
                    "ISRUC_M1M2_subject_count": montage_counts["ISRUC_M1M2"],
                    "partition_rule": "subject-level; ISRUC stratified by frozen montage_variant only" if dataset == "isruc_s1" else "subject-level; no label/stage stratification",
                }
            )

    partition_rows.sort(key=lambda row: (str(row["dataset"]), str(row["subject_id"])))
    oracle_rows.sort(key=lambda row: (str(row["dataset"]), str(row["subject_id"])))
    audit_rows.sort(key=lambda row: (str(row["dataset"]), ROLES.index(str(row["source_role"]))))
    write_csv(
        REPORTS / "subject_partitions_v1.csv",
        ["dataset", "subject_id", "source_role", "montage_variant", "split_seed", "cohort_version", "data_contract_version", "preprocessing_version"],
        partition_rows,
    )
    write_csv(
        REPORTS / "oracle_target_partitions_v1.csv",
        ["dataset", "subject_id", "oracle_role", "montage_variant", "oracle_split_seed", "cohort_version", "data_contract_version", "preprocessing_version"],
        oracle_rows,
    )
    write_csv(
        REPORTS / "step08_subject_split_audit.csv",
        ["dataset", "source_role", "subject_count", "recording_count", "valid_epoch_count", "ISRUC_A1A2_subject_count", "ISRUC_M1M2_subject_count", "partition_rule"],
        audit_rows,
    )
    print(f"wrote {len(partition_rows)} source rows, {len(oracle_rows)} oracle rows, {len(audit_rows)} audit rows")


if __name__ == "__main__":
    main()
