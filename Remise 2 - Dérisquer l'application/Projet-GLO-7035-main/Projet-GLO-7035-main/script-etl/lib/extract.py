from urllib.request import urlretrieve


RESTAURANTS_URL = "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
BIKE_ROUTES_URL = "https://data.cityofnewyork.us/api/geospatial/7vsa-caz7?method=export&format=GeoJSON"

RESTAURANTS_FILE = "datasets/0_original_restaurants.csv"
BIKE_ROUTES_FILE = "datasets/0_original_bike_routes.geojson"


def main():
    
    print("Retrieve restaurants file")
    urlretrieve(RESTAURANTS_URL, RESTAURANTS_FILE)
    print("\n")

    print("Retrieve bike routes file")
    urlretrieve(BIKE_ROUTES_URL, BIKE_ROUTES_FILE)
    print("\n")
