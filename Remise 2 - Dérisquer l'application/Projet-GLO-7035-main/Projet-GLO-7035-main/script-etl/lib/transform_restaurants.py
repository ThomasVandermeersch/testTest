from geojson import Point
import json
from lib.utils import loadCsvAsDF, writeJson

SOURCE_FILE = "datasets/0_original_restaurants.csv"
OUTPUT_FILE = "datasets/1_transformed_restaurants.json"

def aggregateData(df):
    BEFORE_COUNT = len(df)
    df = df.sort_values(by=["DBA", "INSPECTION DATE"])
    df = df.groupby(["CAMIS"], as_index=False).first()
    AFTER_COUNT = len(df)
    DIFF = BEFORE_COUNT - AFTER_COUNT
    PCT = round(DIFF / BEFORE_COUNT * 100)
    print(f"Aggregate data. Ended with {AFTER_COUNT} rows (-{PCT}%)")
    return df


def extractRelevantFeatures(df):
    relevantFeatures = [
        "CAMIS",
        "DBA",
        "BORO",
        "BUILDING",
        "STREET",
        "ZIPCODE",
        "PHONE",
        "CUISINE DESCRIPTION",
        "GRADE",
        "Latitude",
        "Longitude"
    ]
    print(f"Extract relevant features ({len(relevantFeatures)})")
    return df.loc[:, relevantFeatures]


def filterRequiredFeatures(df):
    BEFORE_COUNT = len(df)
    requiredFeatures = [
        "name",
        "latitude",
        "longitude",
    ]
    for rf in requiredFeatures:
        df = df.loc[ (df[rf].notnull()) & (df[rf] != 0), :]
    AFTER_COUNT = len(df)
    DIFF = BEFORE_COUNT - AFTER_COUNT
    PCT = round(DIFF / BEFORE_COUNT * 100)
    print(f"Filter required features ({len(requiredFeatures)}). Removed {DIFF} ({PCT}%) rows")
    return df


def filterByGrade(df):
    BEFORE_COUNT = len(df)
    col = "grade"
    mask = df[col].isin([ "A", "B", "C", "N", None ])
    df = df[mask]
    df.loc[ df[col].isnull(), col ] = "N" # Replace None by "N"
    AFTER_COUNT = len(df)
    DIFF = BEFORE_COUNT - AFTER_COUNT
    PCT = round(DIFF / BEFORE_COUNT * 100)
    print(f"Filter only A, B, C or N (none) grades. Removed {DIFF} ({PCT}%) rows")
    return df


def filterBadValues(df):
    mask = df["uid"] == 30075445 # This is a "Test" record inside the original dataset
    index = df[mask].index
    return df.drop(index)


def renameFeatures(df):
    columns = {
        "CAMIS": "uid",
        "DBA": "name",
        "BORO": "borough",
        "BUILDING": "building",
        "STREET": "street",
        "ZIPCODE": "zipcode",
        "PHONE": "phone",
        "CUISINE DESCRIPTION": "cuisineType",
        "GRADE": "grade",
        "Latitude": "latitude",
        "Longitude": "longitude",
    }
    print(f"Rename features ({len(columns.keys())})")
    return df.rename(columns=columns)


def mapToJson(df):
    print(f"Map to JSON {len(df)} rows")

    def mapper(obj):
        obj["geometry"] = Point((obj["longitude"], obj["latitude"]))
        return obj

    rList = json.loads(df.to_json(orient="records"))

    return list(map(mapper, rList))


def main():
    df = loadCsvAsDF(SOURCE_FILE) # Read original CSV file

    df = aggregateData(df) # Aggregate inspections by restaurants and take the most recent grade

    df = extractRelevantFeatures(df) # Extract relevant columns

    df = renameFeatures(df) # Rename features for usability

    df = filterRequiredFeatures(df) # Filter rows missing any required feature

    df = filterByGrade(df) # Filter rows not or bad graded

    df = filterBadValues(df) # Manual filter test and bad entries

    obj = mapToJson(df) # Map DataFrame to JSON object

    writeJson(OUTPUT_FILE, obj) # Write JSON object to file
