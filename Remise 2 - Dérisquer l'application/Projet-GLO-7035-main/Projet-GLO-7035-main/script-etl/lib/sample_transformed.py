from pymongo import MongoClient
from lib.utils import loadJson, writeFile
from bson.json_util import dumps

DEBUG = False

MONGO_USER = "root"
MONGO_PWD = "password"
MONGO_DATABASE = "parcoursVeloEpicurien"
CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PWD}@localhost:27017/{MONGO_DATABASE}?authSource=admin"

BIKE_ROUTES_JSON = "datasets/1_transformed_bike_routes.json"
RESTAURANTS_JSON = "datasets/1_transformed_restaurants.json"
SAMPLE_BIKE_ROUTES_JSON = "datasets/X_sample_transformed_bike_routes.json"
SAMPLE_RESTAURANTS_JSON = "datasets/X_sample_transformed_restaurants.json"
COLLECTION_BIKE_ROUTES = "bikeRoutesSample"
COLLECTION_RESTAURANTS = "restaurantsSample"

POINT = [-73.98858649914773, 40.72282083814923]
DISTANCE = 100


def loadBikeRoutes():
    print("Load bike routes file")
    return loadJson(BIKE_ROUTES_JSON)


def loadRestaurants():
    print("Load restaurants file")
    return loadJson(RESTAURANTS_JSON)


def getClient():
    print("Connect to database")
    return MongoClient(CONNECTION_STRING)
    

def getCollections(database):
    print("Get collections")
    return database[COLLECTION_BIKE_ROUTES], database[COLLECTION_RESTAURANTS]


def insertInto(collection, data):
    if not isinstance(data, list):
        raise Exception("Data to insert must be a list")
    print(f"Insert {len(data)} documents into collection")
    collection.insert_many(data)
    print(f"Collection has now {collection.count_documents({})} documents")


def main():

    print("DOES NOT WORK PROPERLY -> DO NOT USE")

    client = getClient()
    db = client[MONGO_DATABASE]
    bikeRoutesCol = db[COLLECTION_BIKE_ROUTES]
    restaurantsCol = db[COLLECTION_RESTAURANTS]

    bikeRoutesCol.delete_many({})
    restaurantsCol.delete_many({})

    bikeRoutes = loadBikeRoutes()
    restaurants = loadRestaurants()

    insertInto(bikeRoutesCol, bikeRoutes)
    insertInto(restaurantsCol, restaurants)

    res = restaurantsCol.find({
        "geometry": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": POINT
                },
                "$maxDistance": DISTANCE
            }
        }
    })
    res = list(res)
    dump = dumps(res)
    writeFile(SAMPLE_RESTAURANTS_JSON, dump)


    res = bikeRoutesCol.find({
        "geometry": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": POINT
                },
                "$maxDistance": DISTANCE
            }
        }
    })
    res = list(res)
    dump = dumps(res)
    writeFile(SAMPLE_BIKE_ROUTES_JSON, dump)
