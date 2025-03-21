import os
import pandas as pd

#This file was created strictly just to look at URLs and see if any of them were missing "http//", and is not used for the main program. Feel free to ignore this file. 

def readxlxsAndCreatequeue(path):

    df = pd.read_excel(path)
    df = df.fillna("Empty")
    name_list = df['Pdf_URL'].values.tolist()
    #name_list = df['Report Html Address'].values.tolist()
    
    print(type(df))
    return name_list
column = readxlxsAndCreatequeue(os.path.join("Data","GRI_2017_2020.xlsx"))
column.sort()
for line in column:
    print(line)

