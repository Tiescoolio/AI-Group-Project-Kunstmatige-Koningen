from pymongo import MongoClient

client = MongoClient()
products = client.huwebshop.products
cats = products.find({},["category","sub_category","sub_sub_category","sub_sub_sub_category"],1000)
index = {}
for cat in cats:
	try:
		if cat['category'] not in index and cat['category'] is not None:
			index[cat['category']] = {}
		if cat['sub_category'] not in index[cat['category']] and cat['sub_category'] is not None:
			index[cat['category']][cat['sub_category']] = {}
		if cat['sub_sub_category'] not in index[cat['category']][cat['sub_category']] and cat['sub_sub_category'] is not None:
			index[cat['category']][cat['sub_category']][cat['sub_sub_category']] = {}
		if cat['sub_sub_sub_category'] not in index[cat['category']][cat['sub_category']][cat['sub_sub_category']] and cat['sub_sub_sub_category'] is not None:
			index[cat['category']][cat['sub_category']][cat['sub_sub_category']][cat['sub_sub_sub_category']] = {}
	except:
		pass

indexloc = client.huwebshop.menuindex
indexid = indexloc.insert_one(index).inserted_id

print(index)

input()