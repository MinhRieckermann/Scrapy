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

brower.get('https://batdongsan.com.vn/ban-can-ho-chung-cu-thu-duc/p3?sortValue=8')
username='0393345792'
password='Batdongsan-12345678x@X'


elementID=brower.find_element_by_id('username')
elementID.send_keys(username)


elementID=brower.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()


wait = WebDriverWait(brower, timeout=20000)
#------------------------------------
sleep(100000)
#--------------------------------------------------------------------

city='//div[@class="re__search-box-container"]/div[@class="re__search-box-content js__search-box-content"]/div[contains(@class,"js__search-row-location")]/div/div[contains(@class,"js_search-location-select-header-item")]/div[contains(@class,"js__city-code-select")]'
search_box_input=''
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


    
    #resp.xpath("//div[@class='entity-result__item']/div[1]/div/a[@class='app-aware-link']/@href").getall()
    all_profiles_URL=[]
 





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

# with open('output.csv', 'w',  newline = '', encoding='utf-8') as file_output:
#     headers = ['Name', 'Job Title', 'Location', 'URL']
#     writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
#     writer.writeheader()
#     for linkedin_URL in URLs_all_page:
#         brower.get(linkedin_URL)
#         print('- Accessing profile: ', linkedin_URL)
#         sleep(5)

#         body=(brower.page_source)
#         resp=Selector(text=body)



#         Name=WebDriverWait(brower, 100).until(
#                         EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pv-text-details__left-panel")]/div/h1' ))
#                         )
#         title=WebDriverWait(brower, 100).until(
#                         EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pv-text-details__left-panel")]/div[@class="text-body-medium break-words"]' ))
#                         )
#         location=WebDriverWait(brower, 100).until(
#                         EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"pb2 pv-text-details__left-panel")]/span[1]' ))
#                         )                        
#         # Name=resp.xpath("//div[contains(@class,'pv-text-details__left-panel')]/div/h1/text()").get()
#         # title=resp.xpath("//div[contains(@class,'pv-text-details__left-panel')]/div[@class='text-body-medium break-words']/text()[2]").get()
#         # location=resp.xpath("//div[contains(@class,'pb2 pv-text-details__left-panel')]/span[1]/text()[2]").get()
#         print(Name.text)
#         print(title.text)
#         print(location.text)
#         writer.writerow({headers[0]:Name.text, headers[1]:title.text, headers[2]:location.text, headers[3]:linkedin_URL})
