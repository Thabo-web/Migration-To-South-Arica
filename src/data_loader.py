import pandas as pd

RAW_PATH = "/workspaces/Migration-To-South-Africa/data/API_SM.POP.NETM_DS2_en_csv_v2_34232.csv"

print("Reading:",RAW_PATH)

df = pd.read_csv(RAW_PATH,skiprows=4)
print("Rows:", len(df))
print(df.head(5))