import sys
from datetime import datetime
import psycopg2

# Database config
DB_HOST = "localhost"
DB_NAME = "test_db"  
DB_USER = "postgres"      
DB_PASSWORD = "postgres"   
DB_PORT = "5432"  

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

def execute_task(user_id, date, time):
    """Perform a simple task for the given user."""
    print(f"Executing task for User ID: {user_id}")
    print(f"Task scheduled for: {date} {time}")
    print(f"Task executed at: {datetime.now()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]

    # Fetch schedule for the given user_id
    date, time = fetch_user_schedule(user_id)
    if date and time:
        execute_task(user_id, date, time)
    else:
        print(f"Could not execute task for User ID: {user_id}")
