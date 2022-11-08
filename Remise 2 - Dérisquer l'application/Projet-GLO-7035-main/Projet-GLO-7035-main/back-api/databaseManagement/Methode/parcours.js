const neo4j = require('neo4j-driver')
require('dotenv').config();

let connection_string = "bolt://neo4j:7687";
let user = process.env.NEO4J_AUTH.split("/")[0]
let password = process.env.NEO4J_AUTH.split("/")[1]

console.log(connection_string, user, password)

var driver = neo4j.driver(
    connection_string,
    neo4j.auth.basic(user, password),
    { disableLosslessIntegers: true }
)


function nbSegments(){
    var session = driver.session({ defaultAccessMode: neo4j.session.READ })
    return new Promise(async function (resolve,reject){
        session
        .run('MATCH ()-[bl:goes_to]->() RETURN count(bl) as count')
        .subscribe({
            onNext: record => {
                resolve(record.get("count"))
            },
            onCompleted: () => {
                session.close() // returns a Promise
            },
            onError: error => {
                console.log(error)
            }
        })
    })
}

function longeurSegments(){
    var session = driver.session({ defaultAccessMode: neo4j.session.READ })
    return new Promise(async function (resolve,reject){
        session
        .run('MATCH ()-[bl:goes_to]->() RETURN round(sum(bl.distance), 2) as totalLength')
        .subscribe({
            onNext: record => {
                resolve(record.get("totalLength"))
            },
            onCompleted: () => {
                session.close() // returns a Promise
            },
            onError: error => {
                reject(error)
            }
        })
    })
}

exports.nbSegments = nbSegments
exports.longeurSegments = longeurSegments
