from pymongo import MongoClient

client = MongoClient()
products = client.huwebshop.products
noimgproductcount = products.count_documents({'images':{'$size':0}})
print(noimgproductcount)
input()