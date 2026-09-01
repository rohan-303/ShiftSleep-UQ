"""Pure-Python EDF/EDF+ fixed-header parser.

This module reads only header bytes. It does not decode or process signal samples.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO


class EDFHeaderError(ValueError):
    """Raised when an EDF fixed/signal header is malformed or incomplete."""


def _field(raw: bytes) -> str:
    return raw.decode("ascii", errors="replace").strip()


def _number(raw: bytes, kind: type[int] | type[float]) -> int | float:
    text = _field(raw)
    try:
        return kind(text)
    except (TypeError, ValueError) as exc:
        raise EDFHeaderError(f"invalid numeric EDF field: {text!r}") from exc


@dataclass(frozen=True)
class EDFHeader:
    version: str
    patient: str
    recording: str
    start_date: str
    start_time: str
    header_bytes: int
    reserved: str
    records: int
    record_duration_seconds: float
    signal_count: int
    labels: tuple[str, ...]
    physical_dimensions: tuple[str, ...]
    physical_min: tuple[float, ...]
    physical_max: tuple[float, ...]
    digital_min: tuple[int, ...]
    digital_max: tuple[int, ...]
    samples_per_record: tuple[int, ...]
    signal_reserved: tuple[str, ...]

    @property
    def edf_plus(self) -> bool:
        return self.reserved.startswith("EDF+") or self.reserved.startswith("EDF+D") or self.reserved.startswith("EDF+C")

    @property
    def duration_seconds(self) -> float:
        return self.records * self.record_duration_seconds

    @property
    def sampling_frequencies(self) -> tuple[float, ...]:
        return tuple(n / self.record_duration_seconds for n in self.samples_per_record)


def parse_edf_header(data: bytes) -> EDFHeader:
    """Parse a complete EDF header byte string, without reading signal bodies."""
    if len(data) < 256:
        raise EDFHeaderError("EDF fixed header requires at least 256 bytes")
    n = int(_field(data[252:256]) or "0")
    if n <= 0:
        raise EDFHeaderError("EDF signal count must be positive")
    required = 256 + n * 256
    if len(data) < required:
        raise EDFHeaderError(f"incomplete EDF signal header: need {required}, got {len(data)}")
    fixed = {
        "version": _field(data[0:8]),
        "patient": _field(data[8:88]),
        "recording": _field(data[88:168]),
        "start_date": _field(data[168:176]),
        "start_time": _field(data[176:184]),
        "header_bytes": int(_field(data[184:192]) or "0"),
        "reserved": _field(data[192:236]),
        "records": int(_field(data[236:244]) or "0"),
        "record_duration_seconds": float(_field(data[244:252]) or "0"),
        "signal_count": n,
    }
    if fixed["header_bytes"] != required:
        raise EDFHeaderError("header byte count does not match signal count")
    if fixed["records"] < -1 or fixed["record_duration_seconds"] <= 0:
        raise EDFHeaderError("invalid EDF record count or duration")
    base = 256
    labels = tuple(_field(data[base + i * 16 : base + (i + 1) * 16]) for i in range(n))
    base += 16 * n
    base += 80 * n  # transducer type
    dimensions = tuple(_field(data[base + i * 8 : base + (i + 1) * 8]) for i in range(n))
    base += 8 * n
    physical_min = tuple(float(_field(data[base + i * 8 : base + (i + 1) * 8])) for i in range(n))
    base += 8 * n
    physical_max = tuple(float(_field(data[base + i * 8 : base + (i + 1) * 8])) for i in range(n))
    base += 8 * n
    digital_min = tuple(int(_field(data[base + i * 8 : base + (i + 1) * 8])) for i in range(n))
    base += 8 * n
    digital_max = tuple(int(_field(data[base + i * 8 : base + (i + 1) * 8])) for i in range(n))
    base += 8 * n
    base += 80 * n  # prefiltering
    samples = tuple(int(_field(data[base + i * 8 : base + (i + 1) * 8])) for i in range(n))
    base += 8 * n
    reserved = tuple(_field(data[base + i * 32 : base + (i + 1) * 32]) for i in range(n))
    return EDFHeader(**fixed, labels=labels, physical_dimensions=dimensions, physical_min=physical_min, physical_max=physical_max, digital_min=digital_min, digital_max=digital_max, samples_per_record=samples, signal_reserved=reserved)


def read_edf_header(stream: BinaryIO) -> EDFHeader:
    """Read exactly the fixed plus signal header from a seekable binary stream."""
    fixed = stream.read(256)
    if len(fixed) < 256:
        raise EDFHeaderError("stream ended before EDF fixed header")
    n = int(_field(fixed[252:256]) or "0")
    if n <= 0:
        raise EDFHeaderError("EDF signal count must be positive")
    rest = stream.read(n * 256)
    return parse_edf_header(fixed + rest)
