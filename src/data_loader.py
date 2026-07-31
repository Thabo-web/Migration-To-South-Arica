import pandas as pd
from pathlib import Path
from typing import Optional


def _find_repo_root(start: Optional[Path] = None) -> Path:
    """Find the repository root by searching common markers starting from a few likely locations.

    Strategy:
    - Try a list of candidate starting points: the directory containing this file (if available)
      and the current working directory (cwd). This covers both script and notebook runs.
    - Walk upward from each candidate looking for marker files/dirs (.git, README.md, requirements.txt,
      pyproject.toml, or data). Return the first match found.
    - If nothing is found, fall back to the first existing candidate or cwd.
    """
    markers = {".git", "README.md", "requirements.txt", "pyproject.toml", "data"}

    candidates = []
    try:
        # directory where this file lives (when running as a module/script)
        file_dir = Path(__file__).resolve().parent
        candidates.append(file_dir)
        # also include the parent (repo layout like repo/src/...)
        candidates.append(file_dir.parent)
    except NameError:
        file_dir = None

    # always try cwd because notebooks often run with cwd set to the notebook folder
    candidates.append(Path.cwd())

    # de-duplicate while preserving order
    seen = set()
    uniq_candidates = []
    for c in candidates:
        try:
            rc = c.resolve()
        except Exception:
            rc = c
        if rc not in seen:
            seen.add(rc)
            uniq_candidates.append(c)

    for start_dir in uniq_candidates:
        cur = start_dir
        if not cur.exists():
            continue
        while True:
            if any((cur / m).exists() for m in markers):
                return cur
            if cur.parent == cur:
                break
            cur = cur.parent

    # Fallback: if none of the searches found markers, prefer the repo-layout guess (file_dir.parent)
    if file_dir is not None:
        guessed = file_dir.parent
        if guessed.exists():
            return guessed

    # final fallback
    return Path.cwd()


def _default_csv_path() -> Path:
    """Return the default CSV path inside the repository's data/ directory."""
    repo_root = _find_repo_root()
    return repo_root / "data" / "API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"


def load_data(path: Optional[str] = None, skiprows: int = 4, encoding: str = "utf-8-sig", low_memory: bool = False) -> pd.DataFrame:
    """Load the World Bank CSV as a pandas DataFrame.

    Parameters
    - path: optional path to the CSV. If None the default path inside the repo/data is used.
    - skiprows, encoding, low_memory: passed to pandas.read_csv

    Returns
    - pd.DataFrame

    Raises
    - FileNotFoundError if the CSV can't be located.
    - Any pandas read_csv exception bubbles up for the caller to handle.
    """
    csv_path = Path(path) if path else _default_csv_path()

    # If the calculated path doesn't exist, try a common fallback in case cwd is different
    if not csv_path.exists():
        alt = Path.cwd() / "data" / csv_path.name
        if alt.exists():
            csv_path = alt

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    df = pd.read_csv(csv_path, skiprows=skiprows, encoding=encoding, low_memory=low_memory)
    return df


if __name__ == "__main__":
    # When executed as a script, load and print a quick summary.
    try:
        csv_path = _default_csv_path()
        print("Looking for CSV at:", csv_path)
        # Also print which repo root was detected for debugging
        print("Repo root detected:", _find_repo_root())
        df = load_data()
        print("Rows:", len(df))
        print(df.head(5))
    except Exception as e:
        print("Error loading CSV:", e)
