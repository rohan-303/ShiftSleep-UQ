"""Step 7.1 raw accessible-core acquisition. Downloads no data to git-tracked paths."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
METADATA = RAW / "metadata"
REPORTS = ROOT / "reports"
PHYSIO = "https://physionet.org/files/sleep-edfx/1.0.0/"
NEMAR = "https://data.nemar.org/nm000111/v1.0.1/"
GITHUB = "https://raw.githubusercontent.com/nemarDatasets/nm000111/main/"

FIELDS = ["dataset","subject_id","recording_id","provider_url","http_status","provider_content_length","local_bytes","edf_declared_bytes","byte_delta","checksum_status","header_valid","body_valid","terminal_status","failure_code"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, destination: Path, expected_sha: str | None, attempts: int = 3) -> tuple[int | str, int | str, str, str]:
    """Atomic, resumable-by-restart download. Existing only accepted if checksum-valid."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and expected_sha and sha256(destination) == expected_sha:
        return "EXISTING_VALID", destination.stat().st_size, "MATCH", ""
    if destination.exists():
        destination.unlink()
    part = destination.with_name(destination.name + ".part")
    error = ""
    for attempt in range(attempts):
        try:
            offset = part.stat().st_size if part.exists() else 0
            headers = {"User-Agent": "ShiftSleep-UQ-Step7.1/1.0"}
            if offset:
                headers["Range"] = f"bytes={offset}-"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as response:
                status = getattr(response, "status", response.getcode())
                content_length = response.headers.get("Content-Length", "")
                # A provider that ignores Range must not be appended as though it were a suffix.
                append = offset > 0 and status == 206
                with part.open("ab" if append else "wb") as out:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        out.write(chunk)
            if expected_sha and sha256(part) != expected_sha:
                error = "CHECKSUM_MISMATCH"
                part.unlink(missing_ok=True)
            else:
                os.replace(part, destination)
                return status, content_length, "MATCH" if expected_sha else "NOT_PROVIDED", ""
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            error = f"DOWNLOAD_ERROR:{type(exc).__name__}"
            # Preserve partial bytes for a later HTTP-Range continuation; they are
            # never accepted as a completed artifact without the expected hash.
        if attempt + 1 < attempts:
            time.sleep(2 ** attempt)
    return "ERROR", "", "MISMATCH" if error == "CHECKSUM_MISMATCH" else "NOT_OBTAINED", error


def edf_declared_bytes(path: Path) -> tuple[int | str, str, str]:
    try:
        from shiftsleep_uq.data.edf import read_edf_header
        with path.open("rb") as f:
            h = read_edf_header(f)
        if h.records < 0:
            return "UNKNOWN_RECORD_COUNT", "PASS", "UNKNOWN"
        declared = h.header_bytes + h.records * sum(h.samples_per_record) * 2
        actual = path.stat().st_size
        return declared, "PASS", "PASS" if declared == actual else "FAIL"
    except Exception:
        return "", "FAIL", "FAIL"


