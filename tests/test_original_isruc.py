from pathlib import Path

import pytest

from shiftsleep_uq.data.preprocess import original_recording_spec, read_original_scorer1


def test_original_recording_spec_resolves_frozen_bundle(tmp_path):
    subject = tmp_path / "subject-4" / "4" / "4"
    subject.mkdir(parents=True)
    for name in ("4.rec", "4_1.txt", "4_1.xlsx", "4_2.txt", "4_2.xlsx"):
        (subject / name).touch()
    signal, ann, scorer = original_recording_spec("4", tmp_path / "subject-4")
    assert signal == subject / "4.rec"
    assert ann == subject / "4_1.txt"
    assert scorer == "scorer_1_original_txt"


def test_original_scorer1_parser_reads_numeric_epochs(tmp_path):
    p = tmp_path / "4_1.txt"
    p.write_text("0\n1\n2\n3\n5\n", encoding="utf-8")
    events = read_original_scorer1(p)
    assert events == [(0.0, 30.0, "Sleep stage W"), (30.0, 30.0, "Sleep stage N1"),
                      (60.0, 30.0, "Sleep stage N2"), (90.0, 30.0, "Sleep stage N3"),
                      (120.0, 30.0, "Sleep stage R")]
