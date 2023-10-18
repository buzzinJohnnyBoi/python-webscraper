from bs4 import BeautifulSoup
import requests

class stocks:
    def __init__(self, name, url):
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        self.name = name
        self.price = doc.find("div", {"class": "YMlKec fxKbKc"}).text
    def print(self):
        print("name: " + self.name)
        print("price: " + self.price)
    def to_array(self):
        return [self.name, self.price]
    
    
