import pandas as pd
from pathlib import Path
from typing import Optional


def _find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk up from `start` (or this file) to find the repository root.

    Looks for common marker files/dirs (.git, README.md, requirements.txt, pyproject.toml, data)
    and returns the first directory that contains any of those markers. If nothing is found,
    returns the starting path or cwd.
    """
    markers = {".git", "README.md", "requirements.txt", "pyproject.toml", "CONTRIBUTING.md", "data"}
    try:
        cur = (start or Path(__file__).resolve().parent)#Absolute path of the current file's directory
    except NameError:
        cur = (start or Path.cwd())#current working directory if __file__ is not defined (e.g., in interactive mode)

    if not cur.exists():
        cur = Path.cwd()

    while True:
        if any((cur / m).exists() for m in markers):
            return cur
        if cur.parent == cur:
            # Reached filesystem root, give up and return start/cwd
            return start or Path.cwd()
        cur = cur.parent


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

    # If the calculated path doesn't exist, fallback in case cwd is different
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
        print(f"Looking for CSV at {csv_path}")
        df = load_data()
        
        print("Dimensions: ", df.shape)
        print(df.head())
    except Exception as e:
        print("Error loading CSV: ", e)
