
from csv import reader
from lib.utils import loadJson, writeJson

RESTAURANTS_FILE = "datasets/1_transformed_restaurants.json"
BIKE_ROUTES_FILE = "datasets/1_transformed_bike_routes.json"
NEAREST_MAP_FILE = "datasets/2_nearest_map.csv"

READY_RESTAURANTS_FILE = "datasets/3_ready_restaurants_mongodb.json"
READY_BIKE_ROUTES_FILE = "datasets/3_ready_bike_routes_mongodb.json"


def loadNearestMap():
    print("Load nearest bike routes file")
    obj = {}
    with open(NEAREST_MAP_FILE, "r") as file:
        csv_reader = reader(file)
        next(csv_reader, None)
        for restaurantUid, nearestBikeRouteUid in csv_reader:
            obj[int(restaurantUid)] = nearestBikeRouteUid
    return obj


def filterAndAssignNearestMap(restaurants, nearestMap):
    restaurantsHavingNearest = []
    for restaurant in restaurants:
        restaurantUid = restaurant.get("uid")
        nearestBikeRouteUid = nearestMap.get(restaurantUid, None)
        if nearestBikeRouteUid:
            restaurant["nearestBikeRouteUid"] = nearestBikeRouteUid
            restaurantsHavingNearest.append(restaurant)
    return restaurantsHavingNearest


def main():

    # Restaurants
    restaurants = loadJson(RESTAURANTS_FILE)
    nearestMap = loadNearestMap()
    restaurants = filterAndAssignNearestMap(restaurants, nearestMap)
    writeJson(READY_RESTAURANTS_FILE, restaurants)

    # Bike routes (Nothing to do)
    bikeRoutes = loadJson(BIKE_ROUTES_FILE)
    writeJson(READY_BIKE_ROUTES_FILE, bikeRoutes)
