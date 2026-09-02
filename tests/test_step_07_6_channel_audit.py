from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from step_07_6_channel_schema_audit import decode_label_field


def test_decode_label_field_strips_only_edf_padding():
    raw = b"C3-A2           "
    result = decode_label_field(raw)
    assert result["decoded_before_cleanup"] == "C3-A2           "
    assert result["decoded_after_padding_strip"] == "C3-A2"
    assert result["raw_hex"] == raw.hex()


def test_decode_label_field_preserves_internal_bytes():
    raw = b"LOC\x00-A2         "
    result = decode_label_field(raw)
    assert result["contains_nul"] is True
    assert result["decoded_after_padding_strip"] == "LOC\x00-A2"
