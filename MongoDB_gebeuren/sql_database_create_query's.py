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

products_tabel = """CREATE TABLE IF NOT EXISTS products (
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(255),
                brand VARCHAR(100), 
                category VARCHAR(100),
                sub_category VARCHAR(100),
                sub_sub_category VARCHAR(100),
                sub_sub_sub_category VARCHAR(100),
                gender VARCHAR(50),
                target_audience VARCHAR(100),
                selling_price  INT,
                mrsp  INT,
                price_discount    INT,
                availability  INT,
                aanbiedingen  VARCHAR(255),
                recommendable BOOLEAN
                )"""


viewed_before_tabel = """CREATE TABLE IF NOT EXISTS viewed_before (
                    id INT NOT NULL PRIMARY KEY
                    )"""

similars_tabel = """CREATE TABLE IF NOT EXISTS similars(
                    id INT NOT NULL PRIMARY KEY
                    )"""

ordered_tabel = """CREATE TABLE IF NOT EXISTS ordered (
                    id INT NOT NULL PRIMARY KEY)"""

profiles_tabel = """CREATE TABLE IF NOT EXISTS profiles (
                    id INT NOT NULL PRIMARY KEY,
                    viewed_before_id INT,
                    FOREIGN KEY(viewed_before_id) REFERENCES viewed_before(id),
                    similars_id INT, 
                    FOREIGN KEY(similars_id) REFERENCES similars(id),
                    ordered_id INT,
                    FOREIGN KEY(ordered_id) REFERENCES ordered(id)
                    )"""

cur.execute(products_tabel)
cur.execute(similars_tabel)
cur.execute(viewed_before_tabel)
cur.execute(ordered_tabel)
cur.execute(profiles_tabel)
con.commit()
con.close()