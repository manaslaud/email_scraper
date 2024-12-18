import pandas as pd
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from chromedriver_py import binary_path # this will get you the path variable
from seleniumwire import webdriver
import psycopg2

USERNAME, PASSWORD = 'devdavda_ZW1ay', 'Devonehash+1'
SELECTED_DAY=None
SELECTED_TIME=None

def updateDB(username='',date='',time=''):
    conn = psycopg2.connect(
    dbname="test_db", 
    user="postgres", 
    password="postgres", 
    host="localhost", 
    port="5432"
)
    cur=conn.cursor()
    insert_query = """
    INSERT INTO user_logs (username, date, time) 
    VALUES (%s, %s, %s)
    """
    data=(username,date,time)
    try:
        cur.execute(insert_query, data)
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

def handle_next_page(driver,url='',date='',t=''):
    print('inside handle next page:' + date + t + url)
    username=url.split('.com/')[1]
    print(username)
    time.sleep(2.5)
    try:
        full_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'full_name'))
        )
        email_input = driver.find_element(By.NAME, 'email')

        full_name_input.send_keys('Dev')
        email_input.send_keys('davd3a@onehash.ai')

        actions = ActionChains(driver)
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        actions.move_to_element(submit_button).pause(1).click().perform()

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
        print(f"Form submission successful! New URL: {driver.current_url}")
        updateDB(username,date,t)
        
    except Exception as e:
        print(f"An error occurred on the new page: {e}")

def handle_time_selection(driver,url='',date=''):
    
    try:
        time.sleep(1)
        time_selection_div = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@data-component="spot-list"]'))
        )
        time_options = driver.find_elements(By.XPATH, '//*[@data-component="spot-list"]')
        if time_options:
            for time_option in time_options:
                buttons = time_option.find_elements(By.TAG_NAME, 'button')
                for button in buttons:
                    button.click()
                    print(f"Clicked button with Time Slot: {button.get_attribute('data-start-time')}")
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[text()="Next"]'))
                    )
                    print("Next button found!")
                    if next_button:
                        next_button_text = next_button.text
                        print(f"Clicking on the button with text: {next_button_text}")
                        val=button.get_attribute('data-start-time')
                        time.sleep(2)
                        next_button.click()
                        print("Clicked the Next button, moving to handle the next page.")
                        
                        handle_next_page(driver,url,date,val)
                        return
                    else:
                        print("Next button not found or not clickable.")
        else:
            print("No time options found.")
    except Exception as e:
        print(f"An error occurred while selecting time: {e}")

def get_all_a_tags_selenium(url, slug):

    proxies = {
        'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
        'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
        }

    sw_options = {
    'proxies': {
        'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
        'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
    }
}

    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxies}')
    chrome_options.add_experimental_option("detach", True)

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, seleniumwire_options=sw_options, options=chrome_options)

    try:
        driver.get(url)

        a_tags = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        time.sleep(1.2)
        for tag in a_tags:
            href = tag.get_attribute('href')
            if href and slug in href:
                driver.get(href)
                print('printing one of the <a> href links ',href)
                grid_cells = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@role="gridcell"]'))
                )
                # print(grid_cells)
                time.sleep(4)    
                for cell in grid_cells:
                    buttons = cell.find_elements(By.TAG_NAME, 'button')
                    for button in buttons:
                        # if not button.get_attribute('disabled'):
                        #     print(button.text)
                        #     button.click()
                        #     handle_time_selection(driver)
                        #     return
                        status=button.get_attribute('aria-label').split('-')[1].strip()
                        if status=='Times available':
                            print(button.get_attribute('aria-label').split('-')[0].strip())
                            button.click()
                            handle_time_selection(driver,url,button.get_attribute('aria-label').split('-')[0].strip())
                            return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def process_slug(slug):
    url = f"https://{slug}"
    r = requests.get(url)
    if r.status_code == 200:
        get_all_a_tags_selenium(url, slug)

def read_excel(file_path, sheet_name=0):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0], header=None)  
        
        for slug in df.iloc[:, 0]:  
            print(slug)  
            process_slug(slug)  
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred (read_excel error): {e}")
        return None

if __name__ == "__main__":
    file_path = "Calendly_data.xlsx"
    read_excel(file_path)