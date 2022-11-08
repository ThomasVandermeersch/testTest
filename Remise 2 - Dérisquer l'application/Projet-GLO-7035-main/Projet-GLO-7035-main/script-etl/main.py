from argparse import ArgumentParser
from lib import extract, transform_restaurants, transform_bike_routes, load_mongodb, load_neo4j, transform_find_nearest, prepare_for_mongodb, prepare_for_neo4j


if __name__ == "__main__":
    # Args parser configuration
    parser = ArgumentParser(description="Run ETL script pipeline for GLO-7035 application")

    parser.add_argument("-e", "--extract", help="Extract data from source and get raw datasets",  action="store_true")
    parser.add_argument("-t", "--transform", help="Transform both raw datasets",  action="store_true")
    parser.add_argument("-l", "--load", help="Load read-to-import datasets into both mongodb and neo4j",  action="store_true")
    parser.add_argument("--load-mongodb", help="Load read-to-import datasets into mongodb only",  action="store_true")
    parser.add_argument("--load-neo4j", help="Load read-to-import datasets into neo4j only",  action="store_true")
    parser.add_argument("--truncate", help="Dump databases before insertion", action="store_true")
    parser.add_argument("--debug", help="Display some debug information", action="store_true")
    parser.add_argument("--symlines", help="Enable symbolic lines creation on transformation step", action="store_true")
    parser.add_argument("--skip-nearest-map", help="Skip nearest map step (may take up to 7 hours)", action="store_true")
    parser.add_argument("--mongodb-host")
    parser.add_argument("--neo4j-host")


    args = parser.parse_args()

    truncate = getattr(args, "truncate")
    debug = getattr(args, "debug")

    ## Extract
    if getattr(args, "extract"):
        print("\n> Data extraction...")
        extract.main()

    # Transform (bike routes)
    if getattr(args, "transform"):
        print("\n> Bike routes data transformation...")
        transform_bike_routes.main()

        print("\n> Restaurants data transformation...")
        transform_restaurants.main()

    if getattr(args, "transform") and not getattr(args, "skip_nearest_map"):
        print("\n> Find nearest bike route for each restaurants...")
        transform_find_nearest.DEBUG = debug
        symlines = getattr(args, "symlines")
        transform_find_nearest.main(symLines=symlines)

    # Prepare
    if getattr(args, "transform"):
        print("\n> Prepare for MongoDB...")
        prepare_for_mongodb.main()

        print("\n> Prepare for Neo4j...")
        prepare_for_neo4j.main()
    
    # Load (mongodb)
    if getattr(args, "load") or getattr(args, "load_mongodb"):
        print("\n> Data loading into MongoDB...")
        load_mongodb.DEBUG = debug
        mongoHost = getattr(args, "mongodb_host")
        if mongoHost:
            load_mongodb.MONGO_HOST = mongoHost
        load_mongodb.main(truncate)

    # Load (neo4j)
    if getattr(args, "load") or getattr(args, "load_neo4j"):
        print("\n> Data loading into Neo4j...")
        load_neo4j.DEBUG = debug
        neo4jHost = getattr(args, "neo4j_host")
        if neo4jHost:
            load_neo4j.NEO4J_HOST = neo4jHost
        load_neo4j.main(truncate)

    print("\n> Add -h flag for help")
    print("> End of script")