def sc_checksum_map() -> dict[str, str]:
    path = METADATA / "sleep-edfx/1.0.0/SHA256SUMS.txt"
    if not path.exists():
        status, _, chk, err = fetch(PHYSIO + "SHA256SUMS.txt", path, None)
        if err or status == "ERROR":
            raise RuntimeError(f"cannot obtain official SC checksum inventory: {err}")
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        pieces = line.split(maxsplit=1)
        if len(pieces) == 2:
            result[pieces[1]] = pieces[0]
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard-index", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    args = ap.parse_args()
    if args.shards < 1 or not 0 <= args.shard_index < args.shards:
        raise SystemExit("invalid shard parameters")
    expected_all = list(csv.DictReader((REPORTS / "core_expected_population.csv").open(encoding="utf-8", newline="")))
    expected = [row for i, row in enumerate(expected_all) if i % args.shards == args.shard_index]
    expected_sc = [r for r in expected if r["dataset"] == "sleep_edf_sc"]
    expected_isruc = [r for r in expected if r["dataset"] == "isruc_s1"]
    checksums = sc_checksum_map()
    manifest = json.loads((METADATA / "isruc-nemar/v1.0.1/manifest.json").read_text(encoding="utf-8"))
    nemar = {x["path"]: x for x in manifest}
    rows = []

    for r in expected_sc:
        rec, subject = r["recording_id"], r["subject_id"]
        psg_rel = f"sleep-cassette/{rec}-PSG.edf"
        hypnos = [x for x in checksums if x.startswith(f"sleep-cassette/{rec[:-1]}") and x.endswith("-Hypnogram.edf")]
        if len(hypnos) != 1 or psg_rel not in checksums:
            rows.append({"dataset":"sleep_edf_sc","subject_id":subject,"recording_id":rec,"provider_url":PHYSIO+psg_rel,"terminal_status":"EXCLUDED_ACQUISITION","failure_code":"OFFICIAL_PAIRING_INVENTORY_ERROR"})
            continue
        psg = RAW / "sleep-edfx/1.0.0/sleep-cassette" / f"{rec}-PSG.edf"
        ann = METADATA / "sleep-edfx/1.0.0" / Path(hypnos[0]).name
        ps, pcl, pchk, perr = fetch(PHYSIO + psg_rel, psg, checksums[psg_rel])
        hs, hcl, hchk, herr = fetch(PHYSIO + hypnos[0], ann, checksums[hypnos[0]]) if not perr else ("NOT_ATTEMPTED", "", "NOT_ATTEMPTED", "PSG_FAILURE")
        declared, header, body = edf_declared_bytes(psg) if not perr else ("", "FAIL", "FAIL")
        local = psg.stat().st_size if psg.exists() else ""
        rows.append({"dataset":"sleep_edf_sc","subject_id":subject,"recording_id":rec,"provider_url":PHYSIO+psg_rel,"http_status":ps,"provider_content_length":pcl,"local_bytes":local,"edf_declared_bytes":declared,"byte_delta":int(local)-int(declared) if isinstance(local,int) and isinstance(declared,int) else "","checksum_status":"MATCH" if pchk=="MATCH" and hchk=="MATCH" else f"PSG_{pchk};ANN_{hchk}","header_valid":header,"body_valid":body,"terminal_status":"ACQUIRED" if not perr and not herr and body=="PASS" else "EXCLUDED_PROVIDER_INTEGRITY","failure_code":perr or herr or ("EDF_DECLARED_BYTE_MISMATCH" if body != "PASS" else "")})

    for r in expected_isruc:
        rec = r["recording_id"]
        edf_rel = f"sub-{rec}/eeg/sub-{rec}_task-sleep_eeg.edf"
        event_rel = f"sub-{rec}/eeg/sub-{rec}_task-sleep_events.tsv"
        info = nemar.get(edf_rel)
        if not info:
            rows.append({"dataset":"isruc_s1","subject_id":rec,"recording_id":rec,"provider_url":NEMAR+edf_rel,"terminal_status":"EXCLUDED_ACQUISITION","failure_code":"NEMAR_MANIFEST_MISSING_EDF"})
            continue
        edf = RAW / "isruc-nemar/v1.0.1" / f"sub-{rec}_task-sleep_eeg.edf"
        events = RAW / "isruc-nemar/v1.0.1" / f"sub-{rec}_task-sleep_events.tsv"
        status, clen, checksum, error = fetch(NEMAR + edf_rel, edf, info["checksum"])
        estatus, eclen, echk, eerror = fetch(GITHUB + event_rel, events, None) if not error else ("NOT_ATTEMPTED", "", "NOT_ATTEMPTED", "EDF_FAILURE")
        declared, header, body = edf_declared_bytes(edf) if not error else ("", "FAIL", "FAIL")
        local = edf.stat().st_size if edf.exists() else ""
        rows.append({"dataset":"isruc_s1","subject_id":rec,"recording_id":rec,"provider_url":NEMAR+edf_rel,"http_status":status,"provider_content_length":clen,"local_bytes":local,"edf_declared_bytes":declared,"byte_delta":int(local)-int(declared) if isinstance(local,int) and isinstance(declared,int) else "","checksum_status":"MATCH" if checksum=="MATCH" and not eerror else f"EDF_{checksum};EVENT_{echk}","header_valid":header,"body_valid":body,"terminal_status":"ACQUIRED" if not error and not eerror and body=="PASS" else "EXCLUDED_PROVIDER_INTEGRITY","failure_code":error or eerror or ("EDF_DECLARED_BYTE_MISMATCH" if body != "PASS" else "")})

    if len(rows) != len(expected) or len({(r["dataset"],r["recording_id"]) for r in rows}) != len(expected):
        raise RuntimeError("provider terminal accounting invariant failed")
    audit_name = "provider_integrity_audit.csv" if args.shards == 1 else f"provider_integrity_audit.part-{args.shard_index:02d}-of-{args.shards:02d}.csv"
    with (REPORTS / audit_name).open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)
    summary = {"generated_at": datetime.now(timezone.utc).isoformat(), "expected":len(expected), "acquired":sum(r["terminal_status"]=="ACQUIRED" for r in rows), "excluded":sum(r["terminal_status"]!="ACQUIRED" for r in rows)}
    print(json.dumps(summary, sort_keys=True))

if __name__ == "__main__":
    main()
