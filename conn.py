import psycopg2
from datetime import datetime, timedelta
import os
# from datetime import datetime

conn = psycopg2.connect(
    dbname="test_db", 
    user="postgres", 
    password="postgres", 
    host="localhost", 
    port="5432"
)

def parse_datetime(input_str):
    """
    Parse the string 'input_str' to datetime object.
    Preprocesses time string to ensure space between time and AM/PM.
    """
    input_str = input_str.replace('am', ' am').replace('pm', ' pm')    
    try:
        datetime_format = '%A, %B %d %I:%M %p'
        return datetime.strptime(input_str, datetime_format)
    except ValueError as e:
        print(f"Error parsing datetime: {e}")
        return None

def fetch_user_logs():
    """
    Fetch the user logs from the PostgreSQL database.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, username, date, time FROM user_logs")
        logs = cursor.fetchall()
    return logs

def schedule_cron_jobs():
    """
    Schedules cron jobs to run 15 minutes before the time value in the database.
    """
    logs = fetch_user_logs()
    
    for log in logs:
        user_id, username, date_str, time_str = log
        datetime_str = f"{date_str} {time_str}"
        parsed_datetime = parse_datetime(datetime_str)
        if parsed_datetime:
            job_time = parsed_datetime - timedelta(minutes=15)
            
            cron_time = job_time.strftime('%M %H %d %m *')
            print(f"Scheduling job for {username} at {cron_time} for task execution.")
            
            command = f"/usr/bin/python3 /home/manaslaud/Code/OneHash/email_scraper/task_exec.py {user_id} >> /home/manaslaud/Code/OneHash/email_scraper/cron_logs.log 2>&1" 
            cron_job = f"{cron_time} {command}"
            os.system(f"(crontab -l ; echo '{cron_job}') | crontab -")
            print(f"Cron job for {username} scheduled at {cron_time}")
        else:
            print(f"Invalid datetime format for {username}, skipping.")

if __name__ == "__main__":
    schedule_cron_jobs()
