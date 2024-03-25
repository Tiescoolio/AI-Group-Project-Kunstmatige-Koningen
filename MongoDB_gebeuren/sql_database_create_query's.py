import psycopg2 as ps

hostname = "20.108.157.88"
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
                id  NOT NULL PRIMARY KEY,
                name VARCHAR(255),
                brand VARCHAR(100), 
                category VARCHAR(100),
                sub_category VARCHAR(100),
                sub_sub_category VARCHAR(100),
                sub_sub_sub_category VARCHAR(100),
                gender VARCHAR(50),
                target_audience VARCHAR(100),
                selling_price  int(10),
                mrsp  int(10),
                price_discount    int(10),
                availability  int(10),
                aanbiedingen  VARCHAR(255),
                recommendable BOOLEAN
                )"""

profiles_tabel = """CREATE TABLE IF NOT EXISTS profiles (
                    id  NOT NULL PRIMARY KEY,
                    viewed_before_id FOREIGN KEY(viewed_before_id),
                    similars_id  FOREIGN KEY(similars_id),
                    ordered_id  FOREIGN KEY(ordered_id)
                    )"""


viewed_before_tabel = """CREATE TABLE IF NOT EXISTS viewed_before (
                    id  NOT NULL PRIMARY KEY
                    )"""

similars_tabel = """CREATE TABLE IF NOT EXISTS similars(
                    id  NOT NULL PRIMARY KEY
                    )"""

ordered_tabel = """CREATE TABLE IF NOT EXISTS ordered (
                    id  NOT NULL PRIMARY KEY)"""