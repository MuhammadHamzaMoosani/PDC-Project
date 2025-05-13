from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import json
from datetime import datetime

def scrape_kayak_flights(origin, destination):
    date = datetime.now()  # Current date and time
    formatted_day = str(date.day)
    formatted_date = date.strftime("%B") + f" {formatted_day}, {date.year}"
    

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.popups": 0,
        "profile.default_content_setting_values.notifications": 2
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.kayak.com/")

    flight_data = []

    try:
        original_window = driver.current_window_handle

        # Select one-way
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Uqct-title")))
        dropdown.click()
        dropdown.click()

        onway = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="oneway"]')))
        onway.click()

        # Clear origin field
        clear_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Remove value"]')))
        clear_btn.click()

        # Origin
        origin_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Flight origin input"]')))
        origin_input.send_keys(origin)

        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@id="flight-origin-smarty-input-list"]')))
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        if li_elements:
            li_elements[0].click()

        # Destination
        destination_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Flight destination input"]')))
        destination_input.send_keys(destination)

        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@id="flight-destination-smarty-input-list"]')))
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        if li_elements:
            li_elements[0].click()

        # Select Date
        depart_date = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//div[@role="button" and contains(@aria-label, "{formatted_date}")]')))
        depart_date.click()

        # Click search
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Search"]')))
        button.click()

        # Wait for possible tab switch
        print("🪟 Waiting for new tab or popup to open...")
        initial_windows = driver.window_handles

        try:
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > len(initial_windows))
            print("✅ New window opened.")
        except:
            print("⚠️ No new window opened — continuing in same tab.")

        if len(driver.window_handles) > len(initial_windows):
            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break
            driver.close()  # Close original
            driver.switch_to.window(driver.window_handles[0])
        else:
            driver.switch_to.window(original_window)

        # Extract results
        all_results = WebDriverWait(driver, 120).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Fxw9-result-item-container"]'))
        )

        for result in all_results:
            try:
                timeFlighttag = result.find_element(By.XPATH, './/div[@class="vmXl vmXl-mod-variant-large"]')
                timeFlight = timeFlighttag.find_element(By.TAG_NAME, 'span')
                price = result.find_element(By.XPATH, './/div[@class="e2GB-price-text"]')

                flight_data.append({
                    "Orgin":origin,
                    "Destination":destination,
                    "departure_time": timeFlight.text,
                    "price": price.text,
                    "date":formatted_date
                })

            except Exception:
                continue

    except Exception as e:
        print("Error occurred:", e)

    finally:
        driver.quit()

    # Save to JSON
    with open("kayak_flights.json", "w", encoding='utf-8') as f:
        json.dump(flight_data, f, indent=4)

    print("✅ Flight data saved to kayak_flights.json")

