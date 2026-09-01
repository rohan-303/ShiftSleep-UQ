"""Metadata-first dataset schema utilities for ShiftSleep-UQ."""

from .edf import EDFHeaderError, EDFHeader, parse_edf_header

__all__ = ["EDFHeaderError", "EDFHeader", "parse_edf_header"]
