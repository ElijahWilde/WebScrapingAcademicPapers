# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 20:43:28 2020

@author: emet
"""

import pandas as pd
import re
finalResult = {
        'no_doi': [],
        'doi_does_not_return_paper': [],#list of data entries
        'paper_found': [#list of dictionaries
                            {
                                'origonal_citation':'', 
                                'author(s)':[
                                                {
                                                'name':'Sample McExample',
                                                'gender':'',
                                                'institution':'',
                                                'country':'',
                                                'rank':''
                                                }
                                            ]
                            }
                        ]
}

# FORMATTING DATA==============================================================

df = pd.read_csv(r'C:\Users\emet\Desktop\COMP\Freelon\journal_articles_1.csv')
list_of_citations = []
no_doi = []
dois =[]

#iterate over data frame. Seperate it into one list of DOIS and one list of citations with no DOI
for i in range(len(df)):
    
    citation = df.iloc[i,0]
    list_of_citations.append(citation)
    
    doi = re.findall("DOI 10(.*)", citation)
    
    if (len(doi) > 0):
        dois.append("10." + doi[0])

    else:
        no_doi.append(citation)

def findCitation(doi):
    for cit in list_of_citations:
        if doi.strip('https://dx.doi.org/10.') in cit:
            return cit

# MAKING THE SOUP==============================================================     
import requests
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()

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

def whoPublishedThis(soup):    
   if (len(searchClass(("div"),("SAGECopyright"))[0]) > 0):
       return 'SAGE'
   elif(len(searchString('any', 'DOI cannot be found in the DOI System')[0]) > 0):
       return 'ERROR'
   else:
       return 'dunno'
    
# SEARCHING DATA===============================================================
import random
import time
import sys

#https://dx.doi.org/
dois = ["https://doi.org/"+doi if doi != "" else doi for doi in dois]
doi_does_not_return_paper = []

mystery_papers = []
sage_papers = []

numSage = 0
numPapersDone = 0

for doi in dois:
    if doi != "":
      
        numPapersDone += 1
        print(numPapersDone)
        
        e = ''
        try: 
            headers.update({ 'User-Agent': random.choice(user_agent_list)}) #switch browsers to keep em guessing
            req = requests.get(doi, headers)
        except:
            e = sys.exc_info()[0]
            print(e)
            doi_does_not_return_paper.append(doi)
            print("paper appended to 'doi_does_not_return_paper' (threw exception)")
        
        if (e == ''):
            
            soup0 = BeautifulSoup(req.content, 'xml')
            soup1 = BeautifulSoup(req.content, 'html.parser')
            soup2 = BeautifulSoup(req.content, 'lxml')
            
            soups = [soup0,soup1,soup2] #in case I need to add more parsers
            
            pub = whoPublishedThis(soup0)
            
            if (pub == 'SAGE'):
                numSage += 1
                sage_papers.append(doi, soups)
                print("paper appended to 'sage_papers'")
            elif (pub == 'ERROR'):
                doi_does_not_return_paper.append(doi)
                print("paper appended to 'doi_does_not_return_paper' (did not throw exception)")
            else: 
                mystery_papers.append((doi, soups))
                print("paper appended to 'mystery_papers'")
                
            
        time.sleep(.5)
        
        if (len(mystery_papers) >= 3):
            break
