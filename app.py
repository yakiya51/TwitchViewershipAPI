from flask import Flask
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import urllib.parse

BASE_URL = 'https://www.twitch.tv/directory/game/'

def get_viewership(game_name: str) -> int:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    
    encoded_game_name = urllib.parse.quote(game_name)
    driver.get(BASE_URL + encoded_game_name)

    try: 
        viewership = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'strong'))
        )
    except:
        driver.quit()
        return f"ERROR: Failed to scrape viewership data."

    p = viewership.find_element_by_xpath('..').get_attribute('title')
    driver.quit()
    return int(p.replace('Viewers', '').replace(',', '').strip())

app = Flask(__name__)

@app.route('/')
def home():
    return 'index'

@app.route('/viewership/<game>')
def get_viewers(game):
    return {"game": game, "viewers" : get_viewership(game)}
