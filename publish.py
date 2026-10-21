#!/usr/bin/env python3
r"""
V:\__marinus__\01_Docs\publish.py
=================================
CLI Entrypoint for Tesseract City Documentation Publishing.

Delegates execution to the substrate Task Master:
  V:\__sentinus__\00_Tasks\__ssot_task_master.py --event docsPublish

Stages:
  1. 01_generate.py : Regenerate AOIT manifest and API/SDK/LMNOP documentation.
  2. 02_guard.py    : Handbook Deathgrip checks (>2KB) and secrets firewall.
  3. 03_commit.py   : Commit & push in authoring repository (tesseract-docs).
  4. 04_mirror.py   : Mirror to gewey.github.io/tesseract_city/docs & update submodule.
  5. 05_archive.py  : (Optional with --release) Package zip to B:\__general_backup\docs_archive\.

Usage:
  python publish.py              # Run full publish & mirror sync
  python publish.py --release    # Run publish, mirror sync, and seal immutable release archive
  python publish.py --dry-run    # Simulate stages without writing or pushing
"""

import sys
import os
import subprocess
from pathlib import Path

TASK_MASTER = Path("V:/__sentinus__/00_Tasks/__ssot_task_master.py").resolve()


def main():
    if not TASK_MASTER.is_file():
        print(f"❌ Substrate Task Master not found at {TASK_MASTER}", file=sys.stderr)
        sys.exit(1)

    cmd = [sys.executable, str(TASK_MASTER), "--event", "docsPublish"] + sys.argv[1:]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
