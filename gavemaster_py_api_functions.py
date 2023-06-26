import yfinance as yf
from datetime import datetime, timedelta
import requests


def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return round(todays_data['Close'][0], 2)


def get_price_change_percentage(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)

    historical_data = ticker.history(start=start_date, end=end_date)

    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]

    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)


def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    historical_data = ticker.history(start=start_date, end=end_date)
    old_price = historical_data['Close'].iloc[0]
    new_price = historical_data['Close'].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)


def get_best_performing_stock(stocks, days_ago):
    best_stock = None
    best_performance = None

    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if best_performance is None or performance > best_performance:
                best_performance = performance
                best_stock = stock
        except Exception as e:
            print(f"could not get performance for {stock}: {e}")
    return best_stock, best_performance



def get_sport_events_by_date(sport, league, days, teams):

    if days > 0:
        dste = datetime.now() + timedelta(days=days)
    else:
        dste = datetime.now() - timedelta(days=abs(days))

    date = dste.strftime("%Y%m%d")

    url = "https://site.api.espn.com/apis/site/v2/sports/" + sport + "/" + league + "/scoreboard?dates=" + date
    response = requests.get(url)
    json_data = response.json()
    
    events = json_data['events']
    relevant_data = []
    for event in events:
        team1 = event['competitions'][0]['competitors'][0]['team']['displayName']
        team2 = event['competitions'][0]['competitors'][1]['team']['displayName']  

        specific_keys = {
            "event": event.get("name"),
            "isFinished": event["status"]["type"].get('completed'),
            "when": event.get("date"),
            "id": event.get("id"),
            "headlines": event.get("headlines"),
            "venue": event['competitions'][0].get("venue"),
            "format": event['competitions'][0].get("format"),
            "notes": event['competitions'][0].get("notes"),
        }

        if (team1 or team2 in teams) or teams == None:
            relevant_data.append(specific_keys)
    
    return relevant_data