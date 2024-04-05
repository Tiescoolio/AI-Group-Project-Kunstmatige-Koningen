from algorithms.utils import connect_to_db
import pymongo
import time


def insert_prod_data(data, cur) -> None:
    # Truncate existing data to avoid duplicate data
    cur.execute("""TRUNCATE TABLE public.products""")

    sql_query = """
    INSERT INTO products (id, brand, category, sub_category, sub_sub_category, aanbiedingen, recommendable)
    VALUES (%s, %s, LOWER(%s), LOWER(%s), LOWER(%s), %s, %s);
    """
    freq_fastm = {}
    for num, prod in enumerate(data):
        keys = prod.keys()

        # Set discount to None to insert correct NULL value
        # Checks for some weird products.
        properties = prod.get("properties", {})
        if properties is None:
            discount = None
        else:
            discount = properties.get("discount")
            discount = None if discount == "none" else discount

        brand = prod["brand"] if "brand" in keys else None
        category = prod["category"] if "category" in keys else None
        sub_category = prod["sub_category"] if "sub_category" in keys else None
        sub_sub_category = prod["sub_sub_category"] if "sub_sub_category" in keys else None
        recommendable = prod["recommendable"] if "recommendable" in keys else None
        category = category[0] if type(category) == list else category

        # Init data
        query_data = (
            prod["_id"],
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
    col = db["products"]
    all_products = col.find()

    # Time the function
    start = time.time()

    with (connect_to_db() as conn, conn.cursor() as cursor):
        insert_prod_data(all_products, cursor)
    conn.commit()

    end = time.time()
    print(f"data transfer time = {end - start:.4f}s")  # Last time is 6.5784s, 6.8136s
