from bs4 import BeautifulSoup
import requests
import json
import sendemail

# class kijiji:
#     def __init__(self, name, url):
#         result = requests.get(url)
#         doc = BeautifulSoup(result.text, "html.parser")
#         self.name = name
#         self.price = doc.find("div", {"class": "YMlKec fxKbKc"}).text
#     def print(self):
#         print("name: " + self.name)
#         print("price: " + self.price)
#     def to_array(self):
#         return [self.name, self.price]

def writeNewAds(ads):
    with open("/var/projects/email-webscraper/ads.json", "w") as f:
        json.dump(ads, f)
        
def getAds():
    with open("/var/projects/email-webscraper/ads.json", "r") as f:
        return json.load(f)
    
def check_ads(ads, old_ads):
    new_ads = []
    for ad in ads:
        if ad not in old_ads:
            new_ads.append(ad)
    return new_ads




result = requests.get("https://www.kijiji.ca/b-ontario/radar-gun/k0l9004")
doc = BeautifulSoup(result.text, "html.parser")
ad_results = doc.findAll("div", {"class": "search-item regular-ad"})
ads = []

for ad in ad_results:
    description = ad.find("div", {"class": "description"}).text.strip()
    locatDate = ad.find("div", {"class": "location"}).findAll("span")
    location, date = [span.text.strip() for span in locatDate]
            
    price = ad.find("div", {"class": "price"}).text.strip()
    ads.append({
        "description": description,
        "location": location,
        "price": price,
        "link": ad.find("div", {"class": "title"}).a["href"]
    })

old_ads = getAds()

new_ads = check_ads(ads, old_ads)
if new_ads != []:
    print("New ads found:")
    for ad in new_ads:
        print(ad)
        email_receiver = "5192743944@txt.bell.ca"
        sendemail.send(email_receiver, "", """
            New Radar Gun ad found boss
            Price: """+ ad["price"] +"""
            location: """+ ad["location"] +"""
            description: """+ ad["description"] +"""
            link: https://www.kijiji.ca"""+ ad["link"] +"""
        """)
    writeNewAds(ads)
else:
    print("No new ads found.")




print("Ads saved to ads.json")
