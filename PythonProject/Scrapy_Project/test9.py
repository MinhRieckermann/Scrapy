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
from time import sleep
from bs4 import BeautifulSoup

chrome_options=Options()
#chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
brower=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)

brower.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
username='minhtranvu1992@gmail.com'
password='Linkedin-Linh.hoang@54'


elementID=brower.find_element_by_id('username')
elementID.send_keys(username)


elementID=brower.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()

sleep(4)

search=brower.find_element_by_xpath('//input[contains(@class,"search")]')
search.send_keys('accountant people Ho Chi Minh')
search.send_keys(Keys.ENTER)

#search_result=brower.find_element_by_xpath('//div[contains(@class,"search-results__cluster-bottom-banner")]/a')


search_result=WebDriverWait(brower, 4000).until(
                        EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"search-results__cluster-bottom-banner")]/a'))
                        )
search_result.click()
sleep(5)
# Task 3: Scrape the URLs of the profiles
# Task 3.1: Write a function to extract the URLs of one page
def GetURL():
    body=(brower.page_source).encode('utf-8')

    resp=Selector(text=body)

    profile_URL=WebDriverWait(brower, 400).until(
                        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="entity-result__item"]/div[2]/div/div/div/span/span/a[@class="app-aware-link"]'))
                        )
    
    
    #resp.xpath("//div[@class='entity-result__item']/div[1]/div/a[@class='app-aware-link']/@href").getall()
    all_profiles_URL=[]
    # Name=WebDriverWait(brower, 400).until(
    #                     EC.presence_of_all_elements_located((By.XPATH,'//div[@class="entity-result__item"]/div[2]/div/div/div/span/span/a/span/span[1]'))
    #                     )

    for profile in profile_URL:
        if "LinkedIn Member" not in profile.text:

            if profile.get_attribute('href') not in all_profiles_URL:
                all_profiles_URL.append(profile.get_attribute('href'))
    
    return all_profiles_URL


# get_url=WebDriverWait(brower, 1000).until(
#                        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="entity-result__item"]/div[1]/div/a[@class="app-aware-link"]' ))
#                        )

# for i in range(len(get_url)):
#     get_url=WebDriverWait(brower, 1000).until(
#                        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="entity-result__item"]/div[1]/div/a[@class="app-aware-link"]' ))
#                        )
#     detail={
#             'url':get_url[i].get_attribute('href')
#             }
#     profiles.append(detail)

#print(GetURL())
#Task 3.2: Navigate through many page, and extract the profile URLs of each page
def GetURLsonPages():

    input_page = int(input('How many pages you want to scrape: '))
    URLs_all_page = []
    for page in range(input_page):
        URLs_one_page = GetURL()
        sleep(2)


        brower.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        next_url=WebDriverWait(brower, 400).until(
                        EC.presence_of_element_located((By.XPATH,'//button[@aria-label="Next"]' ))
                        )
        next_url.click()
        URLs_all_page = URLs_all_page + URLs_one_page
        sleep(2)
    return URLs_all_page

# #print(GetURLsonPages())
URLs_all_page=GetURLsonPages()
# Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file

with open('output.csv', 'w',  newline = '', encoding='utf-8') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        brower.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(5)

        body=(brower.page_source)
        resp=Selector(text=body)



        Name=WebDriverWait(brower, 100).until(
                        EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pv-text-details__left-panel")]/div/h1' ))
                        )
        title=WebDriverWait(brower, 100).until(
                        EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pv-text-details__left-panel")]/div[@class="text-body-medium break-words"]' ))
                        )
        location=WebDriverWait(brower, 100).until(
                        EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pb2 pv-text-details__left-panel")]/span[1]' ))
                        )                        
        # Name=resp.xpath("//div[contains(@class,'pv-text-details__left-panel')]/div/h1/text()").get()
        # title=resp.xpath("//div[contains(@class,'pv-text-details__left-panel')]/div[@class='text-body-medium break-words']/text()[2]").get()
        # location=resp.xpath("//div[contains(@class,'pb2 pv-text-details__left-panel')]/span[1]/text()[2]").get()
        print(Name.text)
        print(title.text)
        print(location.text)
        writer.writerow({headers[0]:Name.text, headers[1]:title.text, headers[2]:location.text, headers[3]:linkedin_URL})
