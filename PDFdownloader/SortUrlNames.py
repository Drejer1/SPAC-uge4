import os
import pandas as pd

def readxlxsAndCreatequeue(path):

    df = pd.read_excel(path)
    df = df.fillna("Empty")
    name_list = df['Report Html Address'].values.tolist()
    
    print(type(df))
    return name_list
column = readxlxsAndCreatequeue(os.path.join("Data","GRI_2017_2020.xlsx"))
column.sort()
for line in column:
    print(line)

