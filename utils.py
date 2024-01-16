import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

DB_URL = "postgresql://" + username + ":" + password + "@localhost:5432/postgres"