from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants (replace with your actual keys)
BROWSERSTACK_USERNAME = 'shashanksingh_W9rR2x'
BROWSERSTACK_ACCESS_KEY = 'TdePiq1i45x5qPavh3sT'
TRANSLATION_API_KEY = 'AIzaSyAkSl9gQSu5NEzRjfGFNRqo0KUoUqggMQY'
TRANSLATION_URL = 'https://translation.googleapis.com/language/translate/v2'

def print_output(message, data=None):
    """Helper function to print formatted output to terminal"""
    if data:
        print(f"\n=== {message} ===")
        if isinstance(data, list):
            for idx, item in enumerate(data, 1):
                print(f"{idx}. {item}")
        elif isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(data)
    else:
        print(f"\n=== {message} ===")

def get_browserstack_driver(browser_name, os_version, browser_version):
    """Set up BrowserStack driver"""
    options = Options()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    capabilities = {
        "os": "Windows",
        "os_version": os_version,
        "browser": browser_name,
        "browser_version": browser_version,
        "name": "Selenium Test on BrowserStack",
        "browserstack.local": "false",
        "browserstack.selenium_version": "3.141.59",
    }

    driver = webdriver.Remote(
        command_executor=f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
        options=options,
        keep_alive=True
    )
    driver.capabilities.update(capabilities)
    return driver

def translate_titles(titles):
    """Translate titles from Spanish to English"""
    translations = []
    for title in titles:
        payload = {"q": title, "source": "es", "target": "en", "key": TRANSLATION_API_KEY}
        response = requests.post(TRANSLATION_URL, data=payload)
        
        # Check if the response contains the expected data
        try:
            response_data = response.json()
            translated_text = response_data["data"]["translations"][0]["translatedText"]
            translations.append(translated_text)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logging.error(f"Error in translation API response: {e}")
            translations.append(f"Translation failed for: {title}")
    return translations

def scrape_articles(driver):
    """Scrape articles from the website"""
    driver.get("https://elpais.com")
    driver.find_element(By.LINK_TEXT, "Opinión").click()
    
    # Wait for the articles to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))

    articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
    results = []
    
    for article in articles:
        title = article.find_element(By.CSS_SELECTOR, "h2").text
        content = article.find_element(By.CSS_SELECTOR, "p").text
        
        try:
            # Try to locate the image element and get its URL
            img_element = WebDriverWait(article, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "img"))
            )
            img_url = img_element.get_attribute("src")
        except Exception as e:
            img_url = None  # If image is not found, set img_url as None
            logging.warning(f"Image not found for article: {title}")

        results.append({"title": title, "content": content, "img_url": img_url})
    return results


def analyze_headers(headers):
    """Analyze headers for repeated words"""
    word_count = {}
    for header in headers:
        for word in header.split():
            word_count[word] = word_count.get(word, 0) + 1
    repeated_words = {word: count for word, count in word_count.items() if count > 2}
    return repeated_words

def main(browser_name, os_version, browser_version):
    """Main function to run the test for each browser"""
    logging.info(f"Starting test for {browser_name} on {os_version}...")
    driver = None
    try:
        driver = get_browserstack_driver(browser_name, os_version, browser_version)
        logging.info(f"Driver initialized for {browser_name} on {os_version}")

        articles = scrape_articles(driver)
        titles = [article["title"] for article in articles]
        translated_titles = translate_titles(titles)
        repeated_words = analyze_headers(translated_titles)

        print_output("Original Titles", titles)
        print_output("Translated Titles", translated_titles)
        print_output("Repeated Words", repeated_words)

        # Download images
        for idx, article in enumerate(articles):
            img_url = article["img_url"]
            if img_url:
                logging.info(f"Downloading image {img_url}...")
                img_data = requests.get(img_url).content
                with open(f"article_{idx+1}.jpg", "wb") as file:
                    file.write(img_data)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()

def execute_in_parallel():
    """Execute tests in parallel for multiple browsers"""
    browsers = [
        {"browser_name": "Chrome", "os_version": "10", "browser_version": "latest"},
        {"browser_name": "Firefox", "os_version": "10", "browser_version": "latest"},
        {"browser_name": "Safari", "os_version": "13", "browser_version": "latest"},
        {"browser_name": "Edge", "os_version": "10", "browser_version": "latest"},
        {"browser_name": "Opera", "os_version": "10", "browser_version": "latest"},
    ]
    with ThreadPoolExecutor(max_workers=5) as executor:
        for browser in browsers:
            executor.submit(main, **browser)

if __name__ == "__main__":
    execute_in_parallel()
