import requests
import re
import os
import csv
from bs4 import BeautifulSoup

headerList=["Name","SunNeeds","LifeCycle","EaseOfCare","Height","Spread"]
flowerList = []
flowerList.append(headerList)

webPageUrl = "http://www.gardening.cornell.edu/homegardening/scenee139.html"
webPageHtml = requests.get(webPageUrl).text

soup = BeautifulSoup(webPageHtml, "html.parser")

divs = soup.findAll("div", {"class": "normal"})
for idx, div in enumerate(divs):
    if div.b.string == 'By common name:':
        for link in div.find_all('a'):
            name = link.string.replace(',',' - ')
            subWebPageUrl = "http://www.gardening.cornell.edu/homegardening/" + link.get('href')
            subWebPageHtml = requests.get(subWebPageUrl).text
            
            subSoup = BeautifulSoup(subWebPageHtml, "html.parser")
            
            subDivs = subSoup.findAll("div", {"class": "intro"})
            for idx2, subDiv in enumerate(subDivs):
                if subDiv.b != None:
                    if subDiv.b.string == 'Site Characteristics':
                        if subDivs[idx2+1].b.string == 'Sunlight:':
                            sunlight = ''
                            lis = subDivs[idx2+1].ul.findAll('li')
                            for idz, li in enumerate(lis):
                                if idz == 0:
                                    sunlight = li.string
                                else:
                                    sunlight = sunlight + ' | ' + li.string
                    elif subDiv.b.string == 'Plant Traits':
                        for p in subDivs[idx2+1].findAll("p"):
                            if p.b != None:
                                if p.b.string == 'Lifecycle:':
                                    p.b.clear()
                                    lifecycle = re.sub(r'[\t\r\n]', '', p.getText().strip()).replace(',','|')
                                elif p.b.string == 'Ease-of-care:':
                                    p.b.clear()
                                    easeOfCare = re.sub(r'[\t\r\n]', '',p.getText().strip()).replace(',','|')
                                elif p.b.string == 'Height:':
                                    p.b.clear()
                                    height = re.sub(r'[\t\r\n]', '',p.getText().strip()).replace(',','|')
                                elif p.b.string == 'Spread:':
                                    p.b.clear()
                                    spread = re.sub(r'[\t\r\n]', '',p.getText().strip()).replace(',','|')
            flower = [name, sunlight, lifecycle, easeOfCare, height, spread]
            flowerList.append(flower)
#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "flower_types_dataset.csv"
filePath = os.path.join(currentDir, filename)        
    
with open(filePath, 'w', newline = '', encoding = 'utf-8') as csvFile:
  writer = csv.writer(csvFile)
  for flower in flowerList:
    writer.writerow(flower)