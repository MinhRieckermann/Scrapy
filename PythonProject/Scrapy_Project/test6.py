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

    for i in range(len(raw_data['events'])):
        if raw_data['events'][i]['status']['type']=="finished" and raw_data['events'][i]['tournament']['name'].startswith(tournament):
            # tournament=raw_data['events'][i]['tournament']['name']
            # country=raw_data['events'][i]['tournament']['category']['name']
            # roundInfo=raw_data['events'][i]['roundInfo']['round']
            # Hometeam=raw_data['events'][i]['homeTeam']['name']
            # Awayteam=raw_data['events'][i]['awayTeam']['name']
            match_id=raw_data['events'][i]['id']
            break

    TimeAwayScrore=''
    TimeHomeScrore=''
    FTResult=''
    HTResult=''
    DetailScore=''

    api_detail_url='https://www.sofascore.com/api/v1/event/{0}/incidents'#https://web.archive.org/web/20211023110834/
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
            'api_detail_url':detail_url
        }
    else:
        data_result={
            'FTResult':'link error',
            'HTResult':'link error',
            'TimeAwayScrore':'link error',
            'TimeHomeScrore':'link error',
            'DetailScore':'link error',
            'match_id':match_id,
            'api_detail_url':detail_url
        }


    return data_result
    
def incidentevent(url,headers):
    req = requests.get(url,headers=headers)
    raw_data=json.loads(req.content)
        
    TimeAwayScrore=''
    TimeHomeScrore=''
    FTResult=''
    HTResult=''
    if "incidents" in raw_data:

        for dt in raw_data['incidents']:
            if dt['incidentType']=="period":
                if dt['text']=="FT":
                        FTResult=str(dt['homeScore'])+"-"+str(dt['awayScore'])
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
            'DetailScore':TimeHomeScrore+"-"+TimeAwayScrore
        }    
        
    

        return data_result
    else:
        return ''
        

        



#----------------------------------------------------------------------------------------------
chrome_options=Options()
#chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)


driver.get('https://www.sofascore.com/tournament/football/england-amateur/premier-league-2/1129')
results = []


# tab_selector='//div[@class="u-mV12"]/div/div[contains(@class,"Tabs__Header")]/a[text()="By Round"]'

# by_Round=WebDriverWait(driver, 4000).until(
#                         EC.presence_of_element_located((By.XPATH,tab_selector))
#                         )
# by_Round.click()

# by_Round=WebDriverWait(driver, 4000).until(
#                         EC.presence_of_element_located((By.XPATH,tab_selector))
#                         )
# print(by_Round.text)
#country=driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div' )

data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                       )
hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
                                    )
awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
                                    )
time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
                                    )
driver.implicitly_wait(600)
body=driver.page_source

resp=Selector(text=body)

country=resp.xpath("//span[contains(@class,'styles__CategoryName')]/text()[2]").get()
tournament=resp.xpath("//h2/text()").get()
year=resp.xpath("//button[contains(@class,'styles__Selector')]/span/text()").get()
round_match=''#resp.xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'styles__EventListHeader')]/div[2]/div/div/button/span/text()").get()
# for i in range(len(data_url)):
#     data_url=WebDriverWait(driver, 1000).until(
#                        EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
#                        )
#     hometeam=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
#                                     )
#     awayteam=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
#                                     )
#     time_match=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
#                                     )
    
#     link_code=urllib.parse.urlparse(data_url[i].get_attribute('href'))
#     path=link_code[2].rpartition('/')

#     detail={
#             'country':country,
#             'tournament':tournament,
#             'year':year,
#             'hometeam':hometeam[i].text,
#             'awayteam':awayteam[i].text,
#             'time_match':time_match[i].text,
#             'round_match':round_match,
#             'detail_url':data_url[i].get_attribute('href'),
#             'code':path[2]



#         }
#     results.append(detail)
driver.implicitly_wait(400)
next_url=WebDriverWait(driver, 400).until(
                       EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[1]/div' ))
                       )
print (next_url.text)



data=WebDriverWait(driver, 100).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                       )
while next_url:
    try:
        
        

        data=WebDriverWait(driver, 100).until(
                        EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
                        )
        hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[1]'))
                                    )
        awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div[contains(@class,"EventCellstyles__EventCell")]/div[3]/div[2]'))
                                    )
        time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a/div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]'))
                                    )
        # round_match=WebDriverWait(driver, 10).until(
        #                             EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div/div/button/span'))
        #                             )
        
        for i in range(len(data)):
            data=WebDriverWait(driver, 1000).until(
                            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListContent")]/a' ))
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
                    #driver.find_element_by_xpath('//div/div/div[contains(@class,"EventCellstyles__Status")]/div[1]').text,
                    'round_match':'',
                    #driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div/div/button/span').text,
                    'detail_url':data[i].get_attribute('href'),
                    'code':path[2]


                    }
            
            results.append(detail)
        next_url=WebDriverWait(driver, 100).until(
                       EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[1]/div' ))
                       )
        next_url.click()
            
    except:
        break


driver.close()



# with open('football_data.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f,
#                             fieldnames=['country', 'tournament', 'year', 'hometeam', 'awayteam', 'time_match', 'round_match', 'detail_url','code'])
#     writer.writeheader()
#     writer.writerows(results)
#--------------------------------
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
api_event_url='https://www.sofascore.com/api/v1/event/{0}/h2h/events'
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
    event["api_detail_url"]=rep.get("api_detail_url"),

print(results)

with open('football_PremierLeague2_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f,
                            fieldnames=['country', 'tournament', 'year', 'hometeam', 'awayteam', 'time_match', 'round_match', 'detail_url','code','api_event_url',
                                        'FTResult','HTResult','TimeAwayScrore','TimeHomeScrore','DetailScore','match_id','api_detail_url'])
    writer.writeheader()
    writer.writerows(results)