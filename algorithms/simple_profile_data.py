import pprint

from algorithms.utils import connect_to_db
import pymongo
import time


def insert_prof_data(data, cur, conn) -> None:
    # Truncate existing data to avoid duplicate data
    # cur.execute("""TRUNCATE TABLE public.profiles""")

    sql_query_profile = """
    INSERT INTO profiles (id)
    VALUES (%s);
    """


    count = 0
    for num, prof in enumerate(data):
        keys = prof.keys()
        if "recommendations" and "order" not in keys:
            continue
        count += 1

        print(count, keys)
        # Set discount to None to insert correct NULL value
        # Checks for some weird products.
        prof_id = str(prof["_id"])
        # cur.execute("""INSERT INTO profiles (id) VALUES (%s)""", prof_id)

        order = prof.get("order", {})
        if order:
            ids = order.get("ids")
            # print(ids, order)

        prev_rec = prof["previously_recommended"] if "previously_recommended" in keys else None

        # category = prof["category"] if "category" in keys else None
        # sub_category = prof["sub_category"] if "sub_category" in keys else None
        # sub_sub_category = prof["sub_sub_category"] if "sub_sub_category" in keys else None
        # recommendable = prof["recommendable"] if "recommendable" in keys else None
        # category = category[0] if type(category) == list else category

        # Init data

        # print(num, query_data)
        # print(f"{category}, {sub_category}, {sub_sub_category}")
        # cur.execute(sql_query, query_data)
        if count % 10**6 == 0:
            conn.commit()


if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Get products data
    db = client["huwebshop"]
    col = db["profiles"]
    all_profiles = col.find()

    # Time the function
    start = time.time()

    with (connect_to_db() as conn, conn.cursor() as cursor):
        insert_prof_data(all_profiles, cursor, conn)
    # conn.commit()

    end = time.time()
    print(f"data transfer time = {end - start:.4f}s")  # Last time is 6.5784s, 6.8136s
    # Time for all looping all elements = 34.5722s, amount of profiles = 2_081_649
    # Time for skipping useles data = 33.1787s, amount of profiles = 2_017_935
    # Time for skipping all useles data = 17.6500s, amount of profiles = 102_712