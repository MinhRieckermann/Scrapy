import pandas as pd
import pyodbc
from simple_salesforce import Salesforce

# Connect to Salesforce
sf = Salesforce(username='tuan.na@rieckermann.com.jrdev', password='Nat@2021jr', security_token='oQZgAhoa6VPUvS95XkcMLqDAE', domain='test')

# Perform a dynamic SOQL query to select all fields from the Account table
describe_fields = sf.Account.describe()['fields']
field_names = [field['name'] for field in describe_fields]
query = f"SELECT {', '.join(field_names)} FROM Account"
result = sf.query_all(query)
records = result['records']

# Convert the records to a list of dictionaries
records = [record['attributes'] for record in records]

# Get the column names from the first record
columns = list(records[0].keys())

# Specify the table name in SQL Server
table_name = 'Account'

# Assuming you have established a successful connection to SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=Salesforce_DB;UID=sa;PWD=1234')

# Check if the table exists, and create it if it doesn't
cursor = conn.cursor()
existing_tables = [table.table_name for table in cursor.tables(tableType='TABLE')]
if table_name not in existing_tables:
    create_table_query = f"CREATE TABLE {table_name} ("
    for col in columns:
        create_table_query += f"{col} VARCHAR(255), "
    create_table_query = create_table_query[:-2]  # Remove the last comma and space
    create_table_query += ")"
    cursor.execute(create_table_query)

# Insert the data into the SQL Server table
insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
cursor.fast_executemany = True  # Enable fast executemany mode
cursor.executemany(insert_query, records)
conn.commit()

print("Data inserted into SQL Server table successfully")
