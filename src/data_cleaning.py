import pandas as pd 
from src.data_loader import load_data
import pandas as pd
from typing import Iterable, Optional, Any
#PYTHONPATH=. python3 src/data_cleaning.py



def describe_data(df: pd.DataFrame) -> None:
    """Print a summary of the DataFrame, including head, description, info, missing values, and duplicates.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to describe.
    """
    print("Migration to SA data of 8 rows:\n\t\t", df.head(3))
    print("Description:\n ", df.describe())
    print("Informatics:\t ", df.info())
    print("Missing Values:\n", df.isnull().sum())
    print("Duplicates: ", df.duplicated().sum())



def load_cleaned_data(path: str = None) -> pd.DataFrame:
    """Load the cleaned World Bank CSV as a pandas DataFrame.

    Parameters
    ----------
    path : str, optional
        The path to the cleaned CSV file, by default None

    Returns
    -------
    pd.DataFrame
        The cleaned World Bank data as a pandas DataFrame.
    """
    df = load_data() #load the data from the default path or provided path

    describe_data(df) #describe the data before cleaning

    df = standardize_column_names(df) #standardize column names
    df = convert_to_numeric(df, columns=df.columns[4:])#convert columns from index 4 onward to numeric, coercing non-numeric values to NaN    
    df = rename_columns(df, column_mapping={"country_name": "Country Name", "country_code": "Country Code", "indicator_name": "Indicator Name", "indicator_code": "Indicator Code"}) #rename columns for clarity    
    df =  summarize_country_data(df, country_name="South Africa") #summarize data for South Africa
    df = resolve_missing_values(df) #resolve missing values
    df = save_cleaned_data(df) #save the cleaned data to a CSV file

    return df

def rename_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame: 
    """Rename columns of a DataFrame based on a provided mapping.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose columns are to be renamed.
    column_mapping : dict
        A dictionary mapping old column names to new column names.

    Returns
    -------
    pd.DataFrame
        The DataFrame with renamed columns.
    """
    df = standardize_column_names(df) #standardize column names before renaming
    df = df.rename(columns=column_mapping)
    describe_data(df) #describe the data after renaming columns

    return df

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose column names are to be standardized.

    Returns
    -------
    pd.DataFrame
        The DataFrame with standardized column names.
    """
    df.columns = (df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_',regex=False)
        .str.replace('[^a-zA-Z0-9_]', '',regex=True)
    )
    return df    

def convert_to_numeric(df: pd.DataFrame, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Convert the specified columns to numeric (coerce non-numeric to NaN).
    'columns' may be a list, pandas Index, or None.
    Returns a new DataFrame (does not modify input).
    """
    df = df.copy()

    # default to columns from index 4 onward if None
    if columns is None:
        columns = df.columns[4:]

    # normalize to a Python list of column names
    cols = list(columns)

    # ensure the columns exist in df
    cols = [c for c in cols if c in df.columns]

    # Convert each specified column to numeric safely
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

def summarize_country_data(df: pd.DataFrame, country_name: str) -> pd.DataFrame:
    """Summarize data for a specific country.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    country_name : str
        The name of the country to summarize.

    Returns
    -------
    pd.DataFrame
        A summary DataFrame for the specified country.
    """
    country_df = df[df['country_name'] == country_name]
    summary = country_df.describe(include='all')
    return summary

def resolve_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill numeric columns' missing values with column means; drop fully-empty columns."""
    df = df.copy()

    # drop columns that are entirely null (e.g., "Unnamed: 70")
    df = df.dropna(axis=1, how="all")

    # Try to coerce columns that look numeric but are object dtype
    for col in df.columns:
        if df[col].dtype == object:
            coerced = pd.to_numeric(df[col], errors="ignore")
            # if coercion changed values to numeric dtype, keep it
            if coerced.dtype != object:
                df[col] = coerced

    # Select numeric columns and compute their means
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return df

    means = df[numeric_cols].mean(numeric_only=True)

    # Fill numeric columns column-wise with their means (correct alignment by column name)
    df[numeric_cols] = df[numeric_cols].fillna(means)

    return df


def save_cleaned_data(df: pd.DataFrame, path: str = "data/cleaned_migration_data.csv") -> None:
    """Save the cleaned DataFrame to a CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned DataFrame to save.
    path : str, optional
        The path where the CSV file will be saved, by default "data/cleaned_migration_data.csv".
    """
    df.to_csv(path, index=False)
    print(f"Cleaned data saved to {path}")

if __name__ == "__main__":
    import sys
    import traceback

    try:
        df = load_cleaned_data()
    except FileNotFoundError as fnf_error:
        print(f"File not found error: {fnf_error}")
        sys.exit(1)
    except Exception as e:
        print("Error loading data:")
        traceback.print_exc()
        sys.exit(1)

    if df is None or df.empty:
        print("Loaded DataFrame is empty.")
        sys.exit(1)

    # show a summary
    describe_data(df)

    # save and report
    try:
        out_path = save_cleaned_data(df)  # expect a filepath string
        print(f"Cleaned data saved to: {out_path}")
        print(df.head(3))
    except Exception as e:
        print("Error saving cleaned data:")
        traceback.print_exc()
        sys.exit(1)