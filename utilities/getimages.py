from pymongo import MongoClient
import csv

client = MongoClient()
products = client.huwebshop.products
imageurls = products.find({"images.0.0":{"$ne":None},"images.0.1":{"$ne":None}},["images"],0)
with open('imageurls.csv', mode='w', newline='') as imagelist:
	for url in imageurls:
		urlwriter = csv.writer(imagelist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		urlwriter.writerow([url['images'][0][0],url['images'][0][1]])
#	print(str(url))
input()