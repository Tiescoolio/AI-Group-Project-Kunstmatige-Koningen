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


orders_select = """SELECT id, COUNT(*) AS aantal
                    FROM ordered           
                    GROUP BY id
                    ORDER BY aantal DESC
                    limit 4"""
cur.execute(orders_select)
populairste = cur.fetchall()
print(populairste)