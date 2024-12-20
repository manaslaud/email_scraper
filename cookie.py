from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json,os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the remote debugging port


def saveCookies(driver):
    cookies = driver.get_cookies()
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    print('New Cookies saved successfully')

driver.get("https://calendly.com")
saveCookies(driver)