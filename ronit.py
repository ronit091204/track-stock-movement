import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+12059557997"
VERIFIED_NUMBER = "+918860054109"

TWILIO_SID = "AC7d6ee160c6c282f6f6af663fde500aae"
TWILIO_AUTH_TOKEN = "ac319645a698339dfbb5fa318682f525"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key= "ELL72VJJ2BZXOOHJ"
news_api_key = "6ea2a00c5d3e4795a0e93d82bc864760"


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}
response=requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
day_before_yesterday=data_list[1]
day_before_yesterday_closing_price=day_before_yesterday["4. close"]


difference=float(yesterday_closing_price)-float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = round((difference / float(yesterday_closing_price)) * 100)


if abs(diff_percent) > 1:
    news_params = {
        "apiKey": news_api_key,
        "qInTitle": COMPANY_NAME,
    }

    response2=requests.get(NEWS_ENDPOINT,news_params)
    articles = response2.json()["articles"]
    three_articles = articles[:3]
    



    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )





