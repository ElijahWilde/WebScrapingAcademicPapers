import pandas as pd
import re

df = pd.read_csv(r'C:\Users\emet\Desktop\journal_articles_1.csv')

noDoi = []
dois =[]

#iterate over data frame. seperate it into one list of DOIS and one list of citations with no DOI
for i in range(len(df)) :
    
    string = df.iloc[i,0]
    doi = re.findall("DOI 10(.*)", string)
    
    if (len(doi) > 0):
        dois.append("10." + doi[0])
        noDoi.append("")

    else:
        dois.append("")
        noDoi.append(string)
        
        
        
#"I'm totally a real web browser and not a web scraping tool. Trust me."
import requests
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})



from bs4 import BeautifulSoup

url = "https://dx.doi.org/" + dois[16]
#https://dx.doi.org/10.1177/0049124192021002005

req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
print(soup.prettify())


#This is how the div I am looking for appears when I inspect the website:
#<a class="entryAuthor" href="/action/doSearch?target=default&amp;ContribAuthorStored=Browne%2C+Michael+W" aria-label="Open contributor information pop-up for Michael W. Browne"> Michael W. Browne</a>

#But this line does not work:
#soup.find_all("a" class_="entryAuthor")
