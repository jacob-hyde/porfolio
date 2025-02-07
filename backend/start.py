import subprocess
import sys
import time
import pymysql
import os
from init_db import init_db

def wait_for_db():
    max_retries = 30  # Wait up to 30 seconds
    retries = 0
    
    while retries < max_retries:
        try:
            print(f"Attempting to connect to database (attempt {retries + 1}/{max_retries})...")
            pymysql.connect(
                host=os.getenv('MYSQL_HOST', 'db'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', 'root'),
                database=os.getenv('MYSQL_DATABASE', 'portfolio_db')
            )
            print("Successfully connected to database!")
            return True
        except pymysql.Error as e:
            print(f"Database connection failed: {e}")
            retries += 1
            time.sleep(1)
    
    return False

def main():
    # Wait for database to be ready
    if not wait_for_db():
        print("Could not connect to database after maximum retries. Exiting.")
        sys.exit(1)
    
    # Initialize the database
    print("Initializing database...")
    init_db()
    
    # Start the Flask application
    print("Starting Flask application...")
    subprocess.run([sys.executable, "app.py"], check=True)

if __name__ == "__main__":
    main()
