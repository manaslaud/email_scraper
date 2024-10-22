from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize ChromeDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/home/manaslaud/.config/google-chrome/")  # Path to User Data directory
chrome_options.add_argument("profile-directory=Default")  
chrome_options.add_argument("--no-sandbox")  # Overcome OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration

service = Service('/usr/bin/chromedriver')  # Update this path if necessary
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Print a message indicating the browser is opening
    print("Opening browser...")
    driver.get('https://calendly.com/app/personal/link')
    print("Navigated to the URL.")

    # List of slugs (usernames) to check
    slugs = ['slug1', 'slug2', 'slug3']  # Add your slugs here

    for slug in slugs:
        try:
            # Wait for the input field to be present
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'slug'))
            )

            # Clear the input field and enter the new slug
            input_field.clear()
            input_field.send_keys(slug)

            # Optionally trigger a change event with JavaScript (if needed)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", input_field)

            # Wait for a moment to allow the API response to update the DOM
            time.sleep(2)  # Adjust the time as necessary

            # Locate the span to get the status message
            status_span = driver.find_element(By.CSS_SELECTOR, '[data-component="slug-status"] span')
            status_text = status_span.text
            
            # Check the status and store if it's "unavailable"
            if status_text.lower() == "unavailable":
                print(f"The slug '{slug}' is unavailable.")

        except Exception as e:
            print(f"An error occurred for slug {slug}: {e}")

finally:
    driver.quit()  # Close the browser when done
