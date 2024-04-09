#we moeten de _id, has_sale en order.products(kunnen er meerdere of geen zijn) hebben
# BUID & _id (Waar er een sale is)

from IPython.display import display
from pymongo import MongoClient
import pandas
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)

def connect_to_mongo(host, port, db):
    conn = MongoClient(host,port)
    return conn[db]

def get_mongo():
    collectie = "sessions"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id":1, "has_sale":1, "buid": 1})
    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    templist = []
    for index, row in data.iterrows():
        indices = []
        for i in row.values:
            if isinstance(i, dict):
                for j in i.values():
                    indices.append(j)
            else:
                indices.append(i)
        templist.append(indices)

    sessions = []
    for i in templist:
        temp = []
        if i[2] == True:
            temp.append(i[0])
            temp.append(i[1])
            sessions.append(temp)
    return sessions

get_mongo()