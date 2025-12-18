# make-folders-files
Create a folder/file skeleton from an LLM-style tree diagram.

## What it does
- Reads a `tree`-style outline from `structure.txt` (Unicode branches like `├─`, `└─`, `│`).
- Wipes and recreates the `staging/` directory on each run.
- Builds the described directories and empty files so you can copy them into a new repo.

## Requirements
- Python 3.8+ available as `python3` (macOS/Linux) or `python` (Windows).
- The outline should include a root folder line (e.g., `my-app/`) and use trailing `/` to mark directories.

## Quick start
1. Paste your outline into `structure.txt`. You can leave it inside triple backticks or single quotes; those fences are ignored.
2. Run:
   - macOS/Linux: `python3 run.py`
   - Windows: `python run.py`
3. Inspect the generated files under `staging/…` and move them where you need them.

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

## Tips
- Each run deletes and recreates `staging/`, so copy out anything you want to keep before rerunning.
- If nothing is created, make sure the outline starts with a root line and uses the box-drawing characters shown above.
- The script creates empty files; fill them in after you copy the structure to your project.***
