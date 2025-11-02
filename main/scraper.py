import re, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def extract_number(text):
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None

def scrape_alibaba_flights(origin_code, dest_code, depart_date, return_date=None, headless=False):
    print(f"🟢 Launching scraper for {origin_code} → {dest_code} on {depart_date}")
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    results = []

    try:
        url = f"https://www.alibaba.ir/flights/{origin_code}-{dest_code}?adult=1&child=0&infant=0&departing={depart_date}"
        if return_date:
            url += f"&returning={return_date}"

        print("🌐 URL:", url)
        driver.get(url)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']//section")))
        time.sleep(5)

        parent_xpath = "//*[@id='app']//section//div[4]/div"
        blocks = driver.find_elements(By.XPATH, parent_xpath)
        print(f"✈️ Found {len(blocks)} blocks")

        for i in range(1, len(blocks) + 1):
            try:
                bx = f"({parent_xpath})[{i}]"
                dep_time = driver.find_element(By.XPATH, bx + "//div/div/div[1]/div/div[2]/div[2]/div[1]").text.strip()

                try:
                    price_text = driver.find_element(
                        By.XPATH, bx + "//div/div[2]/div[1]/div/span/strong"
                    ).text.strip()
                    price_value = extract_number(price_text)
                    is_full = False
                except:
                    price_text = "تکمیل ظرفیت 💸"
                    price_value = float("inf")
                    is_full = True

                results.append({
                    "dep_time": dep_time,
                    "price_text": price_text,
                    "price_value": price_value,
                    "is_full": is_full,
                })

                print(f"{i}. ✅ {dep_time} | {price_text}")
                time.sleep(0.2)

            except Exception as e:
                print(f"{i}. ⚠️ {e}")
                continue

        results.sort(key=lambda x: (x["is_full"], x["price_value"], x["dep_time"]))
        return results

    except Exception as e:
        print("❌ Error:", e)
        return []
    finally:
        driver.quit()
