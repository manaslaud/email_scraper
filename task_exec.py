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

# Database config
DB_HOST = "localhost"
DB_NAME = "test_db"  
DB_USER = "postgres"      
DB_PASSWORD = "postgres"   
DB_PORT = "5432"  

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

def handleMeetCancellation(user_id,date,t):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the remote debugging port
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://calendly.com")
    a_tags = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    for tag in a_tags:
        href = tag.get_attribute('data-calendly-label')
        if(href=='scheduled-events-link'):
            tag.click()
            break
    time.sleep(5.5)
    print(convertToET(date+' | '+t))
    time_slot_spans=[]
    span_tags = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))
    for span_tag in span_tags:
        if span_tag.get_attribute('data-component') == 'event-time':
            time_slot_spans.append(span_tag)
            print(span_tag.text)


    driver.quit()

#db stores time in IST, convert to ET (HANDLE DATE AND TIME)
def fetch_user_schedule(user_id):
    """Fetch the schedule for the given user ID."""
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            query = "SELECT date, time FROM user_logs WHERE id = %s;"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                date, time = result
                print(f"Fetched schedule for User ID {user_id}: Date = {date}, Time = {time}")
                return date, time
            else:
                print(f"No schedule found for User ID {user_id}")
                return None, None
    finally:
        connection.close()

def execute_task(user_id, date, t):
    # """Perform a simple task for the given user."""
    # print(f"Executing task for User ID: {user_id}")
    # print(f"Task scheduled for: {date} {time}")
    # print(f"Task executed at: {datetime.now()}")
    handleMeetCancellation(user_id,date,t)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]

    # Fetch schedule for the given user_id
    date, t = fetch_user_schedule(user_id)
    if date and t:
        execute_task(user_id, date, t)
    else:
        print(f"Could not execute task for User ID: {user_id}")
