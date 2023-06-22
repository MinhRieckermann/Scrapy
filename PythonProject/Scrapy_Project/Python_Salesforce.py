from simple_salesforce import Salesforce
import pandas as pd
import logging

import pyodbc
import pymssql
from sqlalchemy import create_engine
# Salesforce API credentials
username = 'tuan.na@rieckermann.com.jrdev'
password = 'Nat@2021jr'
security_token = 'oQZgAhoa6VPUvS95XkcMLqDAE'

# Create the Salesforce client
sf = Salesforce(username=username, password=password, security_token=security_token,
                domain='test')  # Use 'login' for production environment

# Perform a dynamic SOQL query to select all fields from the Account table
describe_fields = sf.Account.describe()['fields']
field_names = [field['name'] for field in describe_fields]
query = f"SELECT {', '.join(field_names)} FROM Account"
result = sf.query_all(query)

# Extract the records from the query result
records = result['records']

# Convert the records to a DataFrame
df = pd.DataFrame(records)

# Print the DataFrame
print(df.describe(exclude=['O']))
#print out all columnn with dtype is object
print(list(df.select_dtypes(['object']).columns))
# print out all columns in data frame 
print(df.columns) 

#print(str(df))

#print(df.info)


print(df.dtypes)

# Create a new DataFrame excluding 'BillingAddress' column
df_WithoutBillingAddress = df.drop(['BillingAddress','attributes'], axis=1)

# Replace None values with "NULL"
df_WithoutBillingAddress = df_WithoutBillingAddress.fillna("NULL")

df_WithoutBillingAddress['IsDeleted']=df_WithoutBillingAddress['IsDeleted'].map({True: 1, False: 0})

#df_WithoutBillingAddress['Name'] = df_WithoutBillingAddress['Name'].str.encode('utf-8')

df_WithoutBillingAddress.to_excel('output_salesforce.xlsx', index=False)
# SQL Server connection details
server = 'localhost'
database = 'Salesforce_DB'
username = 'sa'
password = '1234'
table_name = 'Account'
# Create a connection to SQL Server using pymssql
conn = pymssql.connect(server=server, database=database, user=username, password=password,charset='utf8')

try:
    print("Successfully connected to SQL Server")

    # Check if table exists
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    table_exists = cursor.fetchone()[0] == 1

    # If table does not exist, create it
    if not table_exists:
        # Extract column names and data types from the DataFrame
        columns = []
        for column, dtype in zip(df_WithoutBillingAddress.columns, df.dtypes):
            sql_data_type = "NVARCHAR(4000)"  # Default data type
            if 'int' in str(dtype):
                sql_data_type = "INT"
            elif 'float' in str(dtype):
                sql_data_type = "FLOAT"
            elif 'datetime' in str(dtype):
                sql_data_type = "DATETIME"
            elif 'bool' in str(dtype):
                sql_data_type = "NVARCHAR(10)"
            columns.append(f"{column} {sql_data_type}")

        # Create the table using the dynamic create table query
        create_table_query = f"""
        CREATE TABLE {table_name} (
            {', '.join(columns)}
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully")

    # Iterate over the rows in the DataFrame and insert into the table
    for index, row in df_WithoutBillingAddress.iterrows():
        try:
        # Extract the values from the row and encode the strings to utf-8
            values = tuple(value.decode('utf-8') if isinstance(value, bytes) else value for value in row)

        # Create the SQL insert statement
            #sql_insert = f"INSERT INTO {table_name} ({', '.join(df_WithoutBillingAddress.columns)}) VALUES {str(values)}"
            #sql_insert = f"INSERT INTO {table_name} ({', '.join(df_WithoutBillingAddress.columns)}) VALUES ({', '.join(['%s'] * len(df_WithoutBillingAddress.columns))})"
            sql_insert="INSERT INTO {} ({}) VALUES ({})".format(table_name,
                ", ".join(df_WithoutBillingAddress.columns),
                ", ".join(["N'" + str(val) + "'" if isinstance(val, str) else str(val) for val in values])
            )
        # Execute the insert statement
            cursor.execute(sql_insert)

        # Commit the changes to the database
            conn.commit()
        except Exception as e:
            # Log the error message
            logging.error(f"Error occurred for record at index {index}: {str(e)}")
            # Skip the row and continue with the loop
            continue

# Close the cursor and connection
    cursor.close()
    

except pymssql.Error as e:
    print("Error connecting to SQL Server:", e)

finally:
    # Close the connection
    if conn:
        conn.close()
        print("SQL Server connection closed")