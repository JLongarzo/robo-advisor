import datetime
import time
import requests
import os
from dotenv import load_dotenv 
import pandas

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
        testInput = input("Please input a stock ticker like TSLA. Have fun Investing!: ")
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
print("COMPUTING RECOMENDATION... PLEASE WAIT...")


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




#computes monthly change for user's stock
userStockPercentIncreaseMonth = (closePrices[0]-closePrices[20])/closePrices[20]

#computes monthly change for s&p 500
spyPercentIncreaseMonth = (spyClosePrices[0] - spyClosePrices[20])/spyClosePrices[20]

#must test if the stock increased or decreased

userIncDec = "DECREASED"
if (userStockPercentIncreaseMonth > 0):
    userIncDec = "INCREASED"

spyIncDec = "DECREASED"
if (spyPercentIncreaseMonth > 0):
    spyIncDec = "INCREASED"

recommendation = "BUY!"
reason = f"{userInput} IS UNDERPERFORMING THE MARKET"
if(spyPercentIncreaseMonth < userStockPercentIncreaseMonth):
    recommendation = "SELL!, DONT BUY THE STOCK!"
    reason = f"{userInput} IS OVERPERFORMING THE MARKET"



print(f"{userInput} HAS {userIncDec} {str(round(userStockPercentIncreaseMonth*100, 2))}% THIS MONTH")
print(f"THE S&P 500 HAS {spyIncDec} {str(round(spyPercentIncreaseMonth*100, 2))}% THIS MONTH")

print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#found this function here https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
def get_parent_dir(directory):
    import os
    return os.path.dirname(directory)


def write_to_csv(csvData):
	dataPath = get_parent_dir(os.getcwd()) + "/data/"
	csvData.to_csv(dataPath + "prices_" + userInput + ".csv")


csvData = pandas.DataFrame({
		'Time': dates,
		'Opening Price': openPrices,
		'High Price': highPrices,
		'Low Price': lowPrices,
		'Closing Price': closePrices,
		'Volume': dailyVolumes
		})

write_to_csv(csvData)



