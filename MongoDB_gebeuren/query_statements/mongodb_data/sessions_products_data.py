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


# Functie die de data uit de mongoDB haalt
def get_mongo():
    collectie = "sessions"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"buid":1, "order.products":1})

    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    # Zorg ervoor dat de dictionaries uit de lijst worden gehaald en alleen de values overblijven en zorgt ervoor dat de data in de juiste format overblijft
    workable_list = []
    for index, row in data.iterrows():
        indices = []
        for i in row.values:
            if isinstance(i, dict):
                for j in i.values():
                    indices.append(j)
            else:
                indices.append(i)
        workable_list.append(indices)

    # Zorgt ervoor dat de juiste data overblijft
    final_list = []
    for i in workable_list:
        small_list = []
        if i[2] is not None:
            small_list.append(i[1])
            smaller_list = []
            for j in i[2]:
                if isinstance(j, dict):
                    for k in j.values():
                        smaller_list.append(k)
                else:
                    smaller_list.append(j)
            small_list.append(smaller_list)
            final_list.append(small_list)

    return final_list


turn_mongo_to_sql()
