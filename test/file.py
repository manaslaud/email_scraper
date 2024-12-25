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
from seleniumwire import webdriver
import psycopg2
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException

USERNAME, PASSWORD = 'devdavda_ZW1ay', 'Devonehash+1'
proxy_host='p.wenshare.io'
proxy_port='80'
proxy_user='eonyyvfy-rotate'
proxy_pass='oho63b4b5ysn'

SELECTED_DAY=None
SELECTED_TIME=None
BOOKING_TEXT="""
Hey there!
Just wanted to quickly catch up and show you how Cal ID by OneHash is miles ahead of Calendly. Plus, I'd love to invite you to migrate to Cal ID with all features, event types, calendars, notifications, workflows—literally everything—for FREE for 3 years!
It's a sleek, modern scheduling app with a stunning UI and seamless user experience. Trust me, you're going to love it!
Let me know when we can connect. 
"""
BOOKING_TEXT= BOOKING_TEXT.replace("\n", " ").strip()
BOOKING_TEXT_SMALL="""
I'd love to invite you to migrate to Cal ID with all features, event types, calendars, notifications, workflows—literally everything—for FREE for 3 years!
"""
BOOKING_TEXT_SMALL=BOOKING_TEXT_SMALL.replace("\n", " ").strip()


def tickAllRadioButtons(driver, timeout=10):
    try:
        # Wait until all radio buttons are present on the page
        radio_buttons = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='radio']"))
        )

        actions = ActionChains(driver)  # Initialize ActionChains

        for radio_button in radio_buttons:
            if 'question' not in radio_button.get_attribute('name'): continue  # Skip non-relevant radio buttons
            try:

                if radio_button.is_displayed() or radio_button.is_enabled():
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_button)

                        # Use ActionChains to click the radio button
                        if not radio_button.is_selected():
                            actions.move_to_element(radio_button).click().perform()
                            print(f"Radio button with name '{radio_button.get_attribute('name')}' was selected.")
                        else:
                            print(f"Radio button with name '{radio_button.get_attribute('name')}' is already selected.")
                    except ElementClickInterceptedException:
                        print(f"Radio button with name '{radio_button.get_attribute('name')}' is obstructed. Retrying.")
                        driver.execute_script("arguments[0].click();", radio_button)  # Force-click using JavaScript
                else:
                    print(f"Radio button with name '{radio_button.get_attribute('name')}' is not interactable.")
            
            except TimeoutException:
                print(f"Skipping a radio button with name '{radio_button.get_attribute('name')}' due to timeout.")
            except Exception as e:
                print(f"Error handling radio button: {e}")
    except TimeoutException:
        print(f"No radio buttons found within {timeout} seconds.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def tickAllCheckboxes(driver, timeout=10):
    try:
        checkboxes = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox']"))
        )

        actions = ActionChains(driver)  

        for checkbox in checkboxes:
            if 'question' not in checkbox.get_attribute('name'):continue
            try:

                if checkbox.is_displayed() or checkbox.is_enabled():
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                        if not checkbox.is_selected():
                            actions.move_to_element(checkbox).click().perform()
                            print(f"Checkbox with name '{checkbox.get_attribute('name')}' was ticked.")
                            break
                        else:
                            print(f"Checkbox with name '{checkbox.get_attribute('name')}' is already selected.")
                    except ElementClickInterceptedException:
                        print(f"Checkbox with name '{checkbox.get_attribute('name')}' is obstructed. Retrying.")
                        driver.execute_script("arguments[0].click();", checkbox)  # Force-click using JavaScript
                else:
                    print(f"Checkbox with name '{checkbox.get_attribute('name')}' is not interactable.")
            
            except TimeoutException:
                print(f"Skipping a checkbox with name '{checkbox.get_attribute('name')}' due to timeout.")
            except Exception as e:
                print(f"Error handling checkbox: {e}")
    except TimeoutException:
        print(f"No checkboxes found within {timeout} seconds.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def selectFromDropdown(driver, timeout=10):
    try:
        div_element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox' and @type='button']"))
        )
        div_element.click()

        div_element2 = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox' and @aria-label='Options']"))
        )
        buttons = div_element2.find_elements(By.XPATH, ".//button[@type='button' and @role='option']")

        if buttons:
            for button in buttons:
                try:
                    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(button))
                    button.click()
                    print("Button clicked.")
                    break  
                except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                    print(f"Could not click the button: {e}")
        else:
            print("No buttons found inside the div.")

    except TimeoutException:
        print("Timeout while waiting for the dropdown or buttons.")
    except NoSuchElementException:
        print("Element not found in the page.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def fillTextArea(driver, words=BOOKING_TEXT, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "textarea"))
        )

        textareas = driver.find_elements(By.TAG_NAME, "textarea")

        for textarea in textareas:
            try:
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable(textarea)
                )
                
                is_required = textarea.get_attribute("required")
                if is_required:
                    ActionChains(driver).move_to_element(textarea).perform()

                    textarea.clear()  # Clear any existing text
                    textarea.send_keys(words)
                    print(f"Filled required textarea with: '{words}'")
                else:
                    print("Skipping non-required textarea.")
            except TimeoutException:
                print("Skipping a textarea that is not interactable.")
            except Exception as e:
                print(f"Error handling a textarea: {e}")
    except TimeoutException:
        print(f"No textareas were found on the page within {timeout} seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def fillInputFields(driver, words=BOOKING_TEXT_SMALL, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
        )

        input_fields = driver.find_elements(By.TAG_NAME, "input")
        
        for input_field in input_fields:
            try:
                #checking if its a phone no field
                field_name = input_field.get_attribute("name")
                if(input_field.get_attribute('type')=='tel'):
                    input_field.clear()
                    input_field.send_keys("+91 8104978455")
                    continue
                    
                if field_name and "question_" in field_name:
                    # Ensure the input field is interactable
                    WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable(input_field)
                    )
                    ActionChains(driver).move_to_element(input_field).perform()

                    input_field.clear()
                    input_field.send_keys(words)
                    print(f"Filled input field '{field_name}' with: '{words}'")
                else:
                    print(f"Skipping input field with name: '{field_name}'")
            except TimeoutException:
                print("Skipping an input field that is not interactable.")
            except Exception as e:
                print(f"Error handling an input field: {e}")
    except TimeoutException:
        print(f"No input fields were found on the page within {timeout} seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")

