import requests
import pandas as pd
import pyodbc
import json

def GetAccessToken(client_id, client_secret, refresh_token):
    access_token_url = "https://login.microsoftonline.com/e3c37df3-5a5e-400f-bf9e-505bf9526fed/oauth2/v2.0/token"
    
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    
    response = requests.post(access_token_url, data=data)
    response_data = response.json()
    
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        print("Failed to get access token. Error:", response_data.get("error_description", "Unknown error"))
        return None
 ##########################################################################################################
 # 
 # 
 # 
 # 
 # 
 # 
 # 
 #    

def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = ?
    """, (table_name,))
    return cursor.fetchone()[0] == 1

# def create_table_from_df(cursor, df, table_name):
#     columns = df.columns
#     column_defs = ", ".join([f"{col} NVARCHAR(MAX)" for col in columns])
#     create_table_sql = f"CREATE TABLE {table_name} ({column_defs})"
#     cursor.execute(create_table_sql)
def create_table_from_df(cursor, df, table_name):
    dtype_mapping = {
        'object': 'NVARCHAR(255)',
        'float64': 'MONEY',
        'int64': 'INT',
        'bool': 'BIT',
        'datetime64[ns]': 'DATETIME'
    }
    
    column_defs = ", ".join([f"{col} {dtype_mapping.get(str(dtype), 'NVARCHAR(255)')}" for col, dtype in df.dtypes.items()])
    create_table_sql = f"CREATE TABLE {table_name} ({column_defs})"
    cursor.execute(create_table_sql)
def drop_table_if_exists(cursor, table_name):
    cursor.execute(f"""
        IF OBJECT_ID('{table_name}', 'U') IS NOT NULL
        DROP TABLE {table_name}
    """)
def insert_data_from_df(cursor, df, table_name):
    columns = df.columns
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
    for index, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))
base_url = "https://api.businesscentral.dynamics.com/v2.0/e3c37df3-5a5e-400f-bf9e-505bf9526fed/JRTEST/api/v2.0/"

wsurl='https://api.businesscentral.dynamics.com/v2.0/e3c37df3-5a5e-400f-bf9e-505bf9526fed/JRTEST/ODataV4/'
#api_endpoint = "companies"
Refresh_Token = "0.AVYA833D415aD0C_nlBb-VJv7Sf4Ffq_9XtKtPeoITlbqkdWAEo.AgABAwEAAAApTwJmzXqdR4BN2miheQMYAgDs_wUA9P8HXHcxRCb7rheTGObLWTKoCiePd1SDG12n5MWpWZ0LxjJP9gfC3G6nAstLLnkEWrIV53kwQRK90-ZVqd1TQYH5fEP2ADUBiyW3GbDltUBY-dTR03ZfUsCWj8RbPzzip1l5HasRVZxvu542_99t7B_rn3MNIjUiUXNnCxvPeTVExIEzk_ROP6N8ZYWOP5vR5g7ulgf0urxxvdMYFSMNTuslAT7DE9dBXrQnES40hlGUyPCsFSOVQ7W1bkNzbPoggDHjFUUzKZIjA_dwPwzKwAgYPj5Fyd0l2BqQufSjR_yAIVwuLrLe9M8XFHsa48QZUAUfSWHY0WarYr4jrhcqu3HYYl24cYlBWqGJ1T2P1RP0uZYa5RnwU7sLBSA_pswcnj5u8GJb1K630BaHigdol02vOUCSAknBAS42Jejy19FLUi7FYCxm3bNe1xCUnGtDogceY4XCdhHeBxDcv5c3T171F-MrLpy-I3Zd2m6hqy8xepsXEr9seNNoqswgBQZL8xIwEO6LS6cpVRV-QTWv-A-btvC5D2bTdkKXIl7BDna9Nd3PQEDmlVHVH9S5PHujW8TwwadAA9aZhk0hXZQrg8rxUVDEohqOTfGNYT3ofWZBZW9OZvK4eAPNRJTi2ozIfC3R96Cl8akill3iHQg5INOVPY3zbIs59aFCnNZSz2eMZ7f15iLQmRW7eHqU0Vlyj9Xx-WN4inTipWSk-j76ncP0usebnkpxH6HEYkRZ8Bc"
client_id="fa15f827-f5bf-4a7b-b4f7-a821395baa47"
client_secret="vVV8Q~HQXp4xWFASgIUgHGkZ6cYuY9s05Qx7QbaB"

access_token=GetAccessToken(client_id,client_secret,Refresh_Token)
headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Make a test request to check the connection status
response = requests.get(base_url + "companies", headers=headers)
# Process the response
# Check the status
if response.status_code == 200:
    print("Connection successful!")
else:
    print("Connection failed. Error:", response.status_code, response.text)

# Retrieve all companies
response_companies = requests.get(base_url + "companies", headers=headers)
companies = response_companies.json()["value"]

# Loop through each company and retrieve accounts table
accounts_data = []

result=[]

for company in companies:
    company_id = company["id"]
    company_name=company["name"]
    #api_endpoint = f"companies({company_id})/salesInvoices?$expand=salesInvoiceLines"
    api_endpoint = f"Company('{company_name}')/DWH_ProjectPlanningLines"
    #response = requests.get(base_url + api_endpoint, headers=headers)
    response = requests.get(wsurl + api_endpoint, headers=headers)
    
    if response.status_code == 200:
        accounts_data.extend(response.json()["value"])
    else:
        print(f"Failed to retrieve accounts for company '{company_id}'. Error:", response.status_code, response.text)
        
# save accounts_data to json file
with open('accounts_data.json', 'w') as outfile:
    json.dump(accounts_data, outfile, indent=4, sort_keys=True)

# Convert data to DataFrame

df = pd.DataFrame(accounts_data)

# Filter out @odata.etag column if it exists
if '@odata.etag' in df.columns:
    df = df.drop(columns=['@odata.etag'])
# Display the DataFrame
print(df.head())


#  established a  connection to SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=XDESRVUAT001\MSSQLSERVERDEV;DATABASE=BusinessCentral_DB;UID=MetadataAccount;PWD=XDESRVUAT001')

cursor = conn.cursor()

# table_name = "accounts"
# table_name = "Job_List"
#table_name = "Job_Planning_Lines"
table_name = "DWH_ProjectPlanningLines"
if not table_exists(cursor, table_name):
    create_table_from_df(cursor, df, table_name)
    conn.commit()
else:
    print(f"Table '{table_name}' already exists. process re-creation...")
    drop_table_if_exists(cursor, table_name)
    create_table_from_df(cursor, df, table_name)
    conn.commit()

insert_data_from_df(cursor, df, table_name)
conn.commit()

cursor.close()
conn.close()
print("Data inserted successfully.")
