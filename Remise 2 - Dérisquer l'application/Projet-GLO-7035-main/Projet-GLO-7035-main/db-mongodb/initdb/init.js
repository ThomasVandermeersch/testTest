print("START INIT SCRIPT==========================================================")

db.createCollection("bikeRoutes")
db.bikeRoutes.createIndex({ "uid": 1 }, { unique: true })
db.bikeRoutes.createIndexes([
    { "geometry": "2dsphere" },
    { "borough": 1 }
])

db.createCollection("restaurants")
db.restaurants.createIndex({ "uid": 1 }, { unique: true })
db.restaurants.createIndexes([
    { "geometry": "2dsphere" },
    { "borough": 1 },
    { "grade": 1 },
    { "cuisineType": 1 }
])

print("END OF INIT SCRIPT==========================================================")
