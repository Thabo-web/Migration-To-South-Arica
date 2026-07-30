import pandas as pd
from pathlib import Path
import sys

# Compute repository root relative to this file (works when run as module/script)
BASE = Path(__file__).resolve().parents[1]  # repo root
RAW_CSV = BASE / "data" / "API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"

# If running from a notebook where __file__ may not exist, fall back to cwd
if not RAW_CSV.exists():
    RAW_CSV = Path.cwd() / "data" / "API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"

print("Reading:", RAW_CSV.resolve())
if not RAW_CSV.exists():
    print("ERROR: CSV not found at:", RAW_CSV)
    sys.exit(1)

# World Bank CSVs sometimes have an initial 4-line header and a UTF BOM.
# Use encoding='utf-8-sig' to strip BOM, and low_memory=False to avoid dtype warnings.
df = pd.read_csv(RAW_CSV, skiprows=4, encoding="utf-8-sig", low_memory=False)
print("Rows:", len(df))
print(df.head(5))
