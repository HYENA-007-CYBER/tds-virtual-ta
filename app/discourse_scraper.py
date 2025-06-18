import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def login():
    print("🔐 Logging into Discourse portal...")
    driver.get("https://discourse.onlinedegree.iitm.ac.in/login")
    time.sleep(3)

    try:
        username_input = driver.find_element(By.ID, "login-account-name")
        password_input = driver.find_element(By.ID, "login-account-password")
        username_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)

        # Use button ID instead of XPath text
        submit_button = driver.find_element(By.ID, "login-button")
        submit_button.click()
        time.sleep(5)
        print("✅ Logged in successfully!")
    except Exception as e:
        print("❌ Login failed:", e)
        driver.quit()
        exit()


def scrape_topics():
    print("🔍 Scraping Discourse TDS KB...")
    driver.get("https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34")
    time.sleep(5)

    topics_data = []

    # Scroll and collect all topic links
    for _ in range(3):  # adjust scroll times if needed
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    topic_links = driver.find_elements(By.CSS_SELECTOR, "a.title.raw-link.raw-topic-link")

    print(f"🧵 Found {len(topic_links)} topics.")
    for link in topic_links:
        href = link.get_attribute("href")
        title = link.text.strip()
        topics_data.append({"title": title, "url": href})

    return topics_data

def scrape_topic_content(topics):
    full_data = []
    for topic in topics:
        driver.get(topic["url"])
        time.sleep(3)

        try:
            post_elements = driver.find_elements(By.CSS_SELECTOR, "div.topic-body div.cooked")
            posts = [el.text.strip() for el in post_elements if el.text.strip()]
        except Exception as e:
            posts = []
        
        full_data.append({
            "title": topic["title"],
            "url": topic["url"],
            "posts": posts
        })

    return full_data

def save_data(data):
    with open("discourse_tds_kb.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ Scraped", len(data), "topics. Data saved to discourse_tds_kb.json")

if __name__ == "__main__":
    login()
    topics = scrape_topics()
    data = scrape_topic_content(topics)
    save_data(data)
    driver.quit()
