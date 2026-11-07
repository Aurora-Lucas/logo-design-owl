#!/usr/bin/env python3
"""Check unchanged deliverables against their pre-reorganization SHA-256."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'asset-integrity.json').read_text(encoding='utf-8'))
    failed = []
    for asset in manifest['assets']:
        file = ROOT / asset['path']
        if not file.is_file():
            failed.append(f'Missing: {asset["path"]}')
        elif (file.stat().st_size != asset['bytes'] or
              hashlib.sha256(file.read_bytes()).hexdigest() != asset['sha256']):
            failed.append(f'Changed: {asset["path"]}')
    if failed:
        print('\n'.join(failed), file=sys.stderr)
        return 1
    print(f'OK: all {len(manifest["assets"])} original logo deliverables are byte-for-byte unchanged.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
