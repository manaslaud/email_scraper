from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def connect_to_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the remote debugging port

    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.example.com")

    print(driver.title)
    driver.quit()

if __name__ == "__main__":
    connect_to_chrome()
