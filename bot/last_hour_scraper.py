from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import numpy as np
import random
import time
import undetected_chromedriver as uc
import pandas as pd
from parse_tweets import *
from datetime import datetime, timezone


load_dotenv()

TWITTER_USER = os.getenv("TWITTER_USER")
TWITTER_PASS = os.getenv("TWITTER_PASS")


wait_seconds = list(np.arange(5,10))
wait_short = list(np.arange(2,5))

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = uc.Chrome(options=options,version_main=137)
    return driver

def login_to_twitter(driver):
    try:
        driver.get("https://x.com/login")
        time.sleep(5)

        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(TWITTER_USER)
        username_input.send_keys(Keys.RETURN)
        time.sleep(3)

        try:
            confirm_user = driver.find_element(By.NAME, "text")
            confirm_user.send_keys(TWITTER_USER)
            confirm_user.send_keys(Keys.RETURN)
            time.sleep(3)
        except:
            pass

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TWITTER_PASS)
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)

        return True
    except Exception as e:
        print("Login failed:", e)
        return False

def extract_tweets_data(results,records):
    for tweet in records:
        try:
            content = tweet.text
            if "David Faitelson reposted" not in content:
                link = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                tweet_url = link.get_attribute('href')
                timestamp_elem = link.find_element('xpath', './/time')
                timestamp = timestamp_elem.get_attribute('datetime')
                tweet_id = tweet_url.split("/")[-1]
                results.append({"tweet_id": tweet_id, "text": content,"datetime":timestamp})
        except Exception as e:
            print("Skipped a tweet due to error:", e)
    return results

def search_faitel_tweets(driver):
    search_url = "https://x.com/DavidFaitelson_"
    driver.get(search_url)
    time.sleep(random.choice(wait_seconds))

    results = []
    records = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    results = extract_tweets_data(results, records)

    # scroll once
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    records = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    results = extract_tweets_data(results, records)
    
    return results

def parse_tweets(results,now):
    df = pd.DataFrame.from_records(results)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['user'] = df.text.map(get_user)
    df['tweet'] = df.text.map(format_text)

    # Filter only the tweets from the last hour
    df = df[df['datetime']> (now - pd.Timedelta(hours=1))]

    return df


def scrape_tweets():
    now = datetime.now(timezone.utc)
    driver = create_driver()
    logged = login_to_twitter(driver)
    if logged:
        results = search_faitel_tweets(driver)
        driver.quit()
        tweets = parse_tweets(results,now)

        return tweets
    else:
        driver.quit()
        print("Failed log in")
        return []
