import json
from scraper import Scraper
from sendemail import email

def writeAds(type, ads):
    if type == "focus":
        with open("/var/projects/email-webscraper/dad-webscraper/focus/ads.json", "w") as f:
            json.dump(ads, f, indent=4)
    else:
        with open("/var/projects/email-webscraper/dad-webscraper/fiesta/ads.json", "w") as f:
            json.dump(ads, f, indent=4)
        
def getAds(type):
    if type == "focus":
        with open("/var/projects/email-webscraper/dad-webscraper/focus/ads.json", "r") as f:
            return json.load(f)
    else:
        with open("/var/projects/email-webscraper/dad-webscraper/fiesta/ads.json", "r") as f:
            return json.load(f)
    
def writeNewAds(type, ads):
    if type == "focus":
        with open("/var/projects/email-webscraper/dad-webscraper/focus/new.json", "w") as f:
            json.dump(ads, f, indent=4)
    else:
        with open("/var/projects/email-webscraper/dad-webscraper/fiesta/new.json", "w") as f:
            json.dump(ads, f, indent=4)
    
def check_ads(ads, old_ads):
    new_ads = []
    for ad in ads:
        if ad not in old_ads:
            new_ads.append(ad)
    return new_ads

def addNew(ads, sendToArray, type):
    
    newAds = check_ads(ads, getAds(type))
    if newAds != []:

        writeAds(type, newAds + getAds(type))
        writeNewAds(type, newAds)

        for ad in newAds:
            print(ad["year"])
            body = """
            year: """+ ad["year"] +"""
            price: """+ ad["price"] +"""
            location: """+ ad["location"] +"""
            kilometers: """+ ad["kilometers"] +"""
            link: """+ ad["link"] +"""
            """
            
            for contact in sendToArray:
                newEmail = email("johncamp724@gmail.com", "I deleted this part, it is a random string of letters", contact, "", body)
                newEmail.send()
                
            

with open("/var/projects/email-webscraper/dad-webscraper/config.json", "r") as f:
    configObj = json.load(f)


urlFocus = "https://www.kijiji.ca/b-ontario/focus/k0l9004?dc=true"
pageUrlFocus = "https://www.kijiji.ca/b-ontario/focus/page-: 2 :/k0l9004?dc=true"

urlFiesta = "https://www.kijiji.ca/b-ontario/fiesta/k0l9004?dc=true"
pageUrlFiesta = "https://www.kijiji.ca/b-ontario/fiesta/page-: 2 :/k0l9004?dc=true"


newScraperFocus = Scraper([urlFocus, pageUrlFocus], ["li", "li"], configObj["Focus"]["maxPrice"], configObj["Fiesta"]["oldestYear"])

focusAds = newScraperFocus.scrape()

newScraperFiesta = Scraper([urlFiesta, pageUrlFiesta], ["li", "li"], configObj["Fiesta"]["maxPrice"], configObj["Fiesta"]["oldestYear"])

fiestaAds = newScraperFiesta.scrape()


# addNew(ads, configObj["sendTo"])

addNew(fiestaAds, configObj["sendTo"], "fiesta")
addNew(focusAds, configObj["sendTo"], "focus")


