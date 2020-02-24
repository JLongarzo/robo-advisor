import datetime
import time
import requests
import os
from dotenv import load_dotenv 

load_dotenv()

apiKey = str(os.getenv("ALPHAVANTAGE_API_KEY", "ERROR"))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def to_usd(my_price):
    return f"${my_price:,.2f}"




inputInvalid = False
userInput = ""

while(userInput == ""):
    if inputInvalid == False:
        testInput = input("Please input a stock ticker: ")
        if (hasNumbers(testInput) == True or len(testInput) > 4):
            inputInvalid = True
        else:
            userInput = testInput
    else:
        testInput = input("Expecting a properly-formed stock symbol like 'MSFT'. Please try again: ")
        if (hasNumbers(testInput) == True or len(testInput) > 4):
            inputInvalid = True
        else:
            userInput = testInput



t = time.localtime()
currentTime = time.strftime("%I:%m %p", t)



print("-------------------------")
print(f"SELECTED SYMBOL: {userInput}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.date.today())} {currentTime}") 
print("-------------------------")



url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={userInput}&outputsize=full&apikey={apiKey}"

