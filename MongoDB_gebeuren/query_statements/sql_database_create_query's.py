from algorithms.utils import connect_to_db as connect

con = connect()
cur = con.cursor()

with open("../create_queries/products_query.sql") as f:
    products_table = f.read()

with open("../create_queries/profiles_query.sql") as f:
    profiles_table = f.read()

with open("../create_queries/viewed_before_query.sql") as f:
    viewed_before_table = f.read()

with open("../create_queries/similars_query.sql") as f:
    similars_table = f.read()

with open("../create_queries/sessions_query.sql") as f:
    sessions_table = f.read()

with open("../create_queries/sessions_products_query.sql") as f:
    sesssions_producten_table = f.read()


cur.execute(products_table)
cur.execute(profiles_table)
cur.execute(similars_table)
cur.execute(viewed_before_table)
cur.execute(sessions_table)
cur.execute(sesssions_producten_table)

con.commit()
con.close()