from lib.utils import loadJson, writeJson, hashObject

SOURCE_FILE = "datasets/0_original_bike_routes.geojson"
OUTPUT_FILE = "datasets/1_transformed_bike_routes.json"

def extractFeatures(geojson):
    print("Extract features")
    return geojson["features"]


def mapBoro(boroCode):
    boros = {
        "1": "Manhattan",
        "2": "Bronx",
        "3": "Brooklyn",
        "4": "Queens",
        "5": "Staten Island"
    }
    return boros.get(boroCode, None)


def mapBikeDir(bikedir):
    bikedirs = {
        "R": "start-to-end",
        "L": "end-to-start",
        "2": "two-ways"
    }
    return bikedirs.get(bikedir, None)


def mapToJsonRelevantFeatures(lst):
    print("Map features to json")
    def mapper(obj):
        tmp = {
            "street": obj.get("properties").get("street"),
            "borough" : mapBoro(obj.get("properties").get("boro")),
            "bikedir": mapBikeDir(obj.get("properties").get("bikedir")),
            "geometry": obj.get("geometry"),
        }
        tmp["uid"] = hashObject(tmp)
        return tmp

    return list(map(mapper, lst))


def dropDuplicates(lst):
    hashes = []
    out = []
    for obj in lst:
        if obj.get("uid") not in hashes:
            out.append(obj)
            hashes.append(obj.get("uid"))
    return out


def main():
    print("Nothing to transform")

    geojson = loadJson(SOURCE_FILE)

    geolst = extractFeatures(geojson)

    lst = mapToJsonRelevantFeatures(geolst)

    lst = dropDuplicates(lst)

    writeJson(OUTPUT_FILE, lst)
