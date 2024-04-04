import psycopg2
import os
from dotenv import load_dotenv


def connect_to_db():
    # Prompting for the database password
    load_dotenv()

    try:
        # db_password = input("DB password: ")

        # Establishing a connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=os.getenv("db_host"),
            database=os.getenv("db_name"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password")
        )
        return connection
    except psycopg2.OperationalError as error:
        print("Error:", str(error))
        print("Invalid database connection data")