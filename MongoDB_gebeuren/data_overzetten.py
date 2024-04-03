from IPython.display import display
import pandas
from pymongo import MongoClient



pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)

def connect_to_mongo(host, port, db):
    conn = MongoClient(host,port)
    return conn[db]

def turn_mongo_to_sql():
    data = get_mongo()
    display(data)

def get_mongo():
    collectie = "products"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id":1, "name":1, "category":1, "brand":1, "gender":1, "sub_category":1, "sub_sub_category":1, "sub_sub_sub_category":1, "properties.doelgroep":1, "price.selling_price":1,"price.mrsp":1, "price.price_discount":1, "properties.availability":1, "properties.discount":1, "recommendable":1})

    #alfabetische volgorde
    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    #Zorg ervoor dat de dictionaries uit de lijst worden gehaald en alleen de values overblijven en zorgt ervoor dat de juiste data overblijft
    templist = []
    for index, row in data.iterrows():
        indices = []
        #print(len(row.values))
        for i in row.values[:-1]:
            if isinstance(i, dict):
                for j in i.values():
                    indices.append(j)
            else:
                indices.append(i)
        if len(indices) == 13:
            templist.append(indices)
    return templist
turn_mongo_to_sql()



#--------------------------------------------
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

def sql_insert():
    data = get_mongo()
    to_add = """INSERT INTO products (id, name, brand, category, sub_category, sub_sub_category, sub_sub_sub_category, target_audience, selling_price, mrsp, price_discount, availability, aanbiedingen, recommendable)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for i in data:
        print(i)
        #cur.execute(to_add, i)
        #con.commit()
