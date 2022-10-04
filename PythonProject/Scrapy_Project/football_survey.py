import os 
import numpy as np
import pandas as pd
import matplotlib as plt
from functools import reduce
import glob


def footballfunc(filename):
    
    
    df =pd.read_csv(filename)
    df['ChampionName']=os.path.basename(filename).split('.')[0]
    df=df[df['DetailScore'] != "('link error',)"]
    df=df[df['status_match'] == "FT"]
    re_char={"'":"",",":"","(":"",")":"",";":" ","-":" "}
    df['score']=df['DetailScore'].map(lambda a: (''.join(re_char.get(x, x) for x in str(a))) )
    df['Over70']= df['score'].apply(lambda a :any(int(item)>70 for item in str(a).split()))
    df['index']=df['round_match'].apply(lambda round: round.split()[1].replace(" ",""))
    #print(df['index'])
    df['index']=pd.to_numeric(df['index'])

    df_sorted=df.sort_values(by=['index'],ascending=False)
    df_sorted.head(5)

    match=df_sorted #[df_sorted['Over70']==True]
    matchover70byround=match.groupby(['ChampionName','round_match','index','Over70']).count()['FTResult'].unstack().fillna(0)
    return print(matchover70byround.sort_values(by='index'))


path='D://PythonLearning//Scrapy//PythonProject//Scrapy_Project//1_datasurvey'

dir_list = os.listdir(path)

 


for file in dir_list:
    footballfunc(file)