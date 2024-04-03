import psycopg2 as ps

hostname = "localhost"
database = "Group_Project_AI_2024_C"
username = "postgres"
pwd = "pgadmin"
port_id = 5434
#variabelen aanmaken om makkelijker in een keer pycharm te verbinden met postgres
con = ps.connect(
    host = hostname,
    dbname = database,
    user = username,
    password= pwd,
    port = port_id)



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

with open("../create_queries/ordered_query.sql") as f:
    ordered_tabel = f.read()


cur.execute(products_tabel)
cur.execute(profiles_tabel)
cur.execute(similars_tabel)
cur.execute(viewed_before_tabel)
cur.execute(ordered_tabel)

con.commit()
con.close()