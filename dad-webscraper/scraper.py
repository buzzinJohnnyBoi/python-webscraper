from bs4 import BeautifulSoup
import requests
import re

class Scraper:
    def __init__(self, urlArray, keyValueArray, maxPrice, maxYear):
        self.urlArray = urlArray
        self.keyValueArray = keyValueArray
        self.maxPrice = maxPrice
        self.maxYear = maxYear

    def scrape(self):
        ads = []
        for i in range(0, len(self.urlArray)):
            if ": 2 :" in self.urlArray[i]:
                for j in range(2, 100):
                    url = self.urlArray[i].replace(": 2 :", str(j))
                    result = requests.get(url)
                    if result.status_code == 200:
                        doc = BeautifulSoup(result.text, "html.parser")
                        ad_results = doc.find_all(self.keyValueArray[0])
                        ad_results = [listing for listing in ad_results if "listing-card-list-item" in listing.get("data-testid", "")]
                        for listing in ad_results:
                            new_listing = self.getValues(listing)
                            if new_listing != False:
                                ads.append(new_listing)
                                
                        last_page = doc.findAll("a", {"class": "sc-6b17eca1-0 laaUHx sc-afc33ef3-3 hAgCkH"})
                        if len(last_page) == 0:
                            break
                            
            else:
                result = requests.get(self.urlArray[i])
                doc = BeautifulSoup(result.text, "html.parser")
                ad_results = doc.find_all(self.keyValueArray[i])
                ad_results = [listing for listing in ad_results if "listing-card-list-item" in listing.get("data-testid", "")]
                for listing in ad_results:
                    obj = self.getValues(listing)
                    if obj != False:
                        ads.append(self.getValues(listing))
        
        return ads
            
            
    def getValues(self, listing):
        year = listing.find("h3", {"data-testid": "listing-title"}).text
        price = listing.find("p", {"data-testid": "listing-price"}).text
        location = listing.find("p", {"data-testid": "listing-location"}).text
        link = "https://www.kijiji.ca" + listing.find("a", {"data-testid": "listing-link"})['href']
        km_list = listing.findAll("p", {"class": "sc-c54bbc09-0 jWZAHd"})
        
        kilometers = ""
        for km in km_list:
            if "km" in km.text or "kilo" in km.text:
                kilometers = km.text
                
        obj = {
            "year": year,
            "price": price,
            "location": location,
            "kilometers": kilometers,
            "link": link
        }
        if self.validListing(obj) == True:
            return obj
        else:
            return False
        
    
    def validListing(self, obj):
        
        try:
            price_str = obj["price"].replace("$", "").replace(",", "")
            price = float(price_str)
            if price < self.maxPrice:
                s = obj["year"]
                index = s.find("20")

                if index != -1 and index + 2 < len(s):
                    if int(s[index + 2:index + 4]) >= self.maxYear:
                        return True 
                    else:
                        return False
                else:
                    if "19" in obj["year"]:
                        return False
                    return False
                        

        except ValueError:
            return True
        