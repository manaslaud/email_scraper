from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set Chrome options for headless mode (optional for debugging)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')  # Disable sandboxing if required
chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage

# Set the path to the chromedriver
service = Service("/usr/bin/chromedriver")  # Change this path as needed

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com")  # Open Google to test
    print(f"Page title: {driver.title}")  # Should print "Google"
    driver.quit()  # Close the browser
except Exception as e:
    print(f"An error occurred while launching the browser: {e}")
