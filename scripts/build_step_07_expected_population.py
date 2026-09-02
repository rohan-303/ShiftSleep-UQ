"""Freeze Step 7.1 expected accessible-core recording population before acquisition."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
METADATA = ROOT / "data/raw/metadata"
FIELDS = [
    "dataset", "cohort", "subject_id", "recording_id", "expected",
    "source_distribution", "expected_eeg", "expected_eog", "subject_group", "notes",
]


def main() -> None:
    sc_source = REPORTS / "sleep_edf_subject_manifest.csv"
    participants = METADATA / "isruc-nemar/v1.0.1/participants.tsv"
    manifest = METADATA / "isruc-nemar/v1.0.1/manifest.json"
    sc = list(csv.DictReader(sc_source.open(encoding="utf-8", newline="")))
    sc = [r for r in sc if r["substudy"] == "SC"]
    isruc = list(csv.DictReader(participants.open(encoding="utf-8-sig", newline=""), delimiter="\t"))
    isruc = [r for r in isruc if re.fullmatch(r"sub-I\d{3}", r["participant_id"])]
    files = json.loads(manifest.read_text(encoding="utf-8"))
    edf_paths = {x["path"] for x in files if x["path"].endswith("_task-sleep_eeg.edf")}

    if len(sc) != 153 or len({r["subject_id"] for r in sc}) != 78:
        raise RuntimeError("Sleep-EDF SC source inventory must be exactly 153 recordings / 78 subjects")
    if len(isruc) != 100 or len({r["participant_id"] for r in isruc}) != 100:
        raise RuntimeError("ISRUC-S1 participants inventory must be exactly 100 subjects")

    rows = []
    for r in sorted(sc, key=lambda x: x["recording_id"]):
        rows.append({
            "dataset": "sleep_edf_sc", "cohort": "Sleep-EDF SC",
            "subject_id": r["subject_id"], "recording_id": r["recording_id"], "expected": "YES",
            "source_distribution": "PhysioNet sleep-edfx/1.0.0 sleep-cassette; official RECORDS + SHA256SUMS",
            "expected_eeg": "EEG Fpz-Cz", "expected_eog": "EOG horizontal",
            "subject_group": r["subject_id"],
            "notes": "Official filename-derived subject/night identity; all provider-listed SC recordings are expected.",
        })
    for r in sorted(isruc, key=lambda x: x["participant_id"]):
        subject = r["participant_id"].removeprefix("sub-")
        path = f"sub-{subject}/eeg/sub-{subject}_task-sleep_eeg.edf"
        if path not in edf_paths:
            raise RuntimeError(f"NEMAR EDF missing from manifest: {path}")
        rows.append({
            "dataset": "isruc_s1", "cohort": "ISRUC-S1",
            "subject_id": subject, "recording_id": subject, "expected": "YES",
            "source_distribution": "NEMAR nm000111 v1.0.1; participants.tsv + manifest.json",
            "expected_eeg": "C3-A2", "expected_eog": "LOC-A2", "subject_group": subject,
            "notes": "One fixed expected S1 recording per NEMAR participant; scorer-1 event stream is primary.",
        })
    if len(rows) != 253 or len({(r["dataset"], r["recording_id"]) for r in rows}) != 253:
        raise RuntimeError("expected-recording identity uniqueness/count invariant failed")
    with (REPORTS / "core_expected_population.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"sleep_edf_sc": len(sc), "sleep_edf_subjects": len({r['subject_id'] for r in sc}), "isruc_s1": len(isruc), "total": len(rows)}, sort_keys=True))

if __name__ == "__main__":
    main()
