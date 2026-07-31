# Migration-To-South-Arica

A small data analysis project that investigates migration (World Bank SM.POP.NETM) with a reproducible notebook and a reusable loader in `src/`.

Status
- Basic data loader (src/data_loader.py)
- Notebook: `notebooks/migration_analysis.ipynb` uses the loader
- Tests: `tests/test_data_loader.py` (pytest)
- CI: GitHub Actions workflow runs pytest on push/PR
- CONTRIBUTING.md added with recommended workflows

Quick summary
- Keep analysis logic in `src/` and use notebooks for interactive exploration.
- The loader detects the repository root and provides an explicit CSV path so notebooks don't depend on the kernel working directory.

Repository layout
- data/                              # CSV files (not committed here if large)
- notebooks/migration_analysis.ipynb # exploratory notebook (calls src.data_loader)
- src/data_loader.py                 # repo-aware loader (use load_data())
- src/analysis.py                    # small example analysis helper
- tests/test_data_loader.py          # pytest tests for the loader
- .github/workflows/ci.yml           # CI to run pytest
- CONTRIBUTING.md                    # contribution & git workflow guidance

Quick start (local)
1. Clone and switch to main
   git clone https://github.com/Thabo-web/Migration-To-South-Arica
   cd Migration-To-South-Arica
   git checkout main

2. Install dependencies
   python -m pip install --upgrade pip
   pip install -r requirements.txt

3. Run tests
   pytest -q

4. Load the real CSV (explicit check)
   python - <<'PY'
   from src import data_loader as dl
   import importlib
   importlib.reload(dl)
   print("Repo root:", dl._find_repo_root())
   print("Default CSV:", dl._default_csv_path())
   try:
       df = dl.load_data(path=str(dl._find_repo_root() / "data" / "API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"))
       print("Loaded shape:", df.shape)
   except Exception as e:
       print("Error:", e)
   PY

Running the notebook (recommended)
- Open Jupyter Lab from repo root so imports resolve:
  jupyter lab
- Or, in the notebook run the first cell which:
  - Adds repo root to sys.path when necessary
  - Imports and reloads `src.data_loader`
  - Loads the CSV via an explicit repo-root path
- Always restart the kernel and Run All after changing code in `src/` or use `importlib.reload()`.

Data
- Place the World Bank CSV in `data/API_SM.POP.NETM_DS2_en_csv_v2_34232.csv`
- The loader defaults to that path; it will raise FileNotFoundError if missing.
- If your data is large, consider configuring loader parameters (`low_memory=True`) or loading in chunks.

Tests & CI
- Tests are in `tests/` and run in CI (GitHub Actions).
- To run locally:
  pip install -r requirements.txt
  pytest -q

Common issues & fixes
- FileNotFoundError for CSV:
  - Notebook kernel cwd may be `notebooks/`; run the top cell that sets sys.path or start Jupyter from repo root.
- ModuleNotFoundError: No module named `src`:
  - Ensure you launched Jupyter from repo root or add repo root to PYTHONPATH / install with `pip install -e .`.
- Stale module behavior in notebooks:
  - Use `importlib.reload(module)` or restart kernel and Run All.

Contributing
- See CONTRIBUTING.md for the recommended git workflow (rebase preferred), testing, and notebook practices.
- Make small focused commits, add tests for new behavior, and open a PR.

Next steps you might want
- Add nbval or papermill CI to run notebooks
- Pair notebooks with jupytext to improve diffs and merges
- Expand tests for edge cases (BOM handling, skiprows variations, encoding)

Contact
- Open an issue or draft a PR; tag @Thabo-web for review.

License
- Add a LICENSE file to indicate the project's licensing (MIT is used here by default).