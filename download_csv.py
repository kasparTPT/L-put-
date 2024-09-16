import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def download_csv():
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.add_argument("--disable-search-engine-choice-screen")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = "https://dashboard.elering.ee/et/nps/price"
    driver.get(url)

    time.sleep(5)

    try:
        cookie_button = driver.find_element(By.XPATH, "//button[contains(text(),'Nõustu valitud küpsistega')]")
        cookie_button.click()
        print("Cookie pop-up accepted")
    except Exception as e:
        print("No cookie pop-up found or an error occurred:", e)

    try:
        csv_button = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/ng-component/div[2]/div/div[1]/div[1]/div[1]/a')
        csv_button.click()
        print("CSV download initiated")
    except Exception as e:
        print(f"Failed to find the CSV button: {e}")

    time.sleep(10)

    driver.quit()

    print(f"CSV file downloaded and saved to {download_dir}")

if __name__ == "__main__":
    download_csv()
