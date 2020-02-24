import datetime
import time
import requests
import os
from dotenv import load_dotenv 

load_dotenv()

apiKey = str(os.getenv("ALPHAVANTAGE_API_KEY", "ERROR"))



def to_usd(my_price):
    return f"${my_price:,.2f}"

