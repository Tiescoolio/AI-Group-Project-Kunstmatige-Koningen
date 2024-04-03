import psycopg2 as ps

hostname = "localhost"
database = "AI Group Project"
username = "postgres"
pwd = ""
port_id = 5432
#variabelen aanmaken om makkelijker in een keer pycharm te verbinden met postgres
con = ps.connect(
    host = hostname,
    dbname = database,
    user = username,
    password= pwd,
    port = port_id)
#dit verbind pycharm met postgres
cur = con.cursor()

with open("queries/products_query.sql") as f:
    products_tabel = f.read()

with open("queries/profiles_query.sql") as f:
    profiles_tabel = f.read()

with open("queries/viewed_before_query.sql") as f:
    viewed_before_tabel = f.read()

with open("queries/similars_query.sql") as f:
    similars_tabel = f.read()

with open("queries/ordered_query.sql") as f:
    ordered_tabel = f.read()


cur.execute(products_tabel)
cur.execute(profiles_tabel)
cur.execute(similars_tabel)
cur.execute(viewed_before_tabel)
cur.execute(ordered_tabel)

con.commit()
con.close()