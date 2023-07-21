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

base_url = "https://api.businesscentral.dynamics.com/v2.0/e3c37df3-5a5e-400f-bf9e-505bf9526fed/JRDEV/api/v2.0/"
#api_endpoint = "companies"
Refresh_Token = "0.AVYA833D415aD0C_nlBb-VJv7Sf4Ffq_9XtKtPeoITlbqkdWAGg.AgABAAEAAAD--DLA3VO7QrddgJg7WevrAgDs_wUA9P8Z-rdVvJDafX2bmP4VWi2G2AMnCxbqycOqwVpJmFcwtsoMS7GbhN5CIo8sQaeYCbi-iOh5shJ2GLV-X-zOWLQIW2nxe707TsRb_9KvkZuvYZdVOJFHKfi_wer8W4wqPs0zR4ASGDiAm5afDo1wXaf-LGm1pRrOY_Rm03Ppzl_hCO8uuA8f7a1gEqxo1vMehVk3CXuylHs0y6zLs-du3QjDHhUtDhVL9UnZTIJFpaJCKPEzEfL2Gs2fzr4t3C96J3lSMJ4VrZbvYFEorj_A5aYrqRPmfj_hIAeavO1Nar66YV_lGXqkOU5kRbcP-bkJxkzaSBYJUJO8jT5BUpYEnR3uJnP1hG4grqgY4U-B7q6LyOCo5GDRs7aRpq8HCP-HPrNfxsymQDjiXM_zJsGcUqGs5juzYqqAJdxFu8Zlotpzbze8CKXn5-EUFGs7rsEoZiUxcqOcF-UhFstdbf_Za58swIIvcA-2wQeDf1rDWUsWMtjeLFSCO74JuBcKUYYniVne64If4d5fUlHsd5_5X-wy4KWwfOHQax8omF0MtaU1jYolnBXmjOmHHjMnMMlY5a6e8YmyfXncVW6dkK7eGHYaolv_OdvtW6QPIhvzKN5IzNtlg_HKxVADaWPmbf1Ijcy3RrHh9OciopZ6gL0oT935Osn8oRWE6H1CLt9OgdAGa_I0VYG_QWid9MHb5g0Da6wx7aNq4noG29Dt0LsO4Lds89WXNnlvUW0ths1doV7QI09a4Uqw3UQn031KGVPq-L9XGMz2g6w3EImbAlJCBgCApJqzyaAhXRv4S1mTLg"
client_id="fa15f827-f5bf-4a7b-b4f7-a821395baa47"
client_secret="JQy8Q~9gnSxrg6g3xMNjHaZhQF-xF9Gnvy_YrcK8"

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