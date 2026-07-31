# Contributing

Thanks for contributing! This document describes the recommended development workflow, testing, and notebook practices for this repository.

## Git workflow (industry-recommended)

- Keep your local branch up to date with `main`:
  - Preferred: rebase workflow
    - git fetch origin
    - git checkout -b my-feature
    - work, commit locally
    - git fetch origin
    - git rebase origin/main
    - resolve conflicts if any, then git rebase --continue
    - push: git push --force-with-lease origin my-feature
  - If you prefer merge commits instead, use `git merge origin/main` instead of rebase.

- Make small, focused commits with descriptive messages.
- Use `--force-with-lease` when pushing rebased branches to avoid overwriting others' work.

## Pull Requests

- Create a PR from your feature branch to `main`.
- Add a clear title and description explaining the problem and how your change fixes it.
- Link related issues (e.g., `Fixes #2`).
- Ensure all CI checks pass before merging.

## Tests & CI

- This repo uses pytest and a GitHub Actions workflow to run tests on push/PR.
- To run tests locally:
  - python -m pip install -r requirements.txt
  - pytest -q
- Add tests for new behavior and edge cases (e.g., different CSV encodings, skiprows variations, large-file low-memory mode).

## Notebooks

Notebooks are convenient for exploration but are harder to review and merge. Follow these recommendations:

- Keep analysis logic inside `src/` as reusable functions and modules. Notebooks should call into `src/` rather than contain complex logic.
- Use the loader in `src/data_loader.py` to read data rather than ad-hoc `pd.read_csv("data/...")` with relative paths.
- If you must edit notebooks, consider using jupytext (paired `.py` version) to make diffs readable and merge conflicts easier:
  - Install jupytext and pair the notebook: `jupytext --set-formats ipynb,py notebooks/migration_analysis.ipynb`
- For CI coverage of notebooks, consider `nbval` or `papermill` to execute notebooks in CI.

## Running the notebook reproducibly

- The repository contains a lightweight loader that detects the repo root and provides an explicit CSV path to avoid relying on the notebook working directory.
- In Jupyter, either run the top cell that adds the repo root to `sys.path` (already present in `notebooks/migration_analysis.ipynb`), or run the notebook from the repo root with:
  - `%cd ..` (inside the notebook) before running cells that use relative paths
  - Or launch Jupyter from the repo root: `jupyter lab`

## Linting & Formatting (optional)

- Add and run linters (flake8, ruff) and formatters (black) to maintain consistent style.
- Consider adding pre-commit hooks via `pre-commit` to run checks before commits.

## Troubleshooting

- ModuleNotFoundError: No module named 'src'
  - Ensure the notebook's sys.path includes the repo root or install the package in editable mode: `pip install -e .`.

- Stale imports in notebooks
  - Use `importlib.reload(module)` after editing `src/` modules, or restart the kernel and Run All.

- Divergent branches
  - If `git pull` reports divergent branches, prefer rebasing onto `origin/main` and use `--force-with-lease` to push rebased branches.

## Contact

If you have questions or need help with the repository setup, open an issue and tag @Thabo-web.
