#_ID & ProductID





#RETURN = BUID & PRODUCTEN BIJ DIE BUID
#LIJST met [[BUID] - [ALLE producten]]
# Van alles dat has sale heeft
# ALs order null is weglaten anders lijst maken met alle producten die erin staan
# Producten aan buid linken

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

import time
import string
def get_mongo():
    collectie = "sessions"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"buid":1, "order.products":1})

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

    buid_list = []
    for i in templist:
        temp = []
        if i[2] is not None:
            #temptemp = string(i)i[]
            if len(i[1]) != 1:
                continue
            else:
                temp.append(i[1])

                temptest = []
                for j in i[2]:
                    if isinstance(j, dict):
                        for k in j.values():
                            temptest.append(k)
                    else:
                        temptest.append(j)
                temp.append(temptest)
                buid_list.append(temp)


    return buid_list

turn_mongo_to_sql()