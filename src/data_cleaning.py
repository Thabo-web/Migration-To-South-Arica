import pandas as pd 
from src.data_loader import load_data
#PYTHONPATH=. python3 src/data_cleaning.py

print("Migration to SA data of 7 rows:\n",df.head(8))
print("Description:\n ",df.describe())
print("Informatics:\t ",df.info())
print("# of Missing Values:\n", df.isnull().sum())
print("# of Duplicates: ", df.duplicated().sum())

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
    df = standardize_column_names(df) #standardize column names




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

def convert_to_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Convert specified columns of a DataFrame to numeric type.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose columns are to be converted.
    columns : list
        A list of column names to convert to numeric.

    Returns
    -------
    pd.DataFrame
        The DataFrame with specified columns converted to numeric type.
    """
    numeric_columns = [col for col in columns if col in df.columns]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df