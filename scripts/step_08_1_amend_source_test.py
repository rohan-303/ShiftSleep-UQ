"""Generate the Step 8.1 independent SOURCE TEST amendment artifacts.

Metadata-only: consumes frozen included-subject manifests and never reads signal
arrays, labels, predictions, or fitted parameters.
"""
from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SPLIT_SEED = 2026
ROLES = ("TRAIN", "DEV", "CALIBRATION", "TEST")

# Amendment A-08.1-01 explicitly freezes these constrained quotas. The stable
# hash order assigns subjects within each predeclared stratum; it never uses
# labels, epoch totals, model information, or target outcomes.
QUOTAS = {
    "sleep_edf_sc": {"ALL": {"TRAIN": 47, "DEV": 12, "CALIBRATION": 8, "TEST": 11}},
    "isruc_s1": {
        "ISRUC_A1A2": {"TRAIN": 10, "DEV": 3, "CALIBRATION": 2, "TEST": 2},
        "ISRUC_M1M2": {"TRAIN": 49, "DEV": 12, "CALIBRATION": 8, "TEST": 13},
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def stable_order(dataset: str, stratum: str, subject_ids: list[str]) -> list[str]:
    return sorted(
        subject_ids,
        key=lambda subject: hashlib.sha256(
            f"{SPLIT_SEED}|{dataset}|{stratum}|{subject}".encode("utf-8")
        ).hexdigest(),
    )


def assign_roles(dataset: str, subject_to_stratum: dict[str, str]) -> dict[str, str]:
    assignments: dict[str, str] = {}
    for stratum in sorted(set(subject_to_stratum.values())):
        subjects = [subject for subject, value in subject_to_stratum.items() if value == stratum]
        ordered = stable_order(dataset, stratum, subjects)
        quotas = QUOTAS[dataset][stratum]
        assert sum(quotas.values()) == len(ordered)
        cursor = 0
        for role in ROLES:
            count = quotas[role]
            for subject in ordered[cursor : cursor + count]:
                assignments[subject] = role
            cursor += count
    assert set(assignments) == set(subject_to_stratum)
    assert len(assignments) == len(set(assignments))
    return assignments


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sleep = [
        row for row in read_csv(REPORTS / "core_recording_manifest_v1_1.csv")
        if row["dataset"] == "sleep_edf_sc" and row["terminal_status"] == "INCLUDED"
    ]
    isruc = [
        row for row in read_csv(REPORTS / "isruc_original_recording_manifest_v2.csv")
        if row["terminal_status"] == "INCLUDED"
    ]
    assert len({row["subject_id"] for row in sleep}) == 78
    assert len({row["subject_id"] for row in isruc}) == 99

    datasets = {
        "sleep_edf_sc": (sleep, {row["subject_id"]: "ALL" for row in sleep}, "core_cohort_v2"),
        "isruc_s1": (isruc, {row["subject_id"]: row["montage_variant"] for row in isruc}, "isruc_original_v3"),
    }
    source_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []
    for dataset, (records, strata, cohort_version) in datasets.items():
        roles = assign_roles(dataset, strata)
        by_subject: dict[str, list[dict[str, str]]] = defaultdict(list)
        for record in records:
            by_subject[record["subject_id"]].append(record)
        for subject in sorted(strata):
            source_rows.append(
                {
                    "dataset": dataset,
                    "subject_id": subject,
                    "source_role": roles[subject],
                    "montage_variant": strata[subject] if dataset == "isruc_s1" else "",
                    "split_seed": SPLIT_SEED,
                    "cohort_version": cohort_version,
                    "data_contract_version": "1.2.0",
                    "preprocessing_version": "0.1.0",
                    "amendment_id": "A-08.1-01",
                }
            )
        for role in ROLES:
            selected = [subject for subject in strata if roles[subject] == role]
            selected_records = [record for subject in selected for record in by_subject[subject]]
            montage_counts = defaultdict(int)
            for subject in selected:
                if dataset == "isruc_s1":
                    montage_counts[strata[subject]] += 1
            audit_rows.append(
                {
                    "dataset": dataset,
                    "source_role": role,
                    "subject_count": len(selected),
                    "recording_count": len(selected_records),
                    "valid_epoch_count": sum(int(record.get("valid_canonical_epochs", record.get("valid_epochs", "0")) or 0) for record in selected_records),
                    "ISRUC_A1A2_subject_count": montage_counts["ISRUC_A1A2"],
                    "ISRUC_M1M2_subject_count": montage_counts["ISRUC_M1M2"],
                    "partition_rule": "subject-level; ISRUC stratified by frozen montage_variant only" if dataset == "isruc_s1" else "subject-level; no label/stage/epoch-count stratification",
                }
            )

    source_rows.sort(key=lambda row: (str(row["dataset"]), str(row["subject_id"])))
    audit_rows.sort(key=lambda row: (str(row["dataset"]), ROLES.index(str(row["source_role"]))))
    write_csv(
        REPORTS / "subject_partitions_v2.csv",
        ["dataset", "subject_id", "source_role", "montage_variant", "split_seed", "cohort_version", "data_contract_version", "preprocessing_version", "amendment_id"],
        source_rows,
    )
    write_csv(
        REPORTS / "step08_1_subject_split_audit.csv",
        ["dataset", "source_role", "subject_count", "recording_count", "valid_epoch_count", "ISRUC_A1A2_subject_count", "ISRUC_M1M2_subject_count", "partition_rule"],
        audit_rows,
    )
    print(f"wrote {len(source_rows)} source rows and {len(audit_rows)} audit rows")


if __name__ == "__main__":
    main()
