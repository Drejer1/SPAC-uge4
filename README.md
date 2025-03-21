
# Multithreaded PDF downloader

A project made as part of [Specialisternes](https://dk.specialisterne.com/) academy course during week 4.

This project is designed to scan an xlsx file for links to PDFs and afterwards it will attempt to download from multiple links at a time 





## Features


- Reads xlsx and fills a queue of tasks(download PDF) to be completed  
- Multithreaded downloads PDFs
- Also writes a txt file which tells what PDFs have been downloaded and which have not



## Installation

1. Clone the repository:
```bash
    git clone https://github.com/Drejer1/SPAC-uge4.git
    cd SPAC-uge3/PDFdownloader
```
2. Create a virtual environment and activate it:
```bash
    python -m venv venv 
    source venv/bin/activate  # On Windows 
    use `venv\Scripts\activate`
```
3. Install the required dependencies:
```bash
    pip install -r requirements.txt
```

## Executing
Simply run PDFdownloader.py 

If you want to run with a small sample of PDFs then change 
```python
    xlsx = "GRI_2017_2020.xlsx"
```
to
```python
    xlsx = "GRI_2017_2020_Short.xlsx"
``` 
## Todo 
    - Should make a check for file sizes of the PDFs received. 

## Feedback wanted On
- This readme
- I realise I only do very surface level exception handling, are there any more errors if fixed would result in more PDFs being downloaded.
- There is a weird error where whenever the program finishes(or is about to finish i suppose) A lot of exceptions appear which looks to be related to the threads not being deleted properly, but all the threads are joined and all the writes to files happens within "with" statements so I am at a loss as to why the errors appears.    