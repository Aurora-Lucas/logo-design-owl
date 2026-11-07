#!/usr/bin/env python3
"""Regenerate this project's board using the shared presentation layout."""
from pathlib import Path
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    subprocess.run([sys.executable, str(PROJECT.parent / 'scripts/make_previews.py'),
                    '--project', PROJECT.name], check=True)
