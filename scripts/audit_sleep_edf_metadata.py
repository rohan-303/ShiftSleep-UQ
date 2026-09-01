"""Build metadata-only Sleep-EDF manifests from official RECORDS.

No signal file is opened. Subject IDs are derived only from the official filename
convention documented by PhysioNet and are marked with their identity source.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "data/raw/metadata/sleep-edfx/1.0.0/RECORDS"
OUT = ROOT / "reports"
SC_RE = re.compile(r"SC4(?P<subject>\d{2})(?P<night>[12])[A-Z]\d")
ST_RE = re.compile(r"ST7(?P<subject>\d{2})(?P<night>[12])[A-Z]\d")

def rows():
    for raw in RECORDS.read_text().splitlines():
        path = Path(raw.strip())
        if not path.name.endswith("-PSG.edf"):
            continue
        stem = path.name.removesuffix("-PSG.edf")
        match = SC_RE.fullmatch(stem) or ST_RE.fullmatch(stem)
        if not match:
            raise ValueError(f"unrecognized official Sleep-EDF filename: {path.name}")
        substudy = "SC" if stem.startswith("SC") else "ST"
        subject = match.group("subject")
        night = match.group("night")
        yield {
            "dataset":"Sleep-EDF Expanded v1.0.0", "substudy":substudy,
            "subject_id":f"{substudy}_{subject}", "recording_id":stem,
            "night":night, "treatment_condition_if_verified":("temazepam/placebo; night assignment requires spreadsheet verification" if substudy == "ST" else "NOT_APPLICABLE"),
            "psg_filename":path.as_posix(), "annotation_filename":path.as_posix().replace("-PSG.edf", "-Hypnogram.edf"),
            "identity_confidence":"HIGH_FILENAME_RULE", "notes":"Subject/night derived from official PhysioNet filename convention; no signal opened."
        }

if __name__ == "__main__":
    data=list(rows())
    OUT.mkdir(exist_ok=True)
    with (OUT/"sleep_edf_subject_manifest.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0])); w.writeheader(); w.writerows(data)
    print(f"sleep_edf_subject_manifest: {len(data)} recordings; SC={sum(r['substudy']=='SC' for r in data)} ST={sum(r['substudy']=='ST' for r in data)}; subjects_SC={len({r['subject_id'] for r in data if r['substudy']=='SC'})}; subjects_ST={len({r['subject_id'] for r in data if r['substudy']=='ST'})}")
