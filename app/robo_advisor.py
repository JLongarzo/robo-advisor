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

allUserInputs = []
#while(userInput != "DONE"):

inputInvalid = False
print("--------------------------------------------------")
print("Welcome to Jack's Investment Strategy and data analysis program!")
print("Please input a series of tickers like TSLA or NVDA.")
print("Feel free to input as many tickers as you like one at a time")
print("--------------------------------------------------")

userInput = input("Input DONE to finish. Have fun Investing!: ")

while(userInput != "DONE"):
    if inputInvalid == False:
        testInput = input("Would you like to input another ticker? If not, input DONE: ")
        if (testInput == "DONE"):
            userInput == "DONE"
            break
        elif (hasNumbers(testInput) == True or len(testInput) > 4):
            inputInvalid = True
        else:
            userInput = testInput.upper()
            allUserInputs.append(userInput)
            inputInvalid = False

    else:
        testInput = input("Expecting a properly-formed stock symbol like 'MSFT'. Please try again: ")
        if (testInput == "DONE"):
            userInput == "DONE"
            break
        elif (hasNumbers(testInput) == True or len(testInput) > 4):
            inputInvalid = True
        else:
            userInput = testInput.upper()
            allUserInputs.append(userInput)

t = time.localtime()
currentTime = time.strftime("%I:%m %p", t)

userInputBigString = ""
ndx = 0
while (len(allUserInputs) > ndx):
    userInputBigString = userInputBigString + " " + allUserInputs[ndx]
    ndx = ndx + 1

print("-------------------------")
print(f"SELECTED SYMBOLS:{userInputBigString}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {str(datetime.date.today())} {currentTime}") 
print("-------------------------")

allUrls = []
ndx = 0
while (len(allUserInputs) > ndx):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={allUserInputs[ndx]}&outputsize=full&apikey={apiKey}"
    allUrls.append(url)
    ndx = ndx + 1


allResponses = []

ndx = 0

while (len(allUserInputs) > ndx):
    response = requests.get(allUrls[ndx])
    #check for error
    if "Error" in response.text:
        print(f"Sorry, couldn't find any trading data for {allUserInputs[ndx]}, please try again!")
        exit()

    parsedResponse = response.json()
    allResponses.append(parsedResponse)
    ndx = ndx + 1




allStockData = []

ndx = 0
while (len(allUserInputs) > ndx):
    parsedResponse = allResponses[ndx]
    dates = []
    openPrices = []
    highPrices = []
    lowPrices = []
    closePrices = []
    dailyVolumes = []
    z = 0
    #print('ndx: ', ndx)
    #print(parsedResponse)
    for x, y in parsedResponse['Time Series (Daily)'].items():
        if z < 253:
            dates.append(x)
            openPrices.append(float(y['1. open']))
            highPrices.append(float(y['2. high']))
            lowPrices.append(float(y['3. low']))
            closePrices.append(float(y['4. close']))
            dailyVolumes.append(y['5. volume'])
            z = z + 1
    StockData = {"dates": dates, "openPrices": openPrices, "highPrices": highPrices, "lowPrices": lowPrices, "closePrices": closePrices, "dailyVolumes": dailyVolumes }
    allStockData.append(StockData)
    ndx = ndx + 1




print("COMPUTING RECOMENDATIONS AND STATISTICS... PLEASE WAIT...")
print("-------------------------")


spyUrl = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=spy&outputsize=full&apikey={apiKey}"


spyResponse = requests.get(spyUrl).json()

spyClosePrices = []
spyDates = []

z = 0
for a, b in spyResponse['Time Series (Daily)'].items():
    if z < 21:
        spyDates.append(a)
        spyClosePrices.append(float(b['4. close']))
    z = z + 1


#computes monthly change for s&p 500
spyPercentIncreaseMonth = (spyClosePrices[0] - spyClosePrices[20])/spyClosePrices[20]

allRecommendations = []

ndx = 0
while (len(allUserInputs) > ndx):
    closePrices = allStockData[ndx]["closePrices"]
    #computes monthly change for user's stock
    userStockPercentIncreaseMonth = (closePrices[0]-closePrices[20])/closePrices[20]

    

    #must test if the stock increased or decreased

    userIncDec = "DECREASED"
    if (userStockPercentIncreaseMonth > 0):
        userIncDec = "INCREASED"

    spyIncDec = "DECREASED"
    if (spyPercentIncreaseMonth > 0):
        spyIncDec = "INCREASED"

    recommendation = "BUY!"
    reason = f"{userInput} HAS BEEN UNDERPERFORMING THE MARKET"
    if(spyPercentIncreaseMonth < userStockPercentIncreaseMonth):
        recommendation = "SELL!, DONT BUY THE STOCK!"
        reason = f"{userInput} HAS BEEN OVERPERFORMING THE MARKET"
    Recommendation = { "rec": recommendation, "reason": reason, "userIncDec": userIncDec, "userStockPercentIncreaseMonth": userStockPercentIncreaseMonth }
    allRecommendations.append(Recommendation)
    ndx = ndx + 1


ndx = 0
while (len(allUserInputs) > ndx):
    userInput = allUserInputs[ndx]
    userIncDec = allRecommendations[ndx]["userIncDec"]
    userStockPercentIncreaseMonth = allRecommendations[ndx]["userStockPercentIncreaseMonth"]
    recommendation = allRecommendations[ndx]["rec"]
    reason = allRecommendations[ndx]["reason"]

    StockData = allStockData[ndx]

    latestDate = StockData["dates"][0]

    latestClose = to_usd(StockData["closePrices"][0])


    annualHigh = to_usd(float(max(StockData["highPrices"])))

    annualLow = to_usd(float(min(StockData["lowPrices"])))

    print(f"-----------{allUserInputs[ndx]}-----------")

    print(f"MOST RECENT TRADING DAY: {latestDate}")
    print(f"LATEST CLOSE: {latestClose}")
    print(f"52 WEEK HIGH: {annualHigh}")
    print(f"52 WEEK LOW: {annualLow}")
    print("- - - - - - - - - - - - -")
    print(f"{userInput} HAS {userIncDec} {str(round(userStockPercentIncreaseMonth*100, 2))}% THIS MONTH")
    print(f"THE S&P 500 HAS {spyIncDec} {str(round(spyPercentIncreaseMonth*100, 2))}% THIS MONTH")

    print(f"RECOMMENDATION: {recommendation}")
    print(f"RECOMMENDATION REASON: {reason}")
    print("-------------------------")
    ndx = ndx + 1


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



