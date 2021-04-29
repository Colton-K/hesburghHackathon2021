import requests
from bs4 import BeautifulSoup

northHoursURL = "https://dining.nd.edu/locations-menus/north-dining-hall/"
southHoursURL = "https://dining.nd.edu/locations-menus/south-dining-hall/"
menuURL = "http://nutrition.nd.edu/NetNutrition/1"

def getNorthHours():
    return getDhHours(northHoursURL)

def getSouthHours():
    return getDhHours(southHoursURL)

def getDhHours(url):
    page = requests.get(northURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    text = soup.get_text()
    iStart = text.index('Hours')
    iEnd = text.index('Grab and Go')
    print(text[iStart:iEnd])

def getNorthMenu():
    return ""

def getSouthMenu():
    return ""

if __name__ == "__main__":
    getNorthHours()
    getSouthHours()
    getNorthMenu()