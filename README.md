# Calendly Scraper Project

This project is a basic web scraper built using Python and Selenium. It automates browser interactions and extracts avaiable usernames/ calendly profile URL's from a given seed phrase(intiail name).

## Approach
- Task: Scrape all possible avaiable usernames/ user links from Calendly.
- Issue: There is no publically avaiable API's that get all users.
- There are developer api's that return user details when given user uuid
- If user uuid is sequentially generated then possible to spam this api for every integer to get user details (but uid is not integer but a uuid string)
- Observing dashboard we have an option to choose our own username (used as a slug for generating dynamic URL'S for meet bookings)
- There is an internal api, for checking validity of a slug
  ```bash
  https://calendly.com/api/validators/slug 
  ```
- Upon some trial and error, can see that there is no rate limiter or at the very least rate limiter time frame is higher
- Automate the process of inputing usernames via Selenium, API spamming not possible as CORS enabled and requests only accepted via https://calendly.com
- If a username shows unavailable (error code 422) then it means it already exists and we have found a valid username / url
- Store it in an array
- Generate all possible usernames/slugs and check for unavailablity
- Map all the slugs to a valid URL
- 

## Features
- Automated browser interaction using Selenium.
- Handles dynamic content loading.
- Easily customizable for different websites.

## Requirements

Before running the scraper, ensure you have the following installed:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Selenium**: Install via pip:
  ```bash
  pip install selenium
  ```
- **ChromeDriver**: Download the version that matches your installed Chrome browser from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
  
  Ensure ChromeDriver is accessible via your system's `PATH` or specify the path in your script.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper
   ```

2. Install required dependencies:
   ```bash
   pip install selenium
   ```

3. Download and configure **ChromeDriver** or your preferred browser driver.

4. Update the **target URL** and the **scraping logic** inside the script (`scraper.py`) to match the site you want to scrape.

## Usage

Run the scraper by executing the following command:

```bash
python3 scraper.py
```

### Customization

- Modify the `scraper.py` file to target specific elements on the web page.
  - For example, to extract data from a `<div>` with a specific class, update the element selectors like this:
    ```python
    element = driver.find_element(By.CLASS_NAME, 'your-class-name')
    ```
- Adjust the waiting times for dynamic content loading:
    ```python
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'your-selector')))
    ```
