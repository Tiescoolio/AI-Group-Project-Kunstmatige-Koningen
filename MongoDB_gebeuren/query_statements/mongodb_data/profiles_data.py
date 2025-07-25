from pymongo import MongoClient
import pandas
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', None)


def connect_to_mongo(host, port, db):
    conn = MongoClient(host,port)
    return conn[db]


# Functie die de data uit de mongoDB haalt
def get_mongo():
    collectie = "profiles"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id": 1, "order.ids":1, "recommendations.viewed_before":1, "recommendations.similars":1})
    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    final_showdown = []
    for index, row in data.iterrows():
        indices = []
        for i in row.values:
            if isinstance(i, dict):
                for j in i.values():
                    indices.append(j)
            else:
                indices.append(i)
        final_showdown.append(indices)
    for i in final_showdown:
        if len(i) == 3:
            i.append(None)
    return final_showdown


if __name__ == "__main__":
    get_mongo()

