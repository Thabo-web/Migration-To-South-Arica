import pandas as pd
from pathlib import Path
from typing import Optional


def _default_csv_path() -> Path:
    """Resolve the default CSV path relative to the repository.

    Behavior:
    - When run as a module/file, use the location of this file to find the repo root.
    - When run in a notebook (no __file__), fall back to cwd.
    """
    try:
        base = Path(__file__).resolve().parents[1]
    except NameError:
        base = Path.cwd()
    return base / "data" / "API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"


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
    if not csv_path.exists():
        # Try fallback to cwd/data if the calculated path isn't present
        alt = Path.cwd() / "data" / csv_path.name
        if alt.exists():
            csv_path = alt

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    # World Bank CSVs sometimes have an initial header and a UTF BOM.
    df = pd.read_csv(csv_path, skiprows=skiprows, encoding=encoding, low_memory=low_memory)
    return df


if __name__ == "__main__":
    # When executed as a script, load and print a quick summary.
    try:
        df = load_data()
        print("Reading:", _default_csv_path().resolve())
        print("Rows:", len(df))
        print(df.head(5))
    except Exception as e:
        print("Error loading CSV:", e)
