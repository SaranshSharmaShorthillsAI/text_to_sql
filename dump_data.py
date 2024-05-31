import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os 


username= os.getenv('username')
password=os.getenv('password')
host= os.getenv('host')
database=os.getenv('database')
# Encode the password
encoded_password = quote_plus(password)
 
# Create the MySQL connection string
connection_string = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}/{database}"
 
# Create the engine
engine = create_engine(connection_string)
df = pd.read_csv('bk_sample_data/sample_data_complete_assessment.csv')
 
# Replace 'sam_keys' with the name of your MySQL table
table_name = 'sample_data_complete_assessment'

try:
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print("Data successfully inserted into MySQL table:", table_name)
except Exception as e:
    print("Error:", e)
 
 

 