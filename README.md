# make-folders-files

Build a folder/file skeleton from an LLM-style `tree` diagram and drop it into `staging/` for easy copy/paste.

## Why use it?

- Turn a ChatGPT-style outline into real directories and empty files in seconds.
- Safe by default: `staging/` is wiped and rebuilt each run, leaving the rest of your disk untouched.
- Robust parsing: tolerates missing root slashes, names with spaces, and fenced code blocks around the outline.

## Requirements

- Python 3.8+ (`python3` on macOS/Linux, `python` on Windows).
- An outline that starts with a root line (e.g., `my-app/`) and marks directories with a trailing `/`. If the root line omits `/`, it is treated as a directory automatically.

## Input format

- Use box-drawing branches: `├─`, `└─`, `│` with spacing like the `tree` command outputs.
- Trailing `/` = directory; no trailing `/` = file.
- Names with spaces are supported; keep the indentation aligned.
- You may wrap the outline in ``` or ''' fences; these lines are ignored.

## Quick start

1) Paste your outline into `structure.txt`.
2) Run:
   - macOS/Linux: `python3 run.py`
   - Windows: `python run.py`
3) Check the generated structure under `staging/…` and move it wherever you need it.

## Example input

```
story-engine/
├─ pyproject.toml
├─ README.md
├─ backend/
│  ├─ app/
│  │  ├─ main.py
└─ frontend/
   └─ src/
      └─ App.tsx
```

## What gets created

- All directories from the outline.
- Empty files for every non-directory entry.
- Everything lives under `staging/<root-name>/` so your working folders stay clean.

## Troubleshooting

- Nothing created: ensure the outline has a root line and uses the box-drawing characters shown above.
- Wrong depth: re-align the vertical bars/spaces so each level is three characters (`│` or `   `) before a branch.
- Keep data: copy anything out of `staging/` before rerunning, since it is deleted on each run.
