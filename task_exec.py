import sys
from datetime import datetime
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import pytz
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException

CANCELLATION_TEXT="""
Hey there!  

Apologies in advance if this annoys you —but like every other startup, we're always trying to optimize our marketing with some growth hacks. Just wanted to let you know that *Cal ID—a better alternative to Calendly—exists, and you can do so much more with it, all at **no cost*!  

To save your time, we're canceling this meeting, but we'd absolutely love to onboard you or give you a quick demo. If you're interested, you can schedule a call with our cofounder here: [cal.id/manas](https://cal.id/manas)  

Cheers! 
"""

# Database config
DB_HOST = "localhost"
DB_NAME = "test_db"  
DB_USER = "postgres"      
DB_PASSWORD = "postgres"   
DB_PORT = "5432"  

proxy_host='p.wenshare.io'
proxy_port='80'
proxy_user='eonyyvfy-rotate'
proxy_pass='oho63b4b5ysn'

def convertToET(ist_time_str):
    # ist_time_str = "Wednesday, December 18 | 7:30pm"
    ist_format = "%A, %B %d | %I:%M%p"  

    # Parse the IST time
    ist_time = datetime.strptime(ist_time_str, ist_format)

    ist_timezone = pytz.timezone("Asia/Kolkata")
    et_timezone = pytz.timezone("US/Eastern")

    # Localize the naive IST time to IST timezone (IST does not have DST, but we need to localize it)
    ist_time = ist_timezone.localize(ist_time)

    # Convert the IST time to ET (taking DST into account)
    et_time = ist_time.astimezone(et_timezone)

    # Add 19 minutes to the converted ET time
    et_time_plus_19min = et_time + timedelta(minutes=19)

    # Format and print the final ET time
    output = et_time_plus_19min.strftime("%A, %B %d | %I:%M%p")
    return output


def connect_to_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)
        
        
def handleDeletionFromDb(user_id):
    connection = None
    try:
        connection = connect_to_db()  
        with connection.cursor() as cursor:
            delete_query = "DELETE FROM user_logs WHERE id = %s"
            cursor.execute(delete_query, (user_id,))
            connection.commit()
            print(f"User with ID {user_id} deleted successfully.")
            return True
    except (psycopg2.DatabaseError, psycopg2.Error) as e:
        print(f"Error deleting user with ID {user_id}: {e}")
        if connection:
            connection.rollback()  
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        if connection:
            connection.close() 


def handleMeetCancellation(user_id, date='', t='', slug=''):
    proxy_url=f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}'
    if(date=='' or time=='' or slug==''):
        raise Exception('Date/Time/Slug does not exist')
    if(user_id==''):
        raise Exception('User id does not exist')
    try:
        chrome_options = Options()
        ua = UserAgent()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f'--proxy-server={proxy_url}')
        driver = webdriver.Chrome(options=chrome_options)
        chrome_options.add_argument(f'user-agent={ua.random}') 
        driver.get(f"https://calendly.com/cancellations/{slug}")
        
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            cookie_button.click()
            print("Cookie consent dismissed")
        except TimeoutException:
            print("No cookie consent popup detected")

        time.sleep(10)
        textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'textarea'))
        )[0]
        textarea.send_keys(CANCELLATION_TEXT)
        
        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
        )
        
        while len(buttons) <= 5:
            buttons = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
            )
        
        for button in buttons:
            if button.text == 'Cancel Event' and button.get_attribute('type')=='submit':
                driver.execute_script("arguments[0].scrollIntoView();", button)
                
                driver.execute_script("document.getElementById('onetrust-policy-text').style.display = 'none';")
                
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                time.sleep(6)
                button.click()
                print('Clicked "Cancel Event" button')
                return True
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    finally:
        # Ensure driver quits to release resources
        if 'driver' in locals():
            time.sleep(6)
            driver.quit()
            


def handlePopupCancellationButton(driver):
    spans=driver.find_elements(By.TAG_NAME,'span')
    for span in spans:
        if span.text=='Yes, cancel':
            span.click()
    

#db stores time in IST, 
def fetch_user_schedule(user_id):
    """Fetch the schedule for the given user ID."""
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = "SELECT date, time, slug FROM user_logs WHERE id = %s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                date, time,slug = result
                print(f"Fetched schedule for User ID {user_id}: Date = {date}, Time = {time} Slug ={slug}" )
                return date, time, slug
            else:
                print(f"No schedule found for User ID {user_id}")
                return None, None, None
    finally:
        connection.close()

def execute_task(user_id, date, t, slug):
    if user_id=='' or date=='' or t=='' or slug == '':
        return False
    cancelResult=handleMeetCancellation(user_id,date,t,slug)
    if(cancelResult):
        dbResult=handleDeletionFromDb(user_id)
        if not cancelResult or not dbResult:
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)
    user_id = sys.argv[1]
    date, t,slug = fetch_user_schedule(user_id)
    if date and t:
        res=execute_task(user_id, date, t,slug)
        if res: print('Successful')
        else: print('Error(s) detected while execution')
    else:
        print(f"Could not execute task for User ID: {user_id}")
