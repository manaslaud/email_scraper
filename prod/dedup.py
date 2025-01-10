import psycopg2
from datetime import datetime, timedelta
import os

# Database connection
conn = psycopg2.connect(
    dbname="test_db", 
    user="ec2-user", 
    password="one-hash", 
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
            job_time = parsed_datetime - timedelta(minutes=15)  # Adjust time 15 minutes before
            
            cron_time = job_time.strftime('%M %H %d %m *')  # Format the cron schedule time
            print(f"Scheduling job for {username} at {cron_time} for task execution.")
            
            # Specify the path of the Python script and log file
            command = f"/usr/bin/python3 /home/ec2-user/Bots/email_scraper/task_exec.py {user_id} >> /home/ec2-user/Bots/email_scraper/cron_logs.log 2>&1" 
            cron_job = f"{cron_time} ec2-user {command}"  # Using ec2-user as the user
            
            # Write to system-wide cron file under /etc/cron.d/
            cron_file_path = "/etc/cron.d/allcron"  # Filename as allcron
            with open(cron_file_path, 'a') as f:
                f.write(cron_job + '\n')
            print(f"Cron job for {username} scheduled at {cron_time}")
        else:
            print(f"Invalid datetime format for {username}, skipping.")

if __name__ == "__main__":
    schedule_cron_jobs()