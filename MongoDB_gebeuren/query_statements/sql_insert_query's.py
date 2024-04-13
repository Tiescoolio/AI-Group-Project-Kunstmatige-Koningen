from mongodb_data.products_data import get_mongo
from mongodb_data.profiles_data import get_mongo as profiles_data
from mongodb_data.sessions_products_data import get_mongo as sessions_products_data
from algorithms.utils import connect_to_db as connect

def data_transfer():
    print("begin van mongodb overzet")

    # data transfer from previously made functions, that pull data from mongodb
    products, profielen, sessie_products = get_mongo(), profiles_data(), sessions_products_data()

    # product filtering because mongodb has alphabetic filtering
    if products:
        for product in products:
            product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], \
            product[9], product[10], product[11], product[12] \
                = product[0], product[4], product[1], product[2], product[11], product[12], product[3], product[9], \
            product[6], product[5], product[7], product[8], product[10]

    return products, profielen, sessie_products

def products(products, cur):
    products_insert_query = """INSERT INTO products (id, name, brand, category, sub_category, sub_sub_category, gender, target_audience, selling_price, mrsp, price_discount, aanbiedingen, recommendable)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for product in products:
        cur.execute(products_insert_query, product)


def profiles(profiles, cur):
    profiles_insert_query = """INSERT INTO profiles (id) VALUES (%s)"""
    for profile in profiles:
        profile_id = str(profile[0])
        cur.execute(profiles_insert_query, [profile_id])


def sessions(profiles, cur):
    ordered_insert_query = """INSERT INTO sessions (buid, profile_id) VALUES (%s, %s)"""
    for profile in profiles:
        if profile[1] == None:
            continue
        else:
            profile_id = str(profile[0])
            for buid in profile[1]:
                cur.execute(ordered_insert_query, [buid, profile_id])


def similar(profiles, cur):
    similar_insert_query = """INSERT INTO similars (id, profile_id) VALUES (%s, %s)"""
    for profile in profiles:
        if profile[2] == None:
            continue
        else:
            profile_id = str(profile[0])
            for similar_id in profile[2]:
                cur.execute(similar_insert_query, [similar_id, profile_id])


def viewed_before(profiles, cur):
    viewed_before_insert_query = """INSERT INTO viewed_before (id, profile_id) VALUES (%s, %s)"""
    for profile in profiles:
        if profile[3] == None:
            continue
        else:
            profile_id = str(profile[0])
            for viewed_id in profile[3]:
                cur.execute(viewed_before_insert_query, [viewed_id, profile_id])


def session_products(sessie_producten, cur):
    sessions_products_insert = """INSERT INTO sessions_products (sessions_buid, id) VALUES (%s, %s)"""
    for session in sessie_producten:
        if session[1] == None:
            continue
        elif session[0] == None:
            continue
        else:
            for product in session[1]:
                cur.execute(sessions_products_insert, [session[0][0], product])


def main():
    con = connect()
    cur = con.cursor()

    products, profielen, sessie_products = data_transfer()
    print("begin data insert")

    products(products, cur)
    print("geexecute producten")

    profiles(profielen, cur)
    print("geexecute profielen")

    viewed_before(profielen, cur)
    print("geexecute viewed_before")

    similar(profielen, cur)
    print("Geexecute similar")

    sessions(profielen, cur)
    print("Geexecute sessions")

    session_products(sessie_products, cur)
    print("geexecute sessions_products")

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
