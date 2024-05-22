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
import httpx
import urllib3
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
    data=requests.get(url,headers=headers)
    raw_data=json.loads(data.content)
    
        
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
            #print(decoded_data)
        return  decoded_data
    except urllib.error.URLError as e:
        print("Error:", e)       

        



#----------------------------------------------------------------------------------------------
chrome_options=Options()
#chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)


driver.get('https://www.sofascore.com/tournament/football/denmark/superliga/39#id:52172')
results = []

output_file='football_denmark2023_data.csv'

X_Path_hometeam='//div[contains(@class,"list-wrapper")]/div[contains(@class,"Box eUcumg")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"jLRkRA")]/div[contains(@title,"live score")]/div[1]'
X_Path_awayteam='//div[contains(@class,"list-wrapper")]/div[contains(@class,"Box eUcumg")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"jLRkRA")]/div[contains(@title,"live score")]/div[2]'

X_Path_time_match='//div[contains(@class,"list-wrapper")]/div[contains(@class,"Box eUcumg")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/bdi'
X_Path_status_match='//div[contains(@class,"list-wrapper")]/div[contains(@class,"Box eUcumg")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/div/span[1]/bdi'
X_Path_country="//div[contains(@class,'dqPXrj')]/div/div[2]/div[2]/div[1]/div[contains(@class,'jLRkRA')]/span/text()[2]"
X_Path_tournament="//div[contains(@class,'dqPXrj')]/div/div[2]/div[2]/h2/text()"
X_Path_year="//div[contains(@class,'dqPXrj')]/div/div[2]/div[2]/div[1]/div[2]/div/div/button/div/div/text()"
X_Path_round_match="//div[contains(@class,'list-wrapper')]/div[1]/div/button/div/div/text()"
X_Path_round_match_notext='//div[contains(@class,"list-wrapper")]/div[1]/div/button/div/div'
X_Path_data_url='//div[contains(@class,"list-wrapper")]/div[contains(@class,"Box eUcumg")]/a'
X_Path_next_url='//div[contains(@class,"list-wrapper")]/div[1]/button[1]'

X_Path_season_selected='//div[contains(@class,"dqPXrj")]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/ul/li[3]'
tab_selector='//div[contains(@class,"Box hIovvg")]/div[2]/div[text()="By Round"]'
X_Path_round_match_selected="//div[contains(@class,'list-wrapper')]/div[1]/div/div/div/div/ul/li[34]"
X_Path_round_match_click="//div[contains(@class,'list-wrapper')]/div[1]/div/button"



by_Round=WebDriverWait(driver, 4000).until(
                        EC.presence_of_element_located((By.XPATH,tab_selector))
                        )
by_Round.click()

by_Round=WebDriverWait(driver, 4000).until(
                        EC.presence_of_element_located((By.XPATH,tab_selector))
                        )
print(by_Round.text)
driver.implicitly_wait(5)


# #specially for Mexico league
# Action_Round_match_click=WebDriverWait(driver, 4000).until(
#                         EC.presence_of_element_located((By.XPATH,X_Path_round_match_selected))
#                         )
# Action_Round_match_click.click()
# ###
data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,X_Path_data_url ))
                       )



hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_hometeam))
                                    )
awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_awayteam))
                                    )
time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_time_match))
                                    )
status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_status_match))
                                    )                                    
driver.implicitly_wait(60)
body=(driver.page_source).encode('utf-8')

resp=Selector(text=body)



country=resp.xpath(X_Path_country).get()
tournament=resp.xpath(X_Path_tournament).get()


year=resp.xpath(X_Path_year).get()


round_match=resp.xpath(X_Path_round_match).get()
for i in range(len(data_url)):
    

    data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,X_Path_data_url))
                       )
    

    hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_hometeam))
                                    )
    

    awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_awayteam))
                                    )
    

    time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_time_match))
                                    )

    status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_status_match))
                                    )
    
    link_code=urllib.parse.urlparse(data_url[i].get_attribute('href'))
    path=link_code[2].rpartition('/')

    detail={
            'country':country,
            'tournament':tournament,
            'year':year,
            'hometeam':hometeam[i].text,
            'awayteam':awayteam[i].text,
            'time_match':time_match[i].text,
            'status_match':status_match[i].text,
            'round_match':round_match,
            'detail_url':data_url[i].get_attribute('href'),
            'code':path[2]



        }
    results.append(detail)
driver.implicitly_wait(400)


next_url=WebDriverWait(driver, 400).until(
                       EC.presence_of_element_located((By.XPATH,X_Path_next_url ))
                       )
print (next_url.text)





data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,X_Path_data_url))
                       )
while next_url:
    try:
        next_url.click()



        data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,X_Path_data_url))
                       )

        hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_hometeam))
                                    )

   
        awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_awayteam))
                                    )

        
        time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_time_match))
                                    )
        
        status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,X_Path_status_match))
                                    )

        
        round_match=WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[1]/div/button/div/div'))
                                    )
        
        for i in range(len(data)):
            
            
            data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,X_Path_data_url))
                       )
            link_code=urllib.parse.urlparse(data[i].get_attribute('href'))
            path=link_code[2].rpartition('/')
            detail={
                    'country':country,
                    'tournament':tournament,
                    'year':year,
                    'hometeam':hometeam[i].text,
                    #driver.find_element_by_xpath('//div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]').text,
                    'awayteam':awayteam[i].text,
                    #driver.find_element_by_xpath('//div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]').text,
                    'time_match':time_match[i].text,
                    'status_match':status_match[i].text,
                    #driver.find_element_by_xpath('//div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]').text,
                    'round_match':round_match.text,
                    #driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div/div/button/span').text,
                    'detail_url':data[i].get_attribute('href'),
                    'code':path[2]


                    }
            
            results.append(detail)
            
    except:
        break


driver.close()



# with open('football_data.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f,
#                             fieldnames=['country', 'tournament', 'year', 'hometeam', 'awayteam', 'time_match', 'round_match', 'detail_url','code'])
#     writer.writeheader()
#     writer.writerows(results)
#--------------------------------
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}
api_event_url='https://api.sofascore.com/api/v1/event/{0}/h2h/events'
for event in results:
    event["api_event_url"]=api_event_url.format(event.get("code"))


for event in results:
    rep=h2hevent(event.get("api_event_url"),headers,event.get("tournament"))
    event["FTResult"]=rep.get("FTResult"),
    event["HTResult"]=rep.get("HTResult"),
    event["TimeAwayScrore"]=rep.get("TimeAwayScrore"),
    event["TimeHomeScrore"]=rep.get("TimeHomeScrore"),
    event["DetailScore"]=rep.get("DetailScore"),
    event["match_id"]=rep.get("match_id"),
    event["tournament_nameapi"]=rep.get("tournament_nameapi"),
    event["api_detail_url"]=rep.get("api_detail_url"),
    event["HomeGoal"]=rep.get('homescore'),
    event["AwayGoal"]=rep.get('awayscore')

print(results)

with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f,
                            fieldnames=['country', 'tournament', 'year', 'hometeam', 'awayteam', 'time_match','status_match', 'round_match', 'detail_url','code','api_event_url',
                                        'FTResult','HTResult','TimeAwayScrore','TimeHomeScrore','DetailScore','match_id','tournament_nameapi','api_detail_url','HomeGoal','AwayGoal'])
    writer.writeheader()
    writer.writerows(results)