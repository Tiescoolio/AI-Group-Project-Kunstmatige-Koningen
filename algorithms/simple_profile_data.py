import pprint

from algorithms.utils import connect_to_db
import pymongo
import time


def insert_prof_data(data, cur, conn) -> None:
    # Truncate existing data to avoid duplicate data
    cur.execute("TRUNCATE TABLE ordered, viewed_before, similars, profiles")

    viewed_count = 0
    ordered_count = 0

    count = 0
    for num, prof in enumerate(data):
        keys = prof.keys()
        if "recommendations" and "order" not in keys:
            continue
        count += 1
        # print(count, keys)

        prof_id = str(prof["_id"])
        cur.execute("INSERT INTO profiles (id) VALUES (%s)", (prof_id,))

        order = prof.get("order")
        if order:
            ids = order.get("ids")
            if ids is None:
                continue

            # Send each individual product to a table with a foreign to the profile.
            for p_id in ids:
                if "dd:20" in p_id:
                    continue
                else:
                    cur.execute("""INSERT INTO ordered (id, profile_id) VALUES (%s, %s)""", (p_id, prof_id))
                    count += 1
                    ordered_count += 1

        rec = prof.get("recommendations", {})
        if rec:
            viewed = rec.get("viewed_before")
            if viewed is None:
                continue

            # Send each individual product viewed to a table with a foreign to the profile.
            for p_id in viewed:
                cur.execute("INSERT INTO viewed_before (id, profile_id) VALUES (%s, %s)", (p_id, prof_id))
                count += 1
                viewed_count += 1

        # Commit data every 10_000 elements to increase integrity.
        if count % 10**4 == 0:
            conn.commit()

    print(f"tab les created = {count}")
    print(f"products viewed = {viewed_count}")
    print(f"products ordered = {ordered_count}")


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
    print(f"data transfer time = {end - start:.4f}s")

    # Notation for this programs performance (ran on a beefy computer).
    # Time looping all elements = 34.5722s, amount of profiles left = 2_081_649
    # Time for skipping useless data = 33.1787s, amount of profiles left = 2_017_935
    # Time for skipping all useless data = 17.6500s, amount of profiles left = 102_712

    # Time for sending all data = 29.6744s,
    # Total tables created = 166_837
    # Total products viewed = 43_927
    # Total products ordered = 20_198
