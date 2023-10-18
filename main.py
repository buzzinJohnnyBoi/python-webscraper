import sendemail
import stockclass
from decimal import Decimal
def getStocks():
    stock = stockclass.stocks("google", "https://www.google.com/finance/quote/GOOGL:NASDAQ?sa=X&ved=2ahUKEwjZv-Dzur79AhUAjIkEHcqtBTgQ3ecFegQIHxAg")
    return stock.price[1:]

price = Decimal(getStocks())
num_stocks = round(100_000/90)

bank = num_stocks * (price - 90)

email_sender = "johncamp724@gmail.com"
email_password = "" # I deleted this part
email_receiver = "5192743944@txt.bell.ca"

# subject = "This is not spam "
# body = """
# Hello, this is absolutely not spam, check our my website:
# johntheguy.tk 
# """


sendemail.send(email_receiver, "", "You have made: $" + str(bank) + " off Google stock. Nice")

print("done")