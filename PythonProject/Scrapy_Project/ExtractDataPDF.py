import PyPDF2
import re
import pandas as pd
#import camelot
import camelot.io as camelot
# from Pylance import pymssql

import tabula
from tabula.io import read_pdf, convert_into, convert_into_by_batch

import pyodbc
def word_page_count(filename :str,search:str):
    #Assign File 
    #file_name="7K.pdf"
    doc=PyPDF2.PdfReader(filename)
    #number of page 
    pages=len(doc.pages)

    print(pages)
    #print(doc.getNumPages())
    #search Term
    search_term="food"
    #list of tuples (all occurences,page number)
    list_pages=[]

    for i in range (pages):
        current_page=doc.pages[i]
        text=current_page.extract_text()
        if re.findall(search_term,text):
            count_page=len(re.findall(search_term,text))
            list_pages.append((count_page,i))
    #result
    print(list_pages)

    #number of pages that contain search term at least once 
    count=len(list_pages)

    # total word count 
    total=sum([tup[0] for tup in list_pages])

    print(f"the word '{search_term}' was found {total} times on {count} pages.")

# #Read the PDF File
# file_name="7K.pdf"

# reader=PyPDF2.PdfReader(file_name)

# reader.metadata

# reader.getNumPages
# pages = ''
# for i in range(0,8):
#     pages += reader.pages[i].extract_text()

# pages = pages.replace('\n','')
# pages

# # extract all the tables in the PDF file
# tables = camelot.read_pdf(file_name)
# # number of tables extracted
# print("Total tables extracted:", tables.n)
# # print the first table as Pandas DataFrame
# print(tables[0].df)

# # convert table[0].df to a pandas DataFrame object
# df = pd.DataFrame(tables[0].df)

# # formatting the table view
# table_view = ""

# # loop through each row of the dataframe and extract the values at each column position
# for i in range(df.shape[0]):
#     row_data = ""
#     for j in range(df.shape[1]):
#         # add a separator between columns
#         separator = " | " if j < df.shape[1] - 1 else ""
#         # extract the cell value
#         cell_value = str(df.iloc[i, j])
#         # calculate the amount of padding based on the length of the cell value
#         padding = " " * (10 - len(cell_value))
#         # concatenate the cell value, padding and separator
#         row_data += f"{cell_value}{padding}{separator}"
#     # add the formatted row data to the table view variable
#     table_view += f"{row_data}\n"

# # print the table view
# print(table_view)
# # export the table_view to excel
# with pd.ExcelWriter('output.xlsx') as writer:
#     pd.DataFrame([table_view]).to_excel(writer, sheet_name='Sheet1', index=False, header=False)





# specify the file path
file_path = "7K.pdf"

# extract all tables from the PDF file
tables = camelot.read_pdf(file_path, pages="all",flavor='stream')
tables
tables[0].df.drop([0,1,2,3],axis=0,inplace=True)
print(type(tables[0].df.drop([0,1,2,3],axis=0,inplace=True)))

# # create a Pandas Excel writer object
# writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")

# for i, table in enumerate(tables):
#     # write each table to a separate sheet in the Excel workbook
#     table.df.to_excel(writer, sheet_name=f"Table {i+1}", index=False)

# # save the Excel workbook
# writer.save()