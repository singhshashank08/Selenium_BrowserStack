from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor


BROWSERSTACK_USERNAME = 'shashanksingh_W9rR2x'
BROWSERSTACK_ACCESS_KEY = 'TdePiq1i45x5qPavh3sT'


TRANSLATION_API_KEY = 'AIzaSyAsvLDSUayax-9LbKzgTE5Y1yOBVcsBVSk'
TRANSLATION_URL = 'https://translation.googleapis.com/language/translate/v2'


def get_browserstack_driver(browser_name, os_version, browser_version):
    capabilities = {
        "os": "Windows",
        "os_version": os_version,
        "browser": browser_name,
        "browser_version": browser_version,
        "name": "Selenium Test on BrowserStack",
        "browserstack.local": "false",
        "browserstack.selenium_version": "3.141.59",
    }
    return webdriver.Remote(
        command_executor=f"https://{'shashanksingh_W9rR2x'}:{'TdePiq1i45x5qPavh3sT'}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=capabilities,
    )


def scrape_articles(driver):
    driver.get("https://elpais.com")
    driver.find_element(By.LINK_TEXT, "Opinión").click()
    articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
    results = []
    for article in articles:
        title = article.find_element(By.CSS_SELECTOR, "h2").text
        content = article.find_element(By.CSS_SELECTOR, "p").text
        img_url = article.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        results.append({"title": title, "content": content, "img_url": img_url})
    return results


def translate_titles(titles):
    translations = []
    for title in titles:
        payload = {"q": title, "source": "es", "target": "en", "key": TRANSLATION_API_KEY}
        response = requests.post(TRANSLATION_URL, data=payload)
        translations.append(response.json()["data"]["translations"][0]["translatedText"])
    return translations

def analyze_headers(headers):
    word_count = {}
    for header in headers:
        for word in header.split():
            word_count[word] = word_count.get(word, 0) + 1
    repeated_words = {word: count for word, count in word_count.items() if count > 2}
    return repeated_words


def main(browser_name, os_version, browser_version):
    driver = get_browserstack_driver(browser_name, os_version, browser_version)
    try:
        articles = scrape_articles(driver)
        titles = [article["title"] for article in articles]
        translated_titles = translate_titles(titles)
        repeated_words = analyze_headers(translated_titles)

        print(f"Browser: {browser_name}, OS: {os_version}, Version: {browser_version}")
        print("Original Titles:", titles)
        print("Translated Titles:", translated_titles)
        print("Repeated Words:", repeated_words)

        # Download Images
        for idx, article in enumerate(articles):
            img_url = article["img_url"]
            if img_url:
                img_data = requests.get(img_url).content
                with open(f"article_{idx+1}.jpg", "wb") as file:
                    file.write(img_data)
    finally:
        driver.quit()
def execute_in_parallel():
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
execute_in_parallel()
