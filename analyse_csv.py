import os
import pandas as pd

def get_latest_csv_file(download_dir):
    csv_files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.csv')]

    if not csv_files:
        return None

    latest_file = max(csv_files, key=os.path.getmtime)
    
    return latest_file

def analyse_csv():
    download_dir = os.path.join(os.getcwd(), "downloads")
    
    csv_file = get_latest_csv_file(download_dir)
    
    if not csv_file:
        print("No CSV file found.")
        return

    print(f"Latest CSV file located: {csv_file}")

    try:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')

        if 'NPS Eesti' in df.columns:
            estonia_values = df['NPS Eesti'].dropna().values

            print("Electricity prices for Estonia (NPS Eesti) in EUR / MWh:")
            for i, value in enumerate(estonia_values):
                print(f"Hour {i+1}: {value} EUR / MWh")

        else:
            print("'NPS Eesti' column not found in the CSV file.")
    
    except Exception as e:
        print(f"Error reading the CSV file: {e}")

if __name__ == "__main__":
    analyse_csv()
