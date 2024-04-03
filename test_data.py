import pymongo
import pprint
import time
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["huwebshop"]

# Collection Name
col = db["sessions_modified"]

x = col.find_one()
pprint.pprint(x)

x2 = col.find()

count = 0
data_to_filter = []
start = time.time()


for data in x2:
    if count == 20_000:
        break

    for key in data:
        if len(key) > 1:
            print(key)
            pprint.pprint(data.get(key))

    data_to_filter.append(data)
    count += 1


end = time.time()
print(f"{count}\n{end - start}")

# pprint.pprint(data_to_filter)

