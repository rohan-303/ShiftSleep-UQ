from __future__ import annotations

import csv
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_alias_provenance_covers_every_shared_canonical_mapping_string():
    contract = yaml.safe_load((ROOT / "configs/data_contract_v1.yaml").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((ROOT / "reports/canonical_label_alias_provenance.csv").open(encoding="utf-8", newline="")))
    observed = {(r["canonical_label"], r["accepted_source_string"]) for r in rows}
    expected = {(label, source) for label, sources in contract["label_mappings"].items() for source in sources}
    assert observed == expected
    assert all(r["exact_match_required"] == "TRUE" for r in rows)
    assert {r["status"] for r in rows} <= {"VERIFIED_SOURCE_ALIAS", "INTERNAL_CANONICAL_ALIAS"}


def test_frozen_expected_population_is_complete_unique_and_subject_grouped():
    rows = list(csv.DictReader((ROOT / "reports/core_expected_population.csv").open(encoding="utf-8", newline="")))
    assert len(rows) == 253
    assert len({(r["dataset"], r["recording_id"]) for r in rows}) == 253
    sc = [r for r in rows if r["dataset"] == "sleep_edf_sc"]
    isruc = [r for r in rows if r["dataset"] == "isruc_s1"]
    assert len(sc) == 153 and len({r["subject_id"] for r in sc}) == 78
    assert len(isruc) == 100 and len({r["subject_id"] for r in isruc}) == 100
    assert all(r["expected"] == "YES" and r["subject_group"] == r["subject_id"] for r in rows)
    assert all("split" not in field.lower() for field in rows[0])


def test_frozen_subject_manifest_preserves_expected_subject_grouping():
    expected = list(csv.DictReader((ROOT / "reports/core_expected_population.csv").open(encoding="utf-8", newline="")))
    subjects = list(csv.DictReader((ROOT / "reports/core_subject_manifest_v1.csv").open(encoding="utf-8", newline="")))
    expected_subjects = {(r["dataset"], r["subject_id"]) for r in expected}
    observed_subjects = {(r["dataset"], r["subject_id"]) for r in subjects}
    assert observed_subjects == expected_subjects
    assert len(subjects) == 178
    assert len([r for r in subjects if r["dataset"] == "sleep_edf_sc"]) == 78
    assert len([r for r in subjects if r["dataset"] == "isruc_s1"]) == 100
