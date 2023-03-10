# from atlassian import Jira

# jira = Jira(

#     url='https://rieckermann.atlassian.net/',

#     username='minh.tv@rieckermann.com',

#     password='ATATT3xFfGF0ByXj2ylwOmEGAFQahP8rKbKMyntCQoJGvisgNbnco7u_lVVLT_giwWgGFvzJfS2Y4vT29BOKdfFPi5M9CJIhsVPr6_cb5ZABVAr9IKuiGVuEHOsVqPrmvzidBzMxoL_65qXJstdkhwAlKbFXrcXu1WX5tctCtz2ZyNUHd1X6Jf0=6E7D0F17',

#     cloud=True)

# jql_request ='project = BFP AND issuetype = Story'

# issues = jira.jql(jql_request)

# print(issues)

import requests

from requests.auth import HTTPBasicAuth

import json

import base64
url = "https://rieckermann.atlassian.net/rest/api/3/issue/BFP-2"

credentials = "Basic " + base64.b64encode("minh.tv@rieckermann.com:ATATT3xFfGF0ByXj2ylwOmEGAFQahP8rKbKMyntCQoJGvisgNbnco7u_lVVLT_giwWgGFvzJfS2Y4vT29BOKdfFPi5M9CJIhsVPr6_cb5ZABVAr9IKuiGVuEHOsVqPrmvzidBzMxoL_65qXJstdkhwAlKbFXrcXu1WX5tctCtz2ZyNUHd1X6Jf0=6E7D0F17".encode("ascii")).decode("ascii")

headers = {

   "Accept": "application/json",

   "Authorization": credentials

}
response = requests.request(

   "GET",

   url,

   headers=headers

)
print(type(response.text))

#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))