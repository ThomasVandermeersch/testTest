import pandas as pd
import os
from humanize import naturalsize
import json
from hashlib import shake_256
from geopy import distance, Point
import geojson


def getFileSize(path):
    stats = os.stat(path)
    return naturalsize(stats.st_size)


def loadCsvAsDF(path, headers=True):
    h = 0 if headers else None
    df = pd.read_csv(path, sep=",", header=h)
    print(f"Read file {path} ({getFileSize(path)}) containing {len(df)} rows")
    return df


def loadJson(path):
    print(f"Read JSON {path} ({getFileSize(path)})")
    with open(path, "r") as file:
        return json.load(file)


def loadGeoJson(path):
    print(f"Read GeoJSON {path} ({getFileSize(path)})")
    with open(path, "r") as file:
        return geojson.load(file)


def loadFile(path):
    print(f"Read file {path} ({getFileSize(path)})")
    with open(path, "r") as file:
        return file.read()


def writeFile(path, content):
    with open(path, "w+") as file:
        file.write(content)
    print(f"Write file {path} ({getFileSize(path)})")


def writeCsv(path, df):
    df.to_csv(path)
    print(f"Write CSV {path} ({getFileSize(path)})")


def writeJson(path, obj):
    strObj = json.dumps(obj)
    writeFile(path, strObj)
    print(f"Write JSON {path} ({getFileSize(path)})")


def writeGeoJson(path, obj):
    strObj = geojson.dumps(obj)
    writeFile(path, strObj)
    print(f"Write GeoJSON {path} ({getFileSize(path)})")


def appendFile(path, data):
    with open(path,'a') as file:
        file.write(data + "\n")


def appendCsv(path, items):
    line = ",".join(map(str, items)) + "\n"
    appendFile(path, line)

def hashObject(obj):
    string = json.dumps(obj)
    encoded = string.encode("utf-8")
    return shake_256(encoded).hexdigest(10)


def distanceBetweenCoords(coord1, coord2, decimals=1):
    point1 = Point(coord1[1], coord1[0])
    point2 = Point(coord2[1], coord2[0])
    d = distance.distance(point1, point2).m
    factor = 10**decimals
    return round(d * factor) / factor


def roundCoord(coord, decimals=4):
    factor = 10**decimals
    return [ round(c * factor) / factor for c in coord ]