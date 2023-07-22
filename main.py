import json, requests, datetime
import os

from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

headers = {'Authorization': 'Basic OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA=='}

def get_current_currency():
    req = requests.get("https://api.wise.com/v1/rates?source=NZD&target=BRL", headers=headers)
    data = json.loads(req.text)
    print(f"Current price: {data[0]['rate']}")
    return round(data[0]["rate"], 2)

def get_currency_history():
    req = requests.get("https://wise.com/rates/history+live?source=NZD&target=BRL&length=30&resolution=hourly&unit=day", headers=headers)
    data = json.loads(req.text)

    min_price = min(data, key=lambda x: x['value'])
    max_price = max(data, key=lambda x: x['value'])
    
    history = dict(min_value=str(round(min_price["value"], 2)), 
                   min_value_date=datetime.datetime.fromtimestamp(min_price["time"]/1000).strftime('%d/%m/%Y'),
                   max_value=str(round(max_price["value"], 2)), 
                   max_value_date=datetime.datetime.fromtimestamp(max_price["time"]/1000).strftime('%d/%m/%Y'))

    print(f"Min value: {history['min_value']}, Date: {history['min_value_date']} \nMax value: {history['max_value']}, Date: {history['max_value_date']}")
    return history

def send_telegram_message(current_price, history):
    try:
        apiURL = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
        current_price = str(current_price)
        min_value = str(history['min_value'])
        min_value_date = str(history['min_value_date'])
        max_value = str(history['max_value'])
        max_value_date = str(history['max_value_date'])
         
        response = requests.post(apiURL, json={'chat_id': CHAT_ID, 'text': f"Current price: {current_price} \nMin value: {min_value}, Date: {min_value_date} \nMax value: {max_value}, Date: {max_value_date}"})
        return response.text
    except Exception as e:
        return print(e)

def main():
    current_price, history = (get_current_currency(), get_currency_history())
    
    send_telegram_message(current_price, history)

if __name__ == "__main__":
    main()