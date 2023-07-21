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
    tournamentapi=''

    for i in range(len(raw_data['events'])):
        if raw_data['events'][i]['status']['type']=="finished" and raw_data['events'][i]['tournament']['name'].startswith('Liga Profesional'):
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
            'tournament_nameapi':tournamentapi,
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


driver.get('https://www.sofascore.com/tournament/football/argentina/liga-profesional-de-futbol/155#47647')
results = []
#tab_selector='//div[@class="u-mV12"]/div/div[contains(@class,"Tabs__Header")]/a[text()="By Round"]'
#tab_selector='//div[@class="u-mV12"]/div/div[contains(@class,"sc-5d19fd97-0")]/a[text()="By Round"]'
tab_selector='//div[contains(@class,"sc-hLBbgP Hbif")]/div[text()="By Round"]'
by_Round=WebDriverWait(driver, 4000).until(
                        EC.presence_of_element_located((By.XPATH,tab_selector))
                        )
by_Round.click()

by_Round=WebDriverWait(driver, 4000).until(
                        EC.presence_of_element_located((By.XPATH,tab_selector))
                        )
print(by_Round.text)
#country=driver.find_element_by_xpath('//div[contains(@class,"list-wrapper")]/div[contains(@class,"styles__EventListHeader")]/div[2]/div' )


# data_url=WebDriverWait(driver, 1000).until(
#                        EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a' ))
#                        )
data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a' ))
                       )


# hometeam=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[1]'))
#                                     )
# awayteam=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[2]'))
#                                     )
# time_match=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[1]'))
#                                     )
# status_match=WebDriverWait(driver, 100).until(
#                                     EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[2]'))
#                                     )  
hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[1]'))
                                    )
awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[2]'))
                                    )
time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/span'))
                                    )
status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/div/span[1]/span'))
                                    )                                    
driver.implicitly_wait(60)
body=(driver.page_source).encode('utf-8')

resp=Selector(text=body)


#country=resp.xpath("//span[contains(@class,'sc-6458077b-9')]/text()[2]").get()
country=resp.xpath("//div[contains(@class,'sc-hLBbgP hZKURa')]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div//span/text()[2]").get()
tournament=resp.xpath("//div[contains(@class,'sc-hLBbgP hZKURa')]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/h2/text()").get()

#year=resp.xpath("//button[contains(@class,'sc-40903c5f-4')]/span/text()").get()
year=resp.xpath("//div[contains(@class,'sc-hLBbgP hZKURa')]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[contains(@class,'sc-fnGiBr kdHYZX')]/button/div/span/text()").get()

#round_match=resp.xpath("//div[contains(@class,'list-wrapper')]/div[contains(@class,'sc-cd4cfbdc-0')]/div[2]/div/div/button/span/text()").get()
round_match=resp.xpath("//div[contains(@class,'list-wrapper')]/div[1]/div/button/div/span/text()").get()
for i in range(len(data_url)):
    
    # data_url=WebDriverWait(driver, 1000).until(
    #                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a' ))
    #                    )
    data_url=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a' ))
                       )
    
    # hometeam=WebDriverWait(driver, 100).until(
    #                                 EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[1]'))
    #                                 )
    hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[1]'))
                                    )
    
    # awayteam=WebDriverWait(driver, 100).until(
    #                                 EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[2]'))
    #                                 )
    awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[2]'))
                                    )
    
    # time_match=WebDriverWait(driver, 100).until(
    #                                 EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[1]'))
    #                                 )
    time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/span'))
                                    )
    # status_match=WebDriverWait(driver, 100).until(
    #                                 EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[2]'))
    #                                 )
    status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/div/span[1]/span'))
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

# next_url=WebDriverWait(driver, 400).until(
#                        EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-cd4cfbdc-0")]/div[1]/div' ))
#                        )
next_url=WebDriverWait(driver, 400).until(
                       EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[1]/div[contains(@class,"bKiotZ")]/button/span' ))
                       )
print (next_url.text)




# data=WebDriverWait(driver, 100).until(
#                        EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a' ))
#                        )
data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a' ))
                       )
while next_url:
    try:
        next_url.click()


        # data=WebDriverWait(driver, 100).until(
        #                EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a' ))
        #                )
        data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a' ))
                       )

        # hometeam=WebDriverWait(driver, 100).until(
        #                             EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[1]'))
        #                             )
        hometeam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[1]'))
                                    )

        # awayteam=WebDriverWait(driver, 100).until(
        #                             EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div[contains(@class,"sc-cd4cfbdc-0")]/div[3]/div[2]'))
        #                             )
        awayteam=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[4]/div[contains(@class,"fRddxb")]/div[contains(@title,"live score")]/div[2]'))
                                    )

        # time_match=WebDriverWait(driver, 100).until(
        #                             EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[1]'))
        #                             )
        time_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/span'))
                                    )
        # status_match=WebDriverWait(driver, 100).until(
        #                             EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a/div/div/div[contains(@class,"sc-d47f388d-2")]/div[2]'))
        #                             )
        status_match=WebDriverWait(driver, 100).until(
                                    EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a/div/div[contains(@class,"js-list-cell-target")]/div[2]/div/span[1]/span'))
                                    )

        # round_match=WebDriverWait(driver, 10).until(
        #                             EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-cd4cfbdc-0")]/div[2]/div/div/button/span'))
        #                             )
        round_match=WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[1]/div/button/div/span'))
                                    )
        
        for i in range(len(data)):
            
            # data=WebDriverWait(driver, 100).until(
            #            EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"sc-8e930919-2")]/a' ))
            #            )
            data=WebDriverWait(driver, 1000).until(
                       EC.presence_of_all_elements_located((By.XPATH,'//div[contains(@class,"list-wrapper")]/div[contains(@class,"hBOvkB")]/a' ))
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

print(results)

with open('football_Agrentina_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f,
                            fieldnames=['country', 'tournament', 'year', 'hometeam', 'awayteam', 'time_match','status_match', 'round_match', 'detail_url','code','api_event_url',
                                        'FTResult','HTResult','TimeAwayScrore','TimeHomeScrore','DetailScore','match_id','tournament_nameapi','api_detail_url'])
    writer.writeheader()
    writer.writerows(results)