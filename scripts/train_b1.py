#!/usr/bin/env python
"""Fail-closed B1 entrypoint.

Step 13 freezes the protocol only. Full B1 optimization is reserved for Step 14.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="B1 protocol-only entrypoint")
    parser.add_argument("--protocol-check", action="store_true")
    parser.add_argument("--execute", action="store_true", help="reserved for Step 14; always rejected in Step 13")
    args = parser.parse_args()
    if args.execute:
        raise SystemExit("STEP13_TRAINING_FORBIDDEN: train_b1.py is protocol-only; execute Step 14 separately")
    if not args.protocol_check:
        parser.error("use --protocol-check; full training is forbidden in Step 13")
    forbidden = []
    for pattern in ("artifacts/models/b1_moddrop/**/*.pt", "artifacts/predictions/b1_moddrop/**/*", "artifacts/normalization/b1/**/*"):
        forbidden.extend(ROOT.glob(pattern))
    if forbidden:
        raise SystemExit("STEP13_OUTPUT_BOUNDARY_VIOLATION: " + ", ".join(str(p) for p in forbidden))
    print(json.dumps({"status": "B1_PROTOCOL_ONLY", "full_training": "NOT_EXECUTED", "step14_required": True}, sort_keys=True))


if __name__ == "__main__":
    main()
