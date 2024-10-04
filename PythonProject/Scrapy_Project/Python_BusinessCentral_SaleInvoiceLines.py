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
#     column_defs = ", ".join([f"{col} NVARCHAR(255)" for col in columns])
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
Refresh_Token = "0.AVYA833D415aD0C_nlBb-VJv7Sf4Ffq_9XtKtPeoITlbqkdWAEo.AgABAwEAAAApTwJmzXqdR4BN2miheQMYAgDs_wUA9P9KPxWZNmPGRZStC1gAywiHHBbU3wZSYAWtk2kaWt4PLcDWX5X4-axw-U9F4HmJL9bCA_TVaYTdqDTvBDWClLAbKxUxY8Ek8S7_R9G4S39mazq9pRlCeN1xa9qU5UpB-uAEVnAnsw7qf5y3RlMxYYas00fkAOyjaP4C1AmMbNgiTNEQjs4h58jj7-rmxo-QWfYYkPtqnvP4hTe2XYTlzWlz1Ko30roufO0q1KOEPniqWZhWxmnH7DFpnPjdPYtuBOYWYWZrCckaAesBP144nNu7HsFImfRgZXsjYn9xZMj-_9HMlbs24H6E2h55ISFTFvUMk13nNW6vUYx2JbNtDONchBrZzkVy-6HKHtbKseA4B5iSiKBNMAEYRjwUCoiZwkAOZKJuqa0w9KlsEv6gqWPwZ46CWqVkl0PomYZKJevfUuQHC5_pKGzdYnIJlzXh0KV4vJPjsQeyzgmU6SSFkY8Hqi0VO61G0i7YgbkWZ6IjiC0tu75RNgUUzwksKcnQ3uH9xVTFMhKfnHgTsL1dUjdSYRuNCwnOI_ThyvPKPyZ40PDV-j1gM5TqWl-Upi4lI5lgZoouAeF7ncogPg5uTkBQx6bSZ6IqqMsX4VR_Z5E75SFMoJVELZ4hq5tckKYySzpvOMdm-hXaQXdxRwgCcuT0s2gZDacQka3OztLdPUCJMeeQzliZ_YzStD7imnyBrjFUeeziSXzpRTMBMfmv8wl53C_Ll6c8ijat__kuWnA1jjU"
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
    api_endpoint = f"companies({company_id})/salesInvoices?$expand=salesInvoiceLines"
    #api_endpoint = f"Company('{company_name}')/JobLedgerEntries"
    response = requests.get(base_url + api_endpoint, headers=headers)
    #response = requests.get(wsurl + api_endpoint, headers=headers)
    
    if response.status_code == 200:
        raw_data=response.json()["value"]
    else:
        print(f"Failed to retrieve accounts for company '{company_id}'. Error:", response.status_code, response.text)
    
    for data in raw_data:
        raw2_data=data["salesInvoiceLines"]
        for orderline in raw2_data:
            saleorinvoicederline={
                'accountId':orderline['accountId'],
                'amountExcludingTax':orderline['accountId'],
                'amountIncludingTax':orderline['amountExcludingTax'],
                'description':orderline['description'],
                'description2':orderline['description2'],
                'discountAmount':orderline['discountAmount'],
                'discountAppliedBeforeTax':orderline['discountAppliedBeforeTax'],
                'discountPercent':orderline['discountPercent'],
                'documentId':orderline['documentId'],
                'id':orderline['id'],
                
                'itemId':orderline['itemId'],
                'itemVariantId':orderline['itemVariantId'],
                'lineObjectNumber':orderline['lineObjectNumber'],
                'lineType':orderline['lineType'],
                'locationId':orderline['locationId'],
                'netAmount':orderline['netAmount'],
                'netAmountIncludingTax':orderline['netAmountIncludingTax'],
                'netTaxAmount':orderline['netTaxAmount'],
                'quantity':orderline['quantity'],
                'sequence':orderline['sequence'],
                
                'taxCode':orderline['taxCode'],
                'taxPercent':orderline['taxPercent'],
                'totalTaxAmount':orderline['totalTaxAmount'],
                'unitOfMeasureCode':orderline['unitOfMeasureCode'],
                'unitOfMeasureId':orderline['unitOfMeasureId'],
                'unitPrice':orderline['unitPrice']
                
            }
            result.append(saleorinvoicederline)
# save accounts_data to json file
with open('accounts_data.json', 'w') as outfile:
    json.dump(accounts_data, outfile, indent=4, sort_keys=True)

# Convert data to DataFrame

df = pd.DataFrame(result)

#print dbtype
print(df.dtypes)

# Filter out @odata.etag column if it exists
if '@odata.etag' in df.columns:
    df = df.drop(columns=['@odata.etag'])
# Display the DataFrame
print(df.head())

# export excel with rewrite name 
df.to_excel('accounts_data.xlsx', index=False)


#  established a  connection to SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=BusinessCentral_DB;UID=sa;PWD=1234')

cursor = conn.cursor()

# table_name = "accounts"
# table_name = "Job_List"
#table_name = "Job_Planning_Lines"
table_name = "salesInvoiceLines"
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
