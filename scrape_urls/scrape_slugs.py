import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from fake_useragent import UserAgent


proxy_host='p.webshare.io'
proxy_port='80'
proxy_user='eonyyvfy-rotate'
proxy_pass='oho63b4b5ysn'
proxy_url=f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
ua=UserAgent()

def extract_calendly_url(text):
    regex = r'calendly\.com/[A-Za-z0-9]+'
    matches = re.findall(regex, text)
    return matches

def startChromeDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(f'user-agent={ua.random}')
    chrome_options.add_argument(f'--proxy-server={proxy_url}')

    service = Service('/usr/bin/chromedriver')  
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def checkContactsModal(driver, wait):
    try:
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='top-card-text-details-contact-info']"))
        )
        if element:
            element.click()
            time.sleep(2)
            modal = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='artdeco-modal-outlet']/div[1]"))
            )
            urls = extract_calendly_url(modal.text)
            return urls if urls else None
    except Exception as e:
        print("Error in checkContactsModal:", e)
    return None

def extractFromDiv(driver, wait):
    try:
        element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]'))
        )
        if element:
            urls = extract_calendly_url(element.text)
            return urls if urls else None
    except Exception as e:
        print("Error in extractFromDiv:", e)
    return None

def aboutSection(driver, wait):
    try:
        about_element = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[2]/div[3]/div/div/div/span[1]'))
        )
        if about_element:
            urls = extract_calendly_url(about_element.text)
            return urls if urls else None
    except Exception as e:
        print("Error in aboutSection:", e)
    return None

def read_excel_and_begin(file_path, sheet_name=0):
    driver = startChromeDriver()  
    wait = WebDriverWait(driver, 20)
    results = []

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0], header=None,skiprows=89)  
        for slug in df.iloc[:, 0]:  
            driver.get(slug)  
            print(f"Visiting: {slug}")  
            
            urls = aboutSection(driver, wait)
            if urls:
                print(f"URLs found in aboutSection: {urls}")
                results.append((slug, urls[0]))
                continue

            urls = checkContactsModal(driver, wait)
            if urls:
                print(f"URLs found in checkContactsModal: {urls}")
                results.append((slug, urls[0]))
                continue

            urls = extractFromDiv(driver, wait)
            if urls:
                print(f"URLs found in extractFromDiv: {urls}")
                results.append((slug, urls[0]))
                continue
            
            results.append((slug, "No URLs found"))
            time.sleep(3)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    # Write results to an Excel file
    # output_df = pd.DataFrame(results, columns=["URL", "Calendly URL"])
    # output_df.to_excel("result.xlsx", index=False)
    # print("Results written to result.xlsx")

file_path = 'res1.xlsx'  
read_excel_and_begin(file_path)
