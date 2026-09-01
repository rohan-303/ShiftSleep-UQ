"""Inspect EDF headers via HTTP Range requests without downloading signal bodies."""
from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
from urllib.request import Request, urlopen

from shiftsleep_uq.data.edf import EDFHeaderError, parse_edf_header

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
    "sleep-edf": {
        "records": ROOT / "data/raw/metadata/sleep-edfx/1.0.0/RECORDS",
        "base": "https://physionet.org/files/sleep-edfx/1.0.0/",
        "out": ROOT / "reports/sleep_edf_channel_inventory.csv",
        "dataset": "Sleep-EDF Expanded v1.0.0",
    },
    "cap": {
        "records": ROOT / "data/raw/metadata/capslpdb/1.0.0/RECORDS",
        "base": "https://physionet.org/files/capslpdb/1.0.0/",
        "out": ROOT / "reports/cap_channel_inventory.csv",
        "dataset": "CAP Sleep Database v1.0.0",
    },
}


def range_bytes(url: str, end: int) -> tuple[bytes, str | None]:
    req = Request(url, headers={"Range": f"bytes=0-{end}"})
    with urlopen(req, timeout=45) as response:
        return response.read(), response.headers.get("Content-Range")


def inspect(url: str) -> dict[str, object]:
    fixed, fixed_range = range_bytes(url, 255)
    if len(fixed) != 256 or not fixed_range or not fixed_range.startswith("bytes 0-255/"):
        raise RuntimeError(f"range unsupported or incomplete fixed header: {fixed_range!r} ({len(fixed)} bytes)")
    signal_count = int(fixed[252:256].decode("ascii").strip())
    header_end = 256 + signal_count * 256 - 1
    header, full_range = range_bytes(url, header_end)
    parsed = parse_edf_header(header)
    return {
        "url": url, "range_supported": "TRUE", "content_range": full_range or "NOT_VERIFIED",
        "signal_count": parsed.signal_count, "labels": "|".join(parsed.labels),
        "physical_dimensions": "|".join(parsed.physical_dimensions),
        "sampling_hz": "|".join(f"{x:g}" for x in parsed.sampling_frequencies),
        "samples_per_record": "|".join(map(str, parsed.samples_per_record)),
        "records": parsed.records, "record_duration_s": parsed.record_duration_seconds,
        "duration_s": parsed.duration_seconds, "edf_plus": parsed.edf_plus,
        "patient_header_redacted": "TRUE", "header_bytes_inspected": len(header),
        "status": "VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=CONFIG)
    parser.add_argument("--limit", type=int, default=0, help="optional local audit limit; 0 means all")
    args = parser.parse_args()
    cfg = CONFIG[args.dataset]
    raw = [line.strip() for line in cfg["records"].read_text().splitlines() if line.strip() and not line.startswith("#")]
    edfs = [line for line in raw if line.lower().endswith(".edf")]
    if args.limit:
        edfs = edfs[: args.limit]
    rows = []
    for i, relative in enumerate(edfs, 1):
        url = cfg["base"] + relative
        try:
            row = inspect(url)
            row.update({"dataset": cfg["dataset"], "recording_path": relative})
        except Exception as exc:  # preserve audit failures rather than hiding them
            row = {"dataset": cfg["dataset"], "recording_path": relative, "url": url, "range_supported": "NOT_VERIFIED", "status": f"ERROR:{type(exc).__name__}:{exc}"}
        rows.append(row)
        if i % 25 == 0 or i == len(edfs):
            print(f"{cfg['dataset']}: {i}/{len(edfs)}")
        time.sleep(0.02)
    fields = ["dataset", "recording_path", "url", "range_supported", "content_range", "signal_count", "labels", "physical_dimensions", "sampling_hz", "samples_per_record", "records", "record_duration_s", "duration_s", "edf_plus", "patient_header_redacted", "header_bytes_inspected", "status"]
    cfg["out"].parent.mkdir(exist_ok=True)
    with cfg["out"].open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    verified = sum(r.get("status") == "VERIFIED" for r in rows)
    print(f"output={cfg['out']} rows={len(rows)} verified={verified} failed={len(rows)-verified}")


if __name__ == "__main__":
    main()
