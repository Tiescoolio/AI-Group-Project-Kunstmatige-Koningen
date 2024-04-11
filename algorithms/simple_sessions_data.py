from algorithms.utils import connect_to_db
import pymongo
import time


def insert_session_data(data, cur) -> None:
    # Truncate existing data to avoid duplicate data
    # cur.execute("""TRUNCATE TABLE public.profiles""")

    for num, prof in enumerate(data):
        keys = prof.keys()
        print(keys)
        # Set discount to None to insert correct NULL value
        # Checks for some weird products.
        
        # print(f"{category}, {sub_category}, {sub_sub_category}")
        # cur.execute(sql_query, query_data)


if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Get products data
    db = client["huwebshop"]
    col = db["sessions"]
    all_profiles = col.find()

    # Time the function
    start = time.time()

    with (connect_to_db() as conn, conn.cursor() as cursor):
        insert_session_data(all_profiles, cursor)
    # conn.commit()

    end = time.time()
    print(f"data transfer time = {end - start:.4f}s")  # Last time is 6.5784s, 6.8136s
