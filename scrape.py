# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 20:43:28 2020

@author: emet
"""

import pandas as pd
import re
finalResult = []

# FORMATTING DATA==============================================================

df = pd.read_csv(r'C:\Users\emet\Desktop\COMP\journal_articles_1.csv')

noDoi = []
dois =[]

#iterate over data frame. seperate it into one list of DOIS and one list of citations with no DOI
for i in range(len(df)) :
    
    string = df.iloc[i,0]
    doi = re.findall("DOI 10(.*)", string)
    
    if (len(doi) > 0):
        dois.append("10." + doi[0])
        #noDoi.append("")

    else:
        dois.append("")
        #noDoi.append(string)


# MAKING THE SOUP==============================================================     
import requests
from bs4 import BeautifulSoup

# Set headers
headers = requests.utils.default_headers()

#soup0, soup1, soup2 = BeautifulSoup('<p>will replace these objects later</p>')
soups = []

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def searchString(tagType, searchTerm): #tag type can be "any"
    myList = []
    if tagType == "any":
        for soup in soups:
            myList.append(soup.find_all(text = re.compile(searchTerm)))
    else:
        for soup in soups:
            myList.append(soup.find_all(tagType, text = re.compile(searchTerm)))
    
    return myList

def searchClass(tagType, myClass):
    myList = []
    for soup in soups:
        myList.append(soup.find_all(tagType, {'class':  myClass}))
    return myList
    
# SEARCHING DATA===============================================================
#from torrequest import TorRequest
import random

def whoPublishedThis(soup): 
   if (len(searchClass(("div"),("SAGECopyright"))[0]) > 0):
       return 'SAGE'
    
mysteryDois = []

dois = ["https://dx.doi.org/"+doi if doi != "" else doi for doi in dois]

sagePapers = []
numSage = 0
for doi in dois:
    if doi != "":
        headers.update({ 'User-Agent': random.choice(user_agent_list)}) #switch browsers to keep em guessing
        req = requests.get(doi, headers)

        soup0 = BeautifulSoup(req.content, 'xml')
        #soup1 = BeautifulSoup(req.content, 'html.parser')
        #soup2 = BeautifulSoup(req.content, 'lxml')
        
        soups = [soup0] #in case I need to add more parsers
        
        pub = whoPublishedThis(soup0)
        
        if (pub == 'SAGE'):
            numSage += 1
            sagePapers.append()
        else: 
            mysteryDois.append(doi)
        
