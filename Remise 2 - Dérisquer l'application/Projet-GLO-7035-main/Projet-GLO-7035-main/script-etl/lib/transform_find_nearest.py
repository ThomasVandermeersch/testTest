from lib.utils import loadJson, distanceBetweenCoords, appendCsv, writeFile
from itertools import groupby
from lib.transform_bike_routes import OUTPUT_FILE as BIKE_ROUTES_FILE
from lib.transform_restaurants import OUTPUT_FILE as RESTAURANTS_FILE
import time
import humanize
import datetime as dt
from multiprocessing import Process, Queue

DEBUG = False
MAX_DISTANCE = 100

NEAREST_MAP_FILE = "./datasets/2_nearest_map.csv"
SYMBOLIC_LINES_FILE = "./datasets/2_symbolic_lines.csv"


def distanceRestaurantBikeRoute(restaurant, bikeRoute):
    point = [ restaurant.get("longitude"), restaurant.get("latitude") ]
    line = bikeRoute.get("geometry").get("coordinates")[0]
    return min([
        distanceBetweenCoords(point, line[0]),
        distanceBetweenCoords(point, line[1])
    ])


def findNearestBikeRoute(restaurant, bikeRoutes):
    distancesLst = [ distanceRestaurantBikeRoute(restaurant, bikeRoute) for bikeRoute in bikeRoutes ]
    nearestDistance = min(distancesLst)
    if nearestDistance > MAX_DISTANCE:
        return None, None
    bikeRoute = bikeRoutes[ distancesLst.index(nearestDistance) ]
    return bikeRoute, None if bikeRoute is None else bikeRoute.get("uid")


def buildSymLine(nearestBikeRoute, restaurant):
    nearestBikeRouteCoords = nearestBikeRoute.get("geometry").get("coordinates")[0][0]
    return (
        restaurant.get("longitude"),
        restaurant.get("latitude"),
        nearestBikeRouteCoords[0],
        nearestBikeRouteCoords[1]
    )


def groupByBorough(restaurants):
    boroughKey = lambda k: k.get("borough")
    restaurants = sorted(restaurants, key=boroughKey)
    boroughRestaurants = groupby(restaurants, boroughKey)
    return [ (k, list(v)) for k, v in boroughRestaurants ]


def filterBikeRoutes(bikeRoutes, borough):
    return [ br for br in bikeRoutes if br.get("borough") == borough ]


def parallelFindNearestBikeRoute(nearestMapQueue, symLinesQueue, borough, boroughRestaurants, boroughBikeRoutes):
    print(f"Find nearests in {borough} ({len(boroughRestaurants)} restaurants, {len(boroughBikeRoutes)} bike routes) [MAY TAKE HOURS]")

    # debug
    avgtime = 0
    avgn = 0
    i = 0

    for restaurant in boroughRestaurants:
        # debug
        i += 1
        btime = time.process_time()

        nearestBikeRoute, nearestBikeRouteUid = findNearestBikeRoute(restaurant, boroughBikeRoutes)

        if nearestBikeRoute and nearestBikeRouteUid:
            symLine = buildSymLine(nearestBikeRoute, restaurant)
            nearestMapQueue.put((restaurant.get("uid"), nearestBikeRouteUid))
            if symLinesQueue:
                symLinesQueue.put(symLine)

        # debug
        atime = time.process_time()
        dtime = atime - btime
        rdtime = round(dtime*100)/100
        avgn += 1
        avgtime = round((avgtime + ( (dtime - avgtime) / min(avgn,20))) * 100) / 100
        nleft = len(boroughRestaurants) - i
        estimate = round(nleft * avgtime)
        if DEBUG:
            s = lambda t: humanize.naturaldelta(dt.timedelta(seconds=t))
            print(f"[{borough.ljust(15)}] {i}/{len(boroughRestaurants)} ({round(i/len(boroughRestaurants)*100*100)/100}%) - Time: {rdtime} - Avg time: {avgtime} - Time left: {s(estimate)}")


def parallelNearestMapQueueConsumer(queue):
    writeFile(NEAREST_MAP_FILE, "restaurantUid,bikeRouteUid\n")
    while True:
        item = queue.get()
        appendCsv(NEAREST_MAP_FILE, item)
        

def parallelSymLineQueueConsumer(queue):
    writeFile(SYMBOLIC_LINES_FILE, "fromLong,fromLat,toLong,toLat\n")
    while True:
        item = queue.get()
        appendCsv(SYMBOLIC_LINES_FILE, item)


def main(symLines):
    restaurants = loadJson(RESTAURANTS_FILE)
    bikeRoutes = loadJson(BIKE_ROUTES_FILE)

    nearestMapQueue = Queue()
    symLinesQueue = Queue() if symLines else None
    jobs = []

    # Queue consumers
    process = Process(target=parallelNearestMapQueueConsumer, args=(nearestMapQueue,))
    process.daemon = True
    process.start()

    if symLines:
        process = Process(target=parallelSymLineQueueConsumer, args=(symLinesQueue,))
        process.daemon = True
        process.start()
    else:
        print("Symbolic lines creation disabled")

    # Queue producers
    for borough, boroughRestaurants in groupByBorough(restaurants):
        boroughBikeRoutes = filterBikeRoutes(bikeRoutes, borough)
        process = Process(target=parallelFindNearestBikeRoute, args=(
            nearestMapQueue, symLinesQueue, borough, boroughRestaurants, boroughBikeRoutes
        ))
        jobs.append(process)
        process.start()
    
    # Wait processes
    for process in jobs:
        process.join()