def updateDB(username='',date='',time='',slug=''):
    conn = psycopg2.connect(
    dbname="test_db", 
    user="postgres", 
    password="postgres", 
    host="localhost", 
    port="5432"
)
    cur=conn.cursor()
    insert_query = """
    INSERT INTO user_logs (username, date, time, slug) 
    VALUES (%s, %s, %s, %s)
    """
    data=(username,date,time,slug)
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
        try:
            full_name_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, 'full_name'))
            )
            full_name_input.send_keys('Testing')
        except TimeoutException:
            #checking and sending first name 
            first_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'first_name')))
            first_name_input.clear()
            first_name_input.send_keys('first_name')
            #checking and sending last name
            last_name_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'last_name')))
            last_name_input.clear()
            last_name_input.send_keys('last_name')
            
        email_input = driver.find_element(By.NAME, 'email')
        email_input.send_keys('xyz@gmail.com')
        fillInputFields(driver)
        fillTextArea(driver)
        tickAllCheckboxes(driver)
        tickAllRadioButtons(driver)
        selectFromDropdown(driver)
        actions = ActionChains(driver)
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        actions.move_to_element(submit_button).pause(1).click().perform()

        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
        print(f"Form submission successful! New URL: {driver.current_url}")
        slug=driver.current_url.split("/")[-1].strip()
        updateDB(username,date,t,slug)
        
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
    proxy_url=f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    ua = UserAgent()
    chrome_options = Options()
    # chrome_options.add_argument(f'--proxy-server={proxy_url}')
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(f'user-agent={ua.random}')
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        a_tags = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        while(len(a_tags)<=3):
            a_tags = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))            
        for tag in a_tags:
            href = tag.get_attribute('href')
            print(href)
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
    
    
