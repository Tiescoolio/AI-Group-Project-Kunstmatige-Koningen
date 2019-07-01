# huw_utilities - a collection of various functions used 
import urllib.parse

def createcategoryindex(client):
	cats = client.huwebshop.products.find({},["category","sub_category","sub_sub_category","sub_sub_sub_category"])
	index = {}
	for cat in cats:
		try:
			c = [cat["category"]]
			if c[0] not in index and c[0] is not None:
				index[c[0]] = {}
			c.append(cat["sub_category"])
			if c[1] not in index[c[0]] and c[1] is not None:
				index[c[0]][c[1]] = {}
			c.append(cat["sub_sub_category"])
			if c[2] not in index[c[0]][c[1]] and c[2] is not None:
				index[c[0]][c[1]][c[2]] = {}
			c.append(cat["sub_sub_sub_category"])
			if c[3] not in index[c[0]][c[1]][c[2]] and c[3] is not None:
				index[c[0]][c[1]][c[2]][c[3]] = {}
		except:
			pass
	print(index)
	for key, value in index.items():
		index[key] = recursecatindex(client, key, value)
	indexloc = client.huwebshop.categoryindex
	indexid = indexloc.insert_one(index).inserted_id

def recursecatindex(client, key, value, level=0):
	levels = ["category","sub_category","sub_sub_category","sub_sub_sub_category"]
	if isinstance(value, dict):
		for k2, v2 in value.items():
			value[k2] = recursecatindex(client, k2, v2, level+1)
	if key[0:1] != "_":
		value['_count'] = client.huwebshop.products.count_documents({levels[level]:key})
	return value

def dictflatten(dictionary, sumlist=[]):
	for key, value in dictionary.items():
		sumlist.append(key)
		if isinstance(value, dict) and value:
			sumlist = dictflatten(value, sumlist)
	return sumlist

def categoryencode(cat):
	cat = cat.lower()
	cat = cat.replace(" ","-")
	cat = cat.replace(",","")
	cat = cat.replace("'","")
	cat = cat.replace("&","en")
	cat = cat.replace("ë","e")
	cat = cat.replace("=","-is-")
	cat = cat.replace("%","-procent-")
	cat = cat.replace("--","-")
	cat = urllib.parse.quote(cat)
	return cat