import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")

print(mongo_client)

mongo_db = mongo_client['school']
print(mongo_db)

name = mongo_db['name']
print(name.find()[0])


