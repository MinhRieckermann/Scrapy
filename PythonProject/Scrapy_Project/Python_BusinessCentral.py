import requests
import pandas as pd

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

base_url = ""
#api_endpoint = "companies"
Refresh_Token = ""
client_id=""
client_secret=""

access_token=GetAccessToken(client_id,client_secret,Refresh_Token)
headers = {
    "Authorization": "Bearer " + access_token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}
#response = requests.get(base_url + api_endpoint, headers=headers)
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

for company in companies:
    company_id = company["id"]
    api_endpoint = f"companies({company_id})/accounts"
    
    response = requests.get(base_url + api_endpoint, headers=headers)
    
    if response.status_code == 200:
        accounts_data.extend(response.json()["value"])
    else:
        print(f"Failed to retrieve accounts for company '{company_id}'. Error:", response.status_code, response.text)
# Convert data to DataFrame
df = pd.DataFrame(accounts_data)

# Display the DataFrame
print(df.head())
