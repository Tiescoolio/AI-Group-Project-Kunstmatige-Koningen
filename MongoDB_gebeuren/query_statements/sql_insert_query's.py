from mongodb_data.products_data import get_mongo
import psycopg2 as ps
producten = get_mongo()
for product in producten:
    product[0], product[1], product[2], product[3], product[4], product[5], product[6], product[7], product[8], product[9], product[10], product[11], product[12] \
        =  product[0], product[4], product[1], product[2], product[11], product[12], product[3], product[9], product[6], product[5], product[7], product[8], product[10]


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
products_insert_query = """INSERT INTO products (id, name, brand, category, sub_category, sub_sub_category, gender, target_audience, selling_price, mrsp, price_discount, aanbiedingen, recommendable)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

for product in producten:
    cur.execute(products_insert_query, product)
con.commit()