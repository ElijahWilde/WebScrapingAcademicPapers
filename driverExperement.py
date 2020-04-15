# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 11:55:13 2020

@author: emet
"""


import pandas as pd
import re
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Import Data

df = pd.read_csv(r'C:\Users\emet\Desktop\COMP\journal_articles_1.csv')

#myAuthors = [] #For Debugging Puposes
#myDates = [] #For Debugging Puposes
#myTitles = [] #For Debugging Puposes


#Create Search Terms For Every Paper

mySearchTerms = []

for i in range(len(df)) :
    
    string = df.iloc[i,0]
    print(string)
    
    author = re.findall('([A-Z ]+), [0-9]+, [A-Z ]+', string)
    date = re.findall('[A-Z ]+, ([0-9]+), [A-Z ]+', string)
    title = re.findall('[A-Z ]+, [0-9]+, ([A-Z ]+)', string)
    
    print(title)
    
    #myAuthors.append(author) #For Debugging Puposes
    #myDates.append(date) #For Debugging Puposes
    #myTitles.append(title) #For Debugging Puposes
    
    titleWords = re.findall('[A-Z]+', title[0])
    
    searchTerm = ""
    for j in titleWords:
        searchTerm += "SRCTITLE (*" + j + "*) "
        
    searchTerm += "PUBYEAR = " + str(date[0]) + " AND AUTHLASTNAME (*" + author[0] + "*)"
    
    mySearchTerms.append(searchTerm)
    

#Log In To Scopus

driver = webdriver.Chrome('C:/Users/emet/Desktop/COMP/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://www.scopus.com/search/form.uri?display=advanced');

time.sleep(3)

driver.find_element_by_id('pendo-close-guide-0af373a4').click()
driver.find_element_by_id('signin_link_move').click()

email_box = driver.find_element_by_id('bdd-email')
email_box.send_keys('eswilde98@gmail.com')
email_box.submit()

time.sleep(1)

pwrd_box = driver.find_element_by_id('bdd-password')
pwrd_box.send_keys('Zsxdc123')
driver.find_element_by_id('bdd-elsPrimaryBtn').click()

time.sleep(4)

#Search For Each Article And Store Info About Them In A Beautiful Soup Object

driver.find_element_by_id('searchfield').send_keys(mySearchTerms[4])

driver.find_element_by_id('advSearch').click()
