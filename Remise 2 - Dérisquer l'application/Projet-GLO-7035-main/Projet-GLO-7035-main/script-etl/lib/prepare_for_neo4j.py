from lib.utils import loadJson, writeFile, appendFile, roundCoord, hashObject, distanceBetweenCoords
from csv import reader

RESTAURANTS_FILE = "datasets/1_transformed_restaurants.json"
BIKE_ROUTES_FILE = "datasets/1_transformed_bike_routes.json"
NEAREST_MAP_FILE = "datasets/2_nearest_map.csv"

READY_FILE = "datasets/3_ready_neo4j.cypher"

def loadNearestMap():
    print("Load nearest bike routes file")
    obj = {}
    with open(NEAREST_MAP_FILE, "r") as file:
        csv_reader = reader(file)
        next(csv_reader, None)
        for restaurantUid, nearestBikeRouteUid in csv_reader:
            obj[int(restaurantUid)] = nearestBikeRouteUid
    return obj


def buildQuery(query, *args):
    query = query.format(*args)
    query = query.strip()
    query = " ".join([ l.strip() for l in query.split("\n") ])
    return query


def escapeValue(val):
    return val.replace("\"", "")


def buildCreateRestaurant(restaurant):
    uid = restaurant.get("uid")
    name = restaurant.get("name")
    grade = restaurant.get("grade")
    cuisineType = restaurant.get("cuisineType")
    return buildQuery("""
        MERGE (r:Restaurant {{ uid: {}, name: \"{}\", grade: \"{}\", cuisineType: \"{}\" }})
    """, uid, escapeValue(name), grade, cuisineType)


def buildCreateIntersection(intersectionId):
    return buildQuery("""
        MERGE (i:Intersection {{ hash: \"{}\" }})
    """, intersectionId)


def buildJoinIntersection(fromInterId, toInterId, bikeRouteUid, distance):
    return buildQuery("""
        MATCH (from:Intersection {{ hash: \"{}\" }}) 
        MATCH (to:Intersection {{ hash: \"{}\" }})
        MERGE (from)-[:goes_to {{ uid: \"{}\", distance: {} }}]->(to)
    """, fromInterId, toInterId, bikeRouteUid, distance)


def buildJoinRestaurant(resaurantUid, bikeRouteUid):
    return buildQuery("""
        MATCH (r:Restaurant {{ uid: {} }})
        MATCH (i:Intersection)<-[:goes_to {{ uid: \"{}\" }}]-(:Intersection)
        MERGE (r)-[:is_at]->(i)
    """, resaurantUid, bikeRouteUid)


def insertRestaurants(restaurants):
    print("Insert restaurants")
    for restaurant in restaurants:
        query = buildCreateRestaurant(restaurant)
        appendFile(READY_FILE, query)


def insertBikeRoutes(bikeRoutes):
    print("Insert bike routes")
    createdIntersectionIds = set()
    for br in bikeRoutes:
        # Create intersections
        prevIntersectionId = None
        prevCoord = None
        distance = None
        bikeRouteUid = br.get("uid")
        for coord in br.get("geometry").get("coordinates")[0]:
            coord = roundCoord(coord)
            intersectionId = hashObject(coord)
            if intersectionId not in createdIntersectionIds:
                query = buildCreateIntersection(intersectionId)
                createdIntersectionIds.add(intersectionId)
                appendFile(READY_FILE, query)
            if prevIntersectionId and prevIntersectionId != intersectionId:
                distance = distanceBetweenCoords(coord, prevCoord)
                query = buildJoinIntersection(prevIntersectionId, intersectionId, bikeRouteUid, distance)
                appendFile(READY_FILE, query)
            prevIntersectionId = intersectionId
            prevCoord = coord


def insertNearestMap(nearestMap):
    print("Insert nearest map")
    for restaurantUid, bikeRouteUid in nearestMap.items():
        query = buildJoinRestaurant(restaurantUid, bikeRouteUid)
        appendFile(READY_FILE, query)


def main():
    restaurants = loadJson(RESTAURANTS_FILE)
    bikeRoutes = loadJson(BIKE_ROUTES_FILE)
    nearestMap = loadNearestMap()

    writeFile(READY_FILE, "")

    insertRestaurants(restaurants)
    insertBikeRoutes(bikeRoutes)
    insertNearestMap(nearestMap)
    