#_ID & ProductID

from IPython.display import display
from pymongo import MongoClient
import pandas

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)

def connect_to_mongo(host, port, db):
    conn = MongoClient(host, port)
    return conn[db]

def turn_mongo_to_sql():
    data = get_mongo()
    display(data)

def get_mongo():
    collectie = "sessions"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id":1, "has_sale":1, "order.products":1})
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
        if i[1] == True:
            if i[2] is None:
                temp = [i[0], [None]]
                print(temp)
            else:
                temp2 = []
                for j in i[2]:
                    if isinstance(j, dict):
                        for k in j.values():
                            temp2.append(k)
                    else:
                        temp2.append(j)
                temp.append(temp2)
                temp = [i[0], temp2]
            sessions.append(temp)
    return sessions

turn_mongo_to_sql()