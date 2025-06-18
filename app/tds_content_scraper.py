import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TDS_URL = "https://tds.s-anand.net/#/"

def scrape_tds_toc():
    print("🚀 Launching browser...")

    options = Options()
    # Do not run headless – you need to see what’s happening
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(TDS_URL)

    try:
        print("🔍 Waiting for sidebar container...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar"))
        )
        print("✅ Sidebar found. Scrolling to trigger TOC rendering...")

        # Scroll down + up to trigger lazy load
        driver.execute_script("document.querySelector('.sidebar').scrollTop = 10000")
        time.sleep(1.5)
        driver.execute_script("document.querySelector('.sidebar').scrollTop = 0")
        time.sleep(1.5)

        # Try loading section-links multiple times
        toc_links = []
        for i in range(10):
            print(f"🔁 Attempt {i+1}: Looking for .section-link elements...")
            toc_links = driver.find_elements(By.CSS_SELECTOR, "a.section-link")
            if toc_links:
                print(f"✅ Found {len(toc_links)} links.")
                break
            time.sleep(1)

        if not toc_links:
            raise Exception("❌ .section-link not found even after 10 attempts.")

        toc_data = []
        for link in toc_links:
            title = link.get_attribute("title") or link.text
            href = link.get_attribute("href")
            if title and href:
                toc_data.append({
                    "title": title.strip(),
                    "url": href.strip()
                })
                print(f"• {title.strip()} → {href.strip()}")

        with open("tds_data.json", "w", encoding="utf-8") as f:
            json.dump(toc_data, f, indent=2, ensure_ascii=False)

        print("✅ Scraping complete. Saved to tds_data.json")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_tds_toc()




