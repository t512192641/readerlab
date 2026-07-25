#!/usr/bin/env python3
"""Compatibility entry for the archived clean-seed validator.

This root command remains only so historical receipts and replay scripts keep
working. Current project health uses ``python3 -B tests/entry.py``.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEGACY_VALIDATOR = ROOT / "archive/legacy-code/validate-clean-seed.py"
LEGACY_SHA256 = "6f7220c9e492c5e94291728c5242f3ce8818b0c0c1148d581700d68763d6b855"


def main() -> None:
    payload = LEGACY_VALIDATOR.read_bytes()
    observed = hashlib.sha256(payload).hexdigest()
    if observed != LEGACY_SHA256:
        raise SystemExit(
            "archived clean-seed validator identity mismatch: "
            f"expected {LEGACY_SHA256}, observed {observed}"
        )

    namespace = {
        "__builtins__": __builtins__,
        "__file__": str(ROOT / "validate.py"),
        "__name__": "__main__",
        "__package__": None,
    }
    exec(compile(payload, str(LEGACY_VALIDATOR), "exec"), namespace)


if __name__ == "__main__":
    main()
