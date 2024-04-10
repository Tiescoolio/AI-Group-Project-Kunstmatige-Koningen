from mongodb_data.products_data import get_mongo
from mongodb_data.profiles_data import get_mongo as profiles_data
from mongodb_data.sessions_id_data import get_mongo as sessions_id_data
from mongodb_data.session_products_data import get_mongo as sessions_products_data
from algorithms.utils import connect_to_db as connect


#data overzetten vanuit de gemaakte functies
# producten, profielen, sessies_ids, sessie_products = get_mongo(), profiles_data(), sessions_id_data(), sessions_products_data()
sessies_ids = sessions_id_data()
# sessie_products = sessions_products_data()
#producten op volgorde zetten op basis van de alfabetische volgorde van de mongodb info
# if producten:
#     for product in producten:
#         product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12] \
#         =  product[0], product[4], product[1], product[2], product[11], product[12], product[3], product[9], product[6], product[5], product[7], product[8], product[10]

#inloggen bij postgres

con = connect()
cur = con.cursor()


def products(producten):
    products_insert_query = """INSERT INTO products (id, name, brand, category, sub_category, sub_sub_category, gender, target_audience, selling_price, mrsp, price_discount, aanbiedingen, recommendable)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for product in producten:
        cur.execute(products_insert_query, product)


def profiles(profiles):
    profiles_insert_query = """INSERT INTO profiles (id) VALUES (%s)"""
    for profiel in profiles:
        profiel_id = str(profiel[0])
        cur.execute(profiles_insert_query, (profiel_id,))


def sessions(profiles):
    ordered_insert_query = """INSERT INTO sessions (buid, profile_id) VALUES (%s, %s)"""
    for profiel in profiles:
        if profiel[1] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for buid in profiel[1]:
                cur.execute(ordered_insert_query, [buid, profiel_id])


def similar(profiles):
    similar_insert_query = """INSERT INTO similars (id, profile_id) VALUES (%s, %s)"""
    for profiel in profiles:
        if profiel[2] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for vergelijkbare_id in profiel[2]:
                cur.execute(similar_insert_query, [vergelijkbare_id, profiel_id])


def viewed_before(profiles):
    viewed_before_insert_query = """INSERT INTO viewed_before (id, profile_id) VALUES (%s, %s)"""
    for profiel in profiles:
        if profiel[3] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for viewed_id in profiel[3]:
                cur.execute(viewed_before_insert_query, [viewed_id, profiel_id])



def session_products(sessie_producten):
    sessions_products_insert = """INSERT INTO sessions_products (sessions_buid, id) VALUES (%s, %s)"""
    for sessie in sessie_producten:
        if sessie[1] == None:
            continue
        else:
            for product in sessie[1]:
                cur.execute(sessions_products_insert, [sessie[0], product])


# products(producten)
# print("geexecute producten")

# profiles(profielen)
# print("geexecute profielen")

# viewed_before(profielen)
# print("geexecute viewed_before")
# similar(profielen)
# print("Geexecute similar")
# sessions(profielen)
# print("Geexecute sessions")

# session_products(sessie_products)
# print("geexecute sessions_products")

con.commit()
con.close()