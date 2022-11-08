from pymongo import MongoClient
from lib.utils import loadJson
from csv import reader

DEBUG = False

MONGO_USER = "root"
MONGO_PWD = "password"
MONGO_DATABASE = "parcoursVeloEpicurien"
MONGO_HOST = "localhost"

RESTAURANTS_JSON = "datasets/3_ready_restaurants_mongodb.json"
BIKE_ROUTES_JSON = "datasets/3_ready_bike_routes_mongodb.json"
COLLECTION_BIKE_ROUTES = "bikeRoutes"
COLLECTION_RESTAURANTS = "restaurants"


def getConnectionString():
    return f"mongodb://{MONGO_USER}:{MONGO_PWD}@{MONGO_HOST}:27017/{MONGO_DATABASE}?authSource=admin"


def getClient():
    print("Connect to", getConnectionString())
    return MongoClient(getConnectionString())
    

def getCollections(database):
    print("Get collections")
    return database[COLLECTION_BIKE_ROUTES], database[COLLECTION_RESTAURANTS]


def insertInto(collection, data):
    if not isinstance(data, list):
        raise Exception("Data to insert must be a list")
    print(f"Insert {len(data)} documents into collection")
    collection.insert_many(data)
    print(f"Collection has now {collection.count_documents({})} documents")


def main(truncate=False):
    client = getClient()
    db = client[MONGO_DATABASE]
    bikeRoutesCol = db[COLLECTION_BIKE_ROUTES]
    restaurantsCol = db[COLLECTION_RESTAURANTS]

    if truncate:
        print("Truncate collections")
        bikeRoutesCol.delete_many({})
        restaurantsCol.delete_many({})

    bikeRoutes = loadJson(BIKE_ROUTES_JSON)
    restaurants = loadJson(RESTAURANTS_JSON)

    insertInto(bikeRoutesCol, bikeRoutes)
    insertInto(restaurantsCol, restaurants)
