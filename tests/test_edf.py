import io

import pytest

from shiftsleep_uq.data.edf import EDFHeaderError, parse_edf_header, read_edf_header


def _edf_header(labels=("EEG Fpz-Cz", "EOG horizontal")):
    n = len(labels)
    def f(value, width): return value.ljust(width).encode("ascii")
    fixed = b"0       " + f("X", 80) + f("R", 80) + f("01.01.26", 8) + f("01.01.01", 8) + f(str(256 + n*256), 8) + f("EDF+C", 44) + f("1", 8) + f("30", 8) + f(str(n), 4)
    fields = [
        b"".join(f(x,16) for x in labels), b"".join(f("",80) for _ in labels), b"".join(f("uV",8) for _ in labels),
        b"".join(f("-100",8) for _ in labels), b"".join(f("100",8) for _ in labels),
        b"".join(f("-32768",8) for _ in labels), b"".join(f("32767",8) for _ in labels),
        b"".join(f("",80) for _ in labels), b"".join(f("3000",8) for _ in labels),
        b"".join(f("",32) for _ in labels),
    ]
    return fixed + b"".join(fields)


def test_parse_header_and_sampling():
    h = parse_edf_header(_edf_header())
    assert h.signal_count == 2
    assert h.labels == ("EEG Fpz-Cz", "EOG horizontal")
    assert h.edf_plus is True
    assert h.sampling_frequencies == (100.0, 100.0)


def test_stream_reader():
    h = read_edf_header(io.BytesIO(_edf_header()))
    assert h.duration_seconds == 30.0


def test_malformed_header_rejected():
    with pytest.raises(EDFHeaderError):
        parse_edf_header(b"short")
    bad = bytearray(_edf_header()); bad[252:256] = b"0   "
    with pytest.raises(EDFHeaderError):
        parse_edf_header(bytes(bad))
