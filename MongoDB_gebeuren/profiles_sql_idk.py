from IPython.display import display
from pymongo import MongoClient
import pandas

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
    collectie = "profiles"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id":1})

    #alfabetische volgorde
    print(cursor)
    data = pandas.DataFrame(list(cursor))
    return data

turn_mongo_to_sql()

