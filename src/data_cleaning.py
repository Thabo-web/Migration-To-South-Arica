import pandas as pd 
from src.data_loader import load_data
#PYTHONPATH=. python3 src/data_cleaning.py



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

    print("Migration to SA data of 7 rows:\n",df.head(8))
    print("Description:\n ",df.describe())
    print("Informatics:\t ",df.info())
    print("# of Missing Values:\n", df.isnull().sum())
    print("# of Duplicates: ", df.duplicated().sum()) 

    df = standardize_column_names(df) #standardize column names
    df = convert_to_numeric(df, columns=df.columns[4:]) #convert specified columns to numeric

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
    numeric_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + columns
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
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

def remove_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values from the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame from which to remove missing values.

    Returns
    -------
    pd.DataFrame
        The DataFrame with rows containing missing values removed.
    """
    missing_val = df.isnull().sum()
    return df.dropna()

if __name__ == "__main__":
    # When executed as a script, load and print a quick summary of the cleaned data.
    try:
        df = load_cleaned_data()
        print("Cleaned Data Summary:\n", df.describe())
    except Exception as e:
        print(f"Error loading cleaned data: {e}")