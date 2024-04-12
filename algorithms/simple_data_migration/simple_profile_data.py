from algorithms.utils import connect_to_db
import pymongo
import time


def insert_prof_data(data, cur) -> None:
    # Truncate existing data to avoid duplicate data
    cur.execute("""TRUNCATE TABLE public.profiles""")

    sql_query = """
    INSERT INTO products (id, brand, category, sub_category, sub_sub_category, aanbiedingen, recommendable)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    for num, prof in enumerate(data):
        keys = prof.keys()

        # Set discount to None to insert correct NULL value
        # Checks for some weird products.
        properties = prof.get("properties", {})
        if properties is None:
            discount = None
        else:
            discount = properties.get("discount")
            discount = None if discount == "none" else discount

        brand = prof["brand"] if "brand" in keys else None
        category = prof["category"] if "category" in keys else None
        sub_category = prof["sub_category"] if "sub_category" in keys else None
        sub_sub_category = prof["sub_sub_category"] if "sub_sub_category" in keys else None
        recommendable = prof["recommendable"] if "recommendable" in keys else None
        category = category[0] if type(category) == list else category

        # Init data
        query_data = (
            prof["_id"],
            brand,
            category,
            sub_category,
            sub_sub_category,
            discount,
            recommendable
        )
        print(num, query_data)
        # print(f"{category}, {sub_category}, {sub_sub_category}")
        cur.execute(sql_query, query_data)

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Get products data
    db = client["huwebshop"]
    col = db["profiles"]
    all_profiles = col.find()

    # Time the function
    start = time.time()

    with (connect_to_db() as conn, conn.cursor() as cursor):
        insert_prof_data(all_profiles, cursor)
    conn.commit()

    end = time.time()
    print(f"data transfer time = {end - start:.4f}s")  # Last time is 6.5784s, 6.8136s
