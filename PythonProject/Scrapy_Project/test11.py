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


chrome_options=Options()
#chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
driver=webdriver.Chrome(executable_path=chrome_path,options=chrome_options)


driver.get('https://www.sofascore.com/tournament/football/germany/bundesliga/35')
results = []
tab_selector='//div[@class="u-mV12"]/div/div[contains(@class,"sc-3db02b55-0")]/a[text()="By Round"]'

by_Round=WebDriverWait(driver, 4000).until(
                        EC.presence_of_element_located((By.XPATH,tab_selector))
                        )
print(by_Round)