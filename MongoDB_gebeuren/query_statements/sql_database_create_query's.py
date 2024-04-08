import psycopg2 as ps

hostname = "localhost"
database = ""
username = "postgres"
pwd = ""
port_id =
#variabelen aanmaken om makkelijker in een keer pycharm te verbinden met postgres
con = ps.connect(
    host = hostname,
    dbname = database,
    user = username,
    password= pwd,
    port = port_id
    )



#dit verbind pycharm met postgres
cur = con.cursor()

with open("../create_queries/products_query.sql") as f:
    products_tabel = f.read()

with open("../create_queries/profiles_query.sql") as f:
    profiles_tabel = f.read()

with open("../create_queries/viewed_before_query.sql") as f:
    viewed_before_tabel = f.read()

with open("../create_queries/similars_query.sql") as f:
    similars_tabel = f.read()

with open("../create_queries/sessions_query.sql") as f:
    sessions_tabel = f.read()

with open("../create_queries/sessions_products_query.sql") as f:
    sesssions_producten_tabel = f.read()


cur.execute(products_tabel)
cur.execute(profiles_tabel)
cur.execute(similars_tabel)
cur.execute(viewed_before_tabel)
cur.execute(sessions_tabel)
cur.execute(sesssions_producten_tabel)

con.commit()
con.close()