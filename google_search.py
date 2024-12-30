from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()  
# Perform Google search
query = 'site:linkedin.com/in/ "Book a Meet" OR "calendly.com/"'
driver.get("https://www.google.com")

try:
    accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
    accept_button.click()
except:
    pass 

search_box = driver.find_element(By.NAME, "q")  
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)  

time.sleep(2)

results = []

for page in range(3):  
    print(f"Extracting results from page {page + 1}...")

    time.sleep(2)
    
    elements = driver.find_elements(By.CSS_SELECTOR, "h3")
    
    for element in elements:
        parent_a_tag = element.find_element(By.XPATH, './parent::a')
        href = parent_a_tag.get_attribute("href")
        if href not in results:  
            results.append(href)
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        next_button = driver.find_element(By.XPATH, '//a[@id="pnnext"]')
        next_button.click()  
        time.sleep(2)  
    except Exception as e:
        print(f"No next page found or error: {e}")
        break  

driver.quit()

print("Extracted URLs:")
for result in results:
    print(result)