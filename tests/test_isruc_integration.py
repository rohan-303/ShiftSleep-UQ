import csv
from collections import Counter
from pathlib import Path

import pytest

from shiftsleep_uq.data.preprocess import read_isruc_events, summarize_epoch_accounting
from shiftsleep_uq.data.preprocessing import expand_annotations


@pytest.mark.parametrize("subject", ["I003", "I004", "I005"])
def test_real_nemar_event_table_accounting(subject):
    path = Path(f"data/raw/isruc-nemar/v1.0.1/sub-{subject}_task-sleep_events.tsv")
    if not path.exists():
        pytest.skip("local NEMAR smoke metadata is unavailable")
    events = read_isruc_events(path)
    raw = Counter(label for _, _, label in events)
    assert set(raw) <= {"Sleep stage W", "Sleep stage N1", "Sleep stage N2",
                         "Sleep stage N3", "Sleep stage R", "Sleep stage U"}
    expanded = expand_annotations(events)
    counts, exclusions, valid, excluded = summarize_epoch_accounting(expanded)
    assert valid + excluded == len(expanded)
    assert valid == sum(counts.values())
    assert counts["n1"] == raw["Sleep stage N1"]
    assert counts["n2"] == raw["Sleep stage N2"]
    assert counts["n3"] == raw["Sleep stage N3"]
    assert counts["wake"] == raw["Sleep stage W"]
    assert counts["rem"] == raw["Sleep stage R"]