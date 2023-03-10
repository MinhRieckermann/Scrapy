import csv, os, time
import csv
import pandas as pd
import numpy as np

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
foldername='D:\\PythonLearning\\Scrapy\\PythonProject\\Scrapy_Project\\2_data'
filenames = find_csv_filenames(foldername)
for name in filenames:
  df =pd.read_csv(foldername+"\\"+name,delimiter='\t',dtype={'Revision Budgeting':object})
  df=df[df['Industry'] !="CBLW"]
  df.to_csv(foldername+"\\"+name,index=False,sep='\t')

# df =pd.read_csv(foldername+"\\"+"Forecast Service Price v1.csv",delimiter='\t')
# #,dtype={'Revision Budgeting':object,'% Procurement Type':object}

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df.head(5))
# df=df[df['Industry'] !="CBLW"]

#df.to_csv(foldername+"\\"+"% Procurement Type v1.csv",index=False,sep='\t')

#df.info()

#print(df.to_string())


# print(df.count())

# df.to_csv(foldername+"\\"+"CB OI Db2 target lock v1.csv")
# csv_files = list(filter(lambda f: f.endswith('.csv'), os.listdir(foldername)))

# print(csv_files)