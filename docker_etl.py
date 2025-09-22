import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os

# a url to a CSV file
url = "https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2023-financial-year-provisional/Download-data/annual-enterprise-survey-2023-financial-year-provisional.csv"

# postgres connection details from environment variables
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')

# create a connection string
conn_string = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
conn = create_engine(conn_string) # create a SQLAlchemy engine

# table name in the database
db_table = "finance_data"

def extract_data(url: str) -> pd.DataFrame:
    """Extract data from the CSV file located at the specified URL and convert to dataframe."""
    try:
        data = pd.read_csv(url)
        print("Data extraction successful.")
        # save the extracted data to a CSV file locally
        data.to_csv('extracted_data.csv', index=False)
        # return the dataframe
        return data
    except Exception as e:
        print(f"Error during data extraction: {e}")
        return None
    

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Transform the data by renaming columns and filtering."""
    new_cols = [col.lower() for col in data.columns] # change all column names to lowercase
    data.columns = new_cols # rename columns with new column names
    # select only the columns: year, Value, Units, variable_code
    filtered_data = data[['year', 'value', 'units', 'variable_code']]
    return filtered_data

def load_data(data: pd.DataFrame, conn: create_engine) -> None:
    """Load the transformed data to a PostgreSQL database."""
    try:
        data.to_sql(db_table, con=conn, if_exists='replace', index=False)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error during data loading: {e}")

# run the ETL process
data = extract_data(url)
if data is not None:
    transformed_data = transform_data(data) 
    load_data(transformed_data, conn)

# confirm data is loaded
query = f"SELECT * FROM {db_table} LIMIT 5;"
df_query = pd.read_sql(query, con=conn)
print("\nQuery results from database to confirm data is loaded:")
print(df_query)