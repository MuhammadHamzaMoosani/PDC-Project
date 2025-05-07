from selenium import webdriver  # To control the browser
from selenium.webdriver.common.by import By  # To find elements
from selenium.webdriver.chrome.service import Service  # To manage ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Auto-manage ChromeDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
# options.add_argument("--headless")   # Optional: run browser in the background
from datetime import datetime

now = datetime.now()
formatted_date = now.strftime("%B %d %Y")  # %B = full month name
array=formatted_date.split(" ")
if "0"==array[1][0]:
    array[1]=array[1][1]+","
    print("leading zero")
formatted_date = ' '.join(array)
print(formatted_date)
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.popups": 0,  # 0 = block
    "profile.default_content_setting_values.notifications": 2  # block notifications
})
driver = webdriver.Chrome(options=chrome_options)  # works if chromedriver is in PATH
driver.get("https://www.kayak.com/")
time.sleep(15)
try:
    dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "Uqct-title")))   
    dropdown.click()

    dropdown.click()
    onway = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="oneway"]')))
    onway.click()

    clear_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Remove value"]')))
    clear_btn.click()
    
    origin_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Flight origin input"]')))
    origin_input.send_keys("Jeddah")
    
    #could change below to get ul and then click first element 
    #can do for both orgin and destination 
    ul_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//ul[@id="flight-origin-smarty-input-list"]'))
)

# Now get all <li> children from the UL
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    print(li_elements)
# Click the first <li> (if it exists)
    if li_elements:
        li_elements[0].click()
    else:
        print("No list items found.")
    time.sleep(3)
    time.sleep(3)
    departure_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="Flight destination input"]')))
    departure_input.send_keys("Dubai")
    ul_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//ul[@id="flight-destination-smarty-input-list"]'))
)
    # Now get all <li> children from the UL
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    print(li_elements)
    # Click the first <li> (if it exists)
    if li_elements:
        li_elements[0].click()
    else:
        print("No list items found.")    
    wait = WebDriverWait(driver, 15)

    depart_date = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        f'//div[@role="button" and contains(@aria-label, "{formatted_date}")]'
    )))
    depart_date.click()
    button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Search"]')))
    button.click()

    original_window = driver.current_window_handle

    driver.switch_to.window(original_window)
    driver.close()

    # Now switch to the remaining open tab
    remaining_window = driver.window_handles[0]
    driver.switch_to.window(remaining_window)
    print("here")
    
    #result page 
     #div
     # 
    all_results=WebDriverWait(driver,120).until(
        EC.presence_of_all_elements_located((By.XPATH,'//div[@class="Fxw9-result-item-container"]'))
    )
    time.sleep(2)
    for result in all_results:
        try:
            print("Flight")

            # RELATIVE XPaths are still better for this context
            timeFlighttag = result.find_element(By.XPATH, './/div[@class="vmXl vmXl-mod-variant-large"]')
            timeFlight = timeFlighttag.find_element(By.TAG_NAME, 'span')

            price = result.find_element(By.XPATH, './/div[@class="e2GB-price-text"]')

            print("DTime: " + timeFlight.text)
            print("Price: " + price.text)

        except Exception as e:
            print("Skipping a result due to missing data or error:")
            continue
    text = all_results.text
    print(text)
    time.sleep(10000)
except:
    print("no found")
    

