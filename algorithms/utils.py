import psycopg2, time
import os
from dotenv import load_dotenv


def connect_to_db():
    """This function establishes a connection with the webshop database"""
    load_dotenv()
    try:
        # db_password = input("DB password: ")

        # Establishing a connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=os.getenv("db_host"),
            database=os.getenv("db_name"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            port=os.getenv("db_port")
        )
        return connection
    except psycopg2.OperationalError as error:
        print("Error:", str(error))
        print("Invalid database connection data")


def time_function(func, *args) -> tuple:
    start = time.perf_counter_ns()
    # Run function
    data = func(*args)
    end = time.perf_counter_ns()
    # Calc time in ms
    time_func = (end - start) / (1.0 * 10 ** 6)
    print(f"time for the given function = {time_func}ms")

    return data, time_func