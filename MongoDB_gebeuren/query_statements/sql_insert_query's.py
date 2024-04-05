from mongodb_data.products_data import get_mongo
from mongodb_data.profiles_data import get_mongo as profiles_data
import psycopg2 as ps
producten = get_mongo()
for product in producten:
    product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12] \
        =  product[0], product[4], product[1], product[2], product[11], product[12], product[3], product[9], product[6], product[5], product[7], product[8], product[10]
profielen = profiles_data()

hostname = "localhost"
database = "AI Group Project"
username = "postgres"
pwd = "Gymhond11"
port_id = 5432
#variabelen aanmaken om makkelijker in een keer pycharm te verbinden met postgres
con = ps.connect(
    host = hostname,
    dbname = database,
    user = username,
    password= pwd,
    port = port_id)
cur = con.cursor()

def products():
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
    sessions = []
    for profiel in profiles:
        if profiel[1] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for buid in profiel[1]:
                sessions.append([buid, profiel_id])
            for session in sessions:
                cur.execute(ordered_insert_query, session)

def similar(profiles):
    similar_insert_query = """INSERT INTO similars (id, profile_id) VALUES (%s, %s)"""
    vergelijkbaren = []
    for profiel in profiles:
        if profiel[2] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for vergelijkbare_id in profiel[2]:
                vergelijkbaren.append([vergelijkbare_id, profiel_id])
            for vergelijkbare in vergelijkbaren:
                cur.execute(similar_insert_query, vergelijkbare)

def viewed_before(profiles):
    viewed_before_insert_query = """INSERT INTO viewed_before (id, profile_id) VALUES (%s, %s)"""
    viewed_before = []
    for profiel in profiles:
        if profiel[3] == None:
            continue
        else:
            profiel_id = str(profiel[0])
            for viewed_id in profiel[3]:
                viewed_before.append([viewed_id, profiel_id])
            for bekeken in viewed_before:
                cur.execute(viewed_before_insert_query, bekeken)

def session_products(sessies):
    sessions_products_insert = """INSERT INTO sessions_products (sessions_buid, id) VALUES (%s, %s)"""
    sessions = []
    for sessie in sessies:
        if sessie[1] == None:
            continue
        else:
            for product in sessie[1]:
                sessions.append([sessie[0], product])
            for session in sessions:
                cur.execute(sessions_products_insert, session)

viewed_before(profielen)
con.commit()
con.close()