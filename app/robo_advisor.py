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
            userInput = testInput.upper()
    else:
        testInput = input("Expecting a properly-formed stock symbol like 'MSFT'. Please try again: ")
        if (hasNumbers(testInput) == True or len(testInput) > 4):
            inputInvalid = True
        else:
            userInput = testInput.upper()



t = time.localtime()
currentTime = time.strftime("%I:%m %p", t)



print("-------------------------")
print(f"SELECTED SYMBOL: {userInput}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.date.today())} {currentTime}") 
print("-------------------------")



url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={userInput}&outputsize=full&apikey={apiKey}"



response = requests.get(url)

#check for error
if "Error" in response.text:
    print("Sorry, couldn't find any trading data for that stock symbol, please try again!")
    exit()


parsedResponse = response.json()





dates = []
openPrices = []
highPrices = []
lowPrices = []
closePrices = []
dailyVolumes = []

z = 0
for x, y in parsedResponse['Time Series (Daily)'].items():
    if z < 253:
        dates.append(x)
        openPrices.append(float(y['1. open']))
        highPrices.append(float(y['2. high']))
        lowPrices.append(float(y['3. low']))
        closePrices.append(float(y['4. close']))
        dailyVolumes.append(y['5. volume'])
        z = z + 1




latestDate = dates[0]

latestClose = to_usd(closePrices[0])

annualHigh = to_usd(float(max(highPrices)))

annualLow = to_usd(float(min(lowPrices)))



print(f"MOST RECENT TRADING DAY: {latestDate}")
print(f"LATEST CLOSE: {latestClose}")
print(f"52 WEEK HIGH: {annualHigh}")
print(f"52 WEEK LOW: {annualLow}")
print("-------------------------")



spyUrl = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=spy&outputsize=full&apikey={apiKey}"


spyResponse = requests.get(spyUrl).json()


spyClosePrices = []
spyDates = []

z = 0
for x, y in spyResponse['Time Series (Daily)'].items():
    if z < 21:
        spyDates.append(x)
        spyClosePrices.append(float(y['4. close']))
    z = z + 1





spyPercentIncreaseMonth = (spyClosePrices[0] - spyClosePrices[20])/spyClosePrices[20]
print('spyPercentIncreaseMonth: ', spyPercentIncreaseMonth)

userStockPercentIncreaseMonth = (closePrices[0]-closePrices[20])/closePrices[20]
print('userStockPercentIncreaseMonth', userStockPercentIncreaseMonth)

print(f"{userInput} HAS INCREASED {str(round(userStockPercentIncreaseMonth*100, 2))}% THIS MONTH")
print(f"THE S&P 500 HAS INCREASED {str(round(spyPercentIncreaseMonth*100, 2))}% THIS MONTH")

print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")