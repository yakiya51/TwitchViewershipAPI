from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

DRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'
BASE_URL = 'https://www.twitch.tv/directory/game/'

def get_viewership(game_name: str) -> int:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    driver.get(BASE_URL + game_name)

    try: 
        viewership = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'strong'))
        )
    except:
        print("Failed to scrape viewership data.")
        driver.quit()

    p = viewership.find_element_by_xpath('..').get_attribute('title')
    driver.quit()
    return int(p.replace('Viewers', '').replace(',', '').strip())

app = Flask(__name__)

@app.route('/', mehtods=['GET'])
def home():
    return 'index'

@app.route('/<str:game>', mehtods=['GET'])
def get_viewers(game):
    return {"game": game, "viewers" : get_viewership(game)}
