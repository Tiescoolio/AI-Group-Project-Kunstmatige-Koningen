import os
from dotenv import load_dotenv
from mongodb_data.products_data import get_mongo
from mongodb_data.products_data import get_mongo
import psycopg2 as ps
producten = get_mongo()
for product in producten:
    product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12] \
        =  product[0], product[4], product[1], product[2], product[11], product[12], product[3], product[9], product[6], product[5], product[7], product[8], product[10]

load_dotenv()

hostname = "localhost"
database = "hu_webshop"
username = "postgres"
pwd = os.getenv("db_password")
port_id = 5432
#variabelen aanmaken om makkelijker in een keer pycharm te verbinden met postgres
con = ps.connect(
    host = hostname,
    dbname = database,
    user = username,
    password= pwd,
    # port = port_id
)
cur = con.cursor()

def products():
    products_insert_query = """INSERT INTO products (id, name, brand, category, sub_category, sub_sub_category, gender, target_audience, selling_price, mrsp, price_discount, aanbiedingen, recommendable)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for product in producten:
        cur.execute(products_insert_query, product)

def profiles():
    profiles_insert_query = """INSERT INTO profiles (id) VALUES (%s)"""
    for profiel in profiles:
        cur.execute(profiles_insert_query, profiel[0])

def ordered():
    ordered_insert_query = """INSERT INTO ordered (id, profile_id) VALUES (%s, %s)"""
    ordered = []
    for profiel in profiles:
        for order_id in profiel[1]:
            ordered.append(profiel[0], order_id)
    for order in ordered:
        cur.execute(ordered_insert_query, order)

def similar():
    similar_insert_query = """INSERT INTO similars (id, profile_id) VALUES (%s, %s)"""
    vergelijkbaren = []
    for profiel in profiles:
        for vergelijkbare_id in profiel[2]:
            ordered.append(profiel[0], vergelijkbare_id)
    for vergelijkbare in vergelijkbaren:
        cur.execute(similar_insert_query, vergelijkbare)

def viewed_before():
    viewed_before_insert_query = """INSERT INTO viewed_before (id, profile_id) VALUES (%s, %s)"""
    viewed_before = []
    for profiel in profiles:
        for viewed_id in profiel[3]:
            ordered.append(profiel[0], viewed_id)
    for bekeken in viewed_before:
        cur.execute(viewed_before_insert_query, bekeken)

con.commit()
con.close()