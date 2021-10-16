import requests
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

url = "https://fr.soccerway.com/teams/france/olympique-de-marseille/890/"

req = requests.get(url,headers=headers)

wiki_table = pd.read_html(req.text, attrs = {"class":"matches"} )

df = wiki_table[0].to_csv('score.csv', index = False)