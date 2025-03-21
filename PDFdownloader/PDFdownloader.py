from re import DEBUG
import pandas as pd
import os.path
import requests
import threading
import time
import concurrent.futures
import logging
from queue import Queue
from Models.PDFmeta import PDFmeta  # type: ignore
from tqdm import tqdm

logger = logging.getLogger(__name__)
loggingLevel = logging.DEBUG
logging.basicConfig(filename='failedDownloads.log', encoding ='utf-8',level = loggingLevel)

bufferLock = threading.Lock()
tqdmLock = threading.Lock()

#This is the task that each thread runs. 
#The queue contains PDFmeta objects which stores the BRnumber and URLs of the PDFs.
#The tasks runs until the queue is empty. workedUrls is used to tell what each indevidual thread is working on.
#tqdm is used to show a progress bar of the how many elements in queue remains and what each thread is working on.
#The buffer is used to only append to txt whenever there are more than 50 element to be written. 
def task(queue:Queue,saveFolder:str,threadNumber:int,buffer:list[PDFmeta],pbar:tqdm,workedUrls:list[str]) -> None:
    while not queue.empty():
        PDFm:PDFmeta = queue.get()
        workedUrls[threadNumber] = f"Thread_{threadNumber} working on {PDFm.name}"
        with tqdmLock:
            pbar.set_postfix_str("\n"+"\n".join(workedUrls),refresh=True)
            pbar.update(1)
        PDF = downloader(PDFm,saveFolder)
        buffer.append(PDF)
        if len(buffer) > 50:
            append_to_txt(buffer)
        queue.task_done()

#buffer is popped one at a time to avoid race conditions where: Thread_1 writes buffer to txt -> Thread_2 appends to buffer -> Thread_1 clears buffer. 
def append_to_txt(buffer:list[PDFmeta]) -> None:
    with bufferLock: 
        temp =[]
        while buffer:
            temp.append(buffer.pop(0))
        with open("download_log.txt","a") as txt:
            for PDFm in temp:
                txt.writelines(f"{PDFm.name}, {PDFm.downloadSuccess}")

#The function used to make requests.
def downloadPDF(url,new_save_path) -> bool:
    try:
        response = requests.get(url,timeout=10)
        if response.headers['Content-Type'] == 'application/pdf':
           with open(new_save_path,'wb') as file:
               file.write(response.content)
               #TODO: Do some checks for PDF file size etc.
               return True
        return False
    except Exception as e:
        if loggingLevel == logging.DEBUG:
            logger.debug(f"URL {url}\n{type(e)} Error message{e}")
        else:
            logger.error(f"URL {url}\n{type(e)}")
        return False

#Function called by task. Tries the first url if unsuccesfull tries the second.
#if the download succeeds the function will return the PDFmeta after having set its downloadSuccess value to true.
def downloader(PDFm: PDFmeta,save_path:str) -> PDFmeta:
    new_save_path = os.path.join(save_path,PDFm.name+".pdf")
    bdownload = downloadPDF(PDFm.firstUrl,new_save_path)
    if bdownload:
        PDFm.downloadSuccess = True
        return PDFm
    bdownload = downloadPDF(PDFm.secondUrl,new_save_path)
    if bdownload:
        PDFm.downloadSuccess = True
        return PDFm
    return PDFm

#Reads the xlsx file and fills the queue with PDFmeta objects which defines the objects that tasks need to process.
#Also returns the size of the queue for usage in tqdm as from the documentation Queue.qsize() retreives the "aproximate size" and is not reliable.
def readxlxsAndCreatequeue(path,queue):
    df = pd.read_excel(path)
    name_column = df["BRnum"]
    AL_column = df["Pdf_URL"]
    AM_column = df["Report Html Address"]
    size = 0
    for name, al , am in zip(name_column,AL_column,AM_column):
        queue.put(PDFmeta(name,al,am))
        size +=1
    print(f"{size}  Number of PDFmeta in Queue")
    return size

#Main function
def main ():
    savefolder = "downloads"
    queue = Queue()
    queueSize = readxlxsAndCreatequeue(os.path.join("Data","GRI_2017_2020.xlsx"),queue)
    PDFmCounter = 0
    result = queue.get()
    num_threads = 20
    pool = []
    buffer= []
    #workerUrls is declared with 20 values inorder to later access them by the index of the threads, so each Thread has their own assigned spot in workedUrls
    workedUrls = ["Not Started"] * num_threads
    with tqdm(total=queueSize, desc="Download PDFs") as pbar:
        for index in range(num_threads):
            worker = threading.Thread(target = task, args = (queue,savefolder,index,buffer,pbar,workedUrls))
            worker.start()
            pool.append(worker)
        for idx, worker in enumerate(pool):
            worker.join()
            workedUrls[idx] = f"Thread_{idx} Finished"
            with tqdmLock:
                pbar.set_postfix_str("\n"+"\n".join(workedUrls),refresh=True)
                pbar.update(1)
    print("Queue Empty downloads finished")
if __name__ =="__main__":
    main()