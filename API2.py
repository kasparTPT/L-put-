import requests
import os
from datetime import datetime, timedelta, timezone

def get_estonian_prices(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data from Elering API: {e}")
        return None

    estonian_prices = []
    try:
        for item in data['data']['ee']:
            price_eur_mwh = item['price']
            price_cent_kwh = (price_eur_mwh * 100) / 1000
            estonian_prices.append(price_cent_kwh)
    except KeyError as e:
        print(f"Key error in data extraction: {e}")
        return None

    return estonian_prices

def save_prices_to_file(prices, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(output_file, 'w') as file:
            for i, price in enumerate(prices, start=1):
                file.write(f"Hour {i}: {price:.2f} cents/kWh\n")
        print(f"Prices saved to {output_file}")
    except Exception as e:
        print(f"Error saving prices to file: {e}")

def get_next_day_api_url():
    today = datetime.now(timezone.utc)
    next_day = today + timedelta(days=1)

    start_time = today.replace(hour=21, minute=0, second=0, microsecond=999).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = next_day.replace(hour=21, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    api_url = f"https://dashboard.elering.ee/api/nps/price?start={start_time}&end={end_time}"
    return api_url

if __name__ == "__main__":
    api_url = get_next_day_api_url()
    
    estonian_prices = get_estonian_prices(api_url)

    if estonian_prices:
        output_file = r"C:\Users\Kaspar\LÕPUTÖÖ\prices\estonian_prices.txt"
        save_prices_to_file(estonian_prices, output_file)
    else:
        print("No prices to save.")
