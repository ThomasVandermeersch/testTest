from lib.utils import loadFile
from py2neo import Graph


DEBUG = False

NEO4J_USER = "neo4j"
NEO4J_PWD = "rootpassword"
NEO4J_DATABASE = "parcoursVeloEpicurien"
NEO4J_HOST = "localhost"

READY_FILE = "datasets/3_ready_neo4j.cypher"


def getConnectionString():
    return f"bolt://{NEO4J_HOST}:7687"


def loadCypherQueries():
    file = loadFile(READY_FILE)
    return file.splitlines()


def main(truncate=False):

    queries = loadCypherQueries()

    print("Connect to ", getConnectionString())
    session = Graph(getConnectionString(), auth=(NEO4J_USER, NEO4J_PWD))

    if truncate:
        print("Truncate database")
        session.run("MATCH (n) DETACH DELETE n")

    tx = session.begin()
    n = len(queries)
    i = 0
    for q in queries:
        i+= 1
        if DEBUG:
            print(f"Populate Neo4J database [{round(i/n*100*100)/100}%]")
        tx.run(q)
        if i % 1000 == 0:
            tx.commit()
            tx = session.begin()
    print("")

    tx.commit()
