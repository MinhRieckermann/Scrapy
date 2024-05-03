from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from shutil import which
import csv
from scrapy.selector import Selector
import scrapy
import urllib.parse
import urllib.request
import requests
import json

#---------------------------------------------------------------------------------------------
def h2hevent(url,headers,tournament):
    req = requests.get(url,headers=headers)
    raw_data=json.loads(req.content)
        
    tournament=tournament
    
    country=''
    roundInfo=''
    Hometeam=''
    Awayteam=''
    match_id=''
    tournamentapi=''

    for i in range(len(raw_data['events'])):
        if raw_data['events'][i]['status']['type']=="finished" and raw_data['events'][i]['tournament']['name']==tournament:
            # tournament=raw_data['events'][i]['tournament']['name']
            # country=raw_data['events'][i]['tournament']['category']['name']
            # roundInfo=raw_data['events'][i]['roundInfo']['round']
            # Hometeam=raw_data['events'][i]['homeTeam']['name']
            # Awayteam=raw_data['events'][i]['awayTeam']['name']
            match_id=raw_data['events'][i]['id']
            tournamentapi=raw_data['events'][i]['tournament']['name']
            break

    TimeAwayScrore=''
    TimeHomeScrore=''
    FTResult=''
    HTResult=''
    DetailScore=''

    api_detail_url='https://api.sofascore.com/api/v1/event/{0}/incidents'#https://web.archive.org/web/20211023110834/
    detail_url=api_detail_url.format(match_id)
    
    res=incidentevent(detail_url,headers)    
    if res !='':

        data_result={
            'FTResult':res.get("FTResult"),
            'HTResult':res.get("HTResult"),
            'TimeAwayScrore':res.get("TimeAwayScrore"),
            'TimeHomeScrore':res.get("TimeHomeScrore"),
            'DetailScore':res.get("DetailScore"),
            'match_id':match_id,
            'tournament_nameapi':tournamentapi,
            'api_detail_url':detail_url,
            'homescore':res.get("HomeScore"),
            'awayscore':res.get("AwayScore")
        }
    else:
        data_result={
            'FTResult':'link error',
            'HTResult':'link error',
            'TimeAwayScrore':'link error',
            'TimeHomeScrore':'link error',
            'DetailScore':'link error',
            'match_id':match_id,
            'tournament_nameapi':tournamentapi,
            'api_detail_url':detail_url,
            'homescore':'link error',
            'awayscore':'link error'
        }


    return data_result
    
def incidentevent(url,headers):
    # req = urllib.request.Request(url,headers=headers)
    # data=urllib.request.urlopen(req).read().decode('utf-8')
    data=send_request(url,headers)
    if data !=None:
        raw_data=json.loads(data)
    else:
        raw_data=''
     
    TimeAwayScrore=''
    TimeHomeScrore=''
    FTResult=''
    HTResult=''
    homescore=''
    awayscore=''
    if raw_data!='':
        if "incidents" in raw_data:

            for dt in raw_data['incidents']:
                if dt['incidentType']=="period":
                    if dt['text']=="FT":
                            FTResult=str(dt['homeScore'])+"-"+str(dt['awayScore'])
                            homescore=int(dt['homeScore'])
                            awayscore=int(dt['awayScore'])
                    if dt['text']=="HT":
                            HTResult=str(dt['homeScore'])+"-"+str(dt['awayScore'])
                if dt['incidentType']=="goal":
                    if dt['isHome']==False:
                            TimeAwayScrore=TimeAwayScrore+str(dt['time'])+";"
                    if dt['isHome']==True:
                            TimeHomeScrore=TimeHomeScrore+str(dt['time'])+";"
                            # item['HTResult']=
                            # item['HomeScores']=
                            # item['AwayScores']=
                            # item['TimeAwayScrore']=
                            # item['TimeHomeScrore']=
                            # item['DetailScore']=
                            # item['Hometeam']=
                            # item['Awayteam']=
                            # item['country']=
                            # item['tournament']=
                            # item['season']=
            data_result={
                'FTResult':FTResult,
                'HTResult':HTResult,
                'TimeAwayScrore':TimeAwayScrore,
                'TimeHomeScrore':TimeHomeScrore,
                'DetailScore':TimeHomeScrore+"-"+TimeAwayScrore,
                'HomeScore':homescore,
                'AwayScore':awayscore
            }    
            
        

            return data_result
        else:
            return ''
        
    else:
         data_result={
                'FTResult':'no found',
                'HTResult':'no found',
                'TimeAwayScrore':'no found',
                'TimeHomeScrore':'no found',
                'DetailScore':'no found',
                'HomeScore':'no found',
                'AwayScore':'no found'
            }
    return data_result

def send_request(url, headers=None):
    try:
        # Prepare the request with optional headers
        req = urllib.request.Request(url, headers=headers)
        
        # Open the URL
        with urllib.request.urlopen(req) as response:
            # Read the response data
            data = response.read()
            # If data is None, set it to an empty byte string
            if data is None:
                data = b''
            # Decode the response data assuming it's UTF-8
            decoded_data = data.decode('utf-8')
            # Print the decoded response
            print(decoded_data)
    except urllib.error.URLError as e:
        print("Error:", e)       



#----------------------------------------------------------------------------------------------
chrome_options=Options()
#chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
api_event_url='https://api.sofascore.com/api/v1/event/683397/incidents'
rep=incidentevent(api_event_url,headers)
if rep !='':

        data_result={
            'FTResult':rep.get("FTResult"),
            'HTResult':rep.get("HTResult"),
            'TimeAwayScrore':rep.get("TimeAwayScrore"),
            'TimeHomeScrore':rep.get("TimeHomeScrore"),
            'DetailScore':rep.get("DetailScore"),
            #'match_id':match_id,
            # 'tournament_nameapi':tournamentapi,
            # 'api_detail_url':detail_url
        }
else:
        data_result={
            'FTResult':'link error',
            'HTResult':'link error',
            'TimeAwayScrore':'link error',
            'TimeHomeScrore':'link error',
            'DetailScore':'link error',
            # 'match_id':match_id,
            # 'tournament_nameapi':tournamentapi,
            # 'api_detail_url':detail_url
        }

print(data_result)

