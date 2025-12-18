#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
STRUCTURE_FILE = ROOT / 'structure.txt'
STAGING_DIR = ROOT / 'staging'


def parse_outline(outline_text):
    """
    Parse `tree`-style outlines with Unicode box-drawing.
    Depth is computed from the characters before the first '├' or '└'.
    Each level in that prefix is represented by either '│  ' or '   ' (3 chars).
    """
    paths = []
    stack = []

    for raw in outline_text.splitlines():
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        if line.lstrip().startswith(("'''", '```')):
            continue

        # Root-only line (e.g., "story-engine/")
        if not any(ch in line for ch in ('├', '└')):
            name = line.strip()
            depth = 0
        else:
            # Split at the first branch character and compute depth by prefix width in groups of 3
            m = re.search(r'[├└]', line)
            prefix = line[:m.start()] if m else ''
            # Normalize tabs just in case
            prefix = prefix.replace('\t', '  ')
            depth = (len(prefix) // 3) + 1  # branch lines are children of the root

            # Extract the name after '├─' or '└─' (1+ '─' tolerated)
            m2 = re.search(r'[├└]─+\s*(.+)$', line)
            if not m2:
                # If formatting is odd, skip safely
                continue
            name = m2.group(1).strip()

        # Name may include trailing comment; take the path token only
        name = name.split(' ')[0]
        is_dir = name.endswith('/')
        clean_name = name.rstrip('/')

        # Adjust stack to current depth
        while len(stack) > depth:
            stack.pop()
        if len(stack) == depth:
            stack.append(clean_name)
        else:
            # If outline is malformed, reset
            stack = [clean_name]

        path = '/'.join(stack)
        if is_dir:
            path += '/'
        paths.append(path)

    return paths


def create_structure(paths, root_dir=ROOT):
    for p in paths:
        is_dir = p.endswith('/')
        full_path = Path(root_dir) / p

        if is_dir:
            full_path.mkdir(parents=True, exist_ok=True)
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch(exist_ok=True)


def load_structure(structure_path=STRUCTURE_FILE):
    try:
        text = structure_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise SystemExit(f'Missing structure file: {structure_path}')

    if not text.strip():
        raise SystemExit(f'Structure file is empty: {structure_path}')

    return text


def reset_staging(staging_dir=STAGING_DIR):
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    outline_text = load_structure()
    paths = parse_outline(outline_text)

    if not paths:
        sys.exit('No paths parsed from structure.txt')

    reset_staging()
    create_structure(paths, root_dir=STAGING_DIR)
    print(f'Created structure under {STAGING_DIR}:', *paths, sep='\n- ')
