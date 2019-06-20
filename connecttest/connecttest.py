from pymongo import MongoClient

# The client is the object that connects with the MongoDB database. This is used
# centrally throughout the code below.
# Whitelisting may as of yet be required for connecting to the MongoDB cluster.
client = MongoClient('mongodb+srv://accessUser:DifficultPassword@huwebshoptest-neick.mongodb.net/test?retryWrites=true&w=majority')
products = client.huwebshop.products
productcount = products.count_documents({})
print(str(productcount))