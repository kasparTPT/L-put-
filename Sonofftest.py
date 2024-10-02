import os
import requests
from datetime import datetime

def read_prices_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    prices = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split(":")
                if len(parts) == 2:
                    try:
                        price = float(parts[1].strip().split()[0])
                        prices.append(price)
                    except ValueError:
                        print(f"Could not convert line to price: {line}")
                        return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None
    
    return prices

def check_current_hour_price(prices):
    current_hour = datetime.now().hour

    if current_hour >= len(prices):
        print("Error: Missing price data for the current hour.")
        return
    
    current_price = prices[current_hour]
    
    if current_price < 8:
        print("Käivita elekter!")
        activate_webhook_under_8_cents()
    else:
        print("Jääme katla peale")
        activate_webhook_over_8_cents()

def activate_webhook_under_8_cents():
    url = "https://eu-apia.coolkit.cc/v2/smartscene2/webhooks/execute?id=5a0d55c4f5754c798813f0c21111108d"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Webhook for under 8 cents triggered successfully.")
        else:
            print(f"Failed to trigger webhook for under 8 cents. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error triggering webhook for under 8 cents: {e}")

def activate_webhook_over_8_cents():
    url = "https://eu-apia.coolkit.cc/v2/smartscene2/webhooks/execute?id=65c2e108a1d246208582cab8912ec92a"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Webhook for over 8 cents triggered successfully.")
        else:
            print(f"Failed to trigger webhook for over 8 cents. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error triggering webhook for over 8 cents: {e}")

if __name__ == "__main__":
    file_path = r"C:\Users\Kaspar\LÕPUTÖÖ\prices\estonian_prices.txt"
    
    prices = read_prices_from_file(file_path)
    
    if prices is not None:
        check_current_hour_price(prices)
