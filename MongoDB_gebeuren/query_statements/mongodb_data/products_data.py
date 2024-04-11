import pandas
from pymongo import MongoClient


def connect_to_mongo(host, port, db):
    conn = MongoClient(host,port)
    return conn[db]


# geeft de producten terug die beschikbaar zijn als een lijst vol met diens _ids
def get_availability():
    collectie = "products"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id": 1, "properties.availability": 1})
    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    geen_naam_inspiratie = []
    for index, row in data.iterrows():
        test = row.values
        key = test[0]
        for i in row.values:
            if isinstance(i, dict):
                for j in i.values():
                    if int(j) > 0:
                        geen_naam_inspiratie.append(key)
    return geen_naam_inspiratie


# Functie die de data uit de mongoDB haalt
def get_mongo():
    collectie = "products"
    database = connect_to_mongo("localhost", 27017, "huwebshop")
    cursor = database[collectie].find({}, {"_id":1, "name":1, "category":1, "brand":1, "gender":1, "sub_category":1, "sub_sub_category":1, "sub_sub_sub_category":1, "properties.doelgroep":1, "price.selling_price":1,"price.mrsp":1, "price.price_discount":1, "properties.availability":1, "properties.discount":1, "recommendable":1})
    data = pandas.DataFrame(list(cursor))
    data = data.where(pandas.notnull(data), None)

    # Verwerkt de gegevens en geeft het terug in een uiterst bruikbaar format
    templist = []
    for index, row in data.iterrows():
        indices = []
        for i in row.values[:-1]:
            if isinstance(i, dict):
                for j in i.values():
                    indices.append(j)
            else:
                indices.append(i)
        if len(indices) == 13:
            templist.append(indices)
    products = []
    opties = get_availability()
    for i in templist:
        for j in opties:
            if i[0] == j:
                products.append(i)
    return products


if __name__ == '__main__':
    get_mongo()
