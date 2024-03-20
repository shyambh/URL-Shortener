import os
import json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

con_config = json.loads(os.getenv("MYSQL_CONNECTION_STRING"))


print(con_config)


def connect():
    conn = mysql.connector.connect(**con_config)
    if conn.is_connected():
        print("Database connection is SUCCESSFUL")

    return conn


connect()
