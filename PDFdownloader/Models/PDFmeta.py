from logging import _nameToLevel
from math import nan
from nturl2path import url2pathname

from pandas.tseries.offsets import Second

#Class containing the metadata of the PDFs retrived from the xlsx file. 
#First and second URL (if they exist)
#BRnumber(name) and a value telling if the download was success. 
#The Pandas library will assign empty values as "Not a number" Float type which is the reason for the checks. 
class PDFmeta():
    def __init__(self,_name, firstU:str,secondU:str):
        self.name = _name.replace("/","-")
        self.firstUrl = firstU
        if not type(self.firstUrl) == float:
            if not "http" in self.firstUrl:
                self.firstUrl = "https//" + self.firstUrl
        self.secondUrl = secondU
        if not type(self.secondUrl) == float:
            if not "http" in self.secondUrl:
                self.secondUrl = "https//" + self.secondUrl
        self.downloadSuccess = False

         

