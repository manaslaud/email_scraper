import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def extract_calendly_url(text):
    # Regular expression to find calendly.com slugs
    regex = r'calendly\.com/[A-Za-z0-9]+'
    matches = re.findall(regex, text)
    return matches

def startChromeDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep the browser open after script finishes
    chrome_options.add_argument("--remote-debugging-port=9222")  # Connect to a running Chrome instance with this port
    service = Service('/usr/bin/chromedriver')  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def checkContactsModal(driver, wait):
    try:
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='top-card-text-details-contact-info']"))
        )
        if(element):
            element.click()
            time.sleep(2)
            modal = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='artdeco-modal-outlet']/div[1]")))
            urls=extract_calendly_url(modal.text)
            if(urls):
                print(urls)
            else:
                print('none')
            
        else: 
            raise Exception
        print("Element found:", element.get_attribute('href'))  
    except Exception as e:
        print("Error:", e)

def read_excel_and_begin(file_path, sheet_name=0):
    driver = startChromeDriver()  
    wait = WebDriverWait(driver, 20)  
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0], header=None)  
        for slug in df.iloc[:, 0]:  
            driver.get(slug)  
            
            print(f"Visiting: {slug}")  
            
            checkContactsModal(driver, wait)
            time.sleep(3)
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred (read_excel error): {e}")
        return None
    finally:
        driver.quit()  

file_path = 'urls.xlsx'  
read_excel_and_begin(file_path)
