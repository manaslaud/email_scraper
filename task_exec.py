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

    
def handleMeetCancellation(user_id,date='',t=''):
    try:
        time2_obj= datetime.strptime(t, "%I:%M%p") # 12-hour format with AM/PM
        normalized_time2=time2_obj.strftime("%H:%M")  # 24-hour format
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # Connect to the remote debugging port
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(6)
        driver.get("https://calendly.com/app/scheduled_events/user/me")
        # print(convertToET(date+' | '+t)) wrong day conversion, remove day from result
        time.sleep(6)
        
        #getting day list item tags
        divs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'div')))
        day_list_items_tags=[]
        map_day_and_items={}
        for div in divs:
            if div.get_attribute('data-component')=='day-list-item':
                day_list_items_tags.append(div)
                #finding elements inside day list items, header
                day=div.find_element(By.TAG_NAME,'h2').text.strip()
                dayWoYear=" ".join(day.split()[:-1]).strip()
                parts = dayWoYear.split(", ")  
                day_month = parts[1].split(" ") 
                formatted_date = f"{parts[0]}, {day_month[1]} {day_month[0]}"
                # print(formatted_date)
                #finding event list items of this day, time
                inside_day_list_items = div.find_elements(By.TAG_NAME,'div')
                event_list_items=[]
                for i in inside_day_list_items:
                    if i.get_attribute('data-component')=='event-list-item':
                        event_list_items.append(i)
                # print(event_list_items)
                map_day_and_items[formatted_date.split(", ")[1]]=event_list_items
        print(map_day_and_items)
        arrayToCheck=map_day_and_items[date.split(", ")[1]]
        elToClick=None
        for el in arrayToCheck:
            divs=el.find_elements(By.TAG_NAME,'div')
            for div in divs:
                if div.get_attribute('data-component')=='locked-time':
                    startTime=div.text.split(" ")[0]
                    time1_obj = datetime.strptime(startTime, "%I:%M%p")  # 12-hour format with AM/PM
                    normalized_time1 = time1_obj.strftime("%H:%M")  # 24-hour format
                    print(normalized_time1,normalized_time2)
                    if normalized_time1 == normalized_time2:
                        el.click()
                        buttons=el.find_elements(By.TAG_NAME,'button')
                        for button in buttons:
                            if button.get_attribute('aria-label')=='Cancel':
                                button.click()
                                handlePopupCancellationButton(driver)
        return True
    except Exception as e:
        print("Error occured during meet cancellation: ",{e})
        return False
    finally:
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
    if user_id=='' or date=='' or t=='':
        return False
    cancelResult=handleMeetCancellation(user_id,date,t)
    dbResult=handleDeletionFromDb(user_id)
    if not cancelResult or not dbResult:
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)
    user_id = sys.argv[1]
    date, t = fetch_user_schedule(user_id)
    if date and t:
        res=execute_task(user_id, date, t)
        if res: print('Successful')
        else: print('Error(s) detected while execution')
    else:
        print(f"Could not execute task for User ID: {user_id}")
