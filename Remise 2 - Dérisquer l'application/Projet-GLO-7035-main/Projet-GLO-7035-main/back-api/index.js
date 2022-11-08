const express = require("express")
const app = express()
const PORT = 8080

// Connexion à la base de données
const connexion = require('./databaseManagement/dbMongo_connexion')
connexion()


// Récupération des scripts de base de données 
require('./databaseManagement/Modele/Restaurant');

const restaurant = require("./databaseManagement/Methode/restaurant")
const parcours = require("./databaseManagement/Methode/parcours")

const VILLE_CHOISIE = "New York";

app.get('/heartbeat', (req, res) => {
    console.log("Get heartbeat")
    res.send({ villeChoisie: VILLE_CHOISIE })
})

app.get('/extracted_data', (req,res)=>{    
    console.log("Get extracted data")
    Promise.all([restaurant.count(),parcours.nbSegments()]).then((values)=>{
        res.send({nbRestaurants : values[0], nbSegments: values[1]})
    }).catch((err)=>{
        console.log(err)
    })
})

app.get('/transformed_data', (req,res)=>{
    console.log("Get transformed data")
    Promise.all([restaurant.count_by_type(),parcours.longeurSegments()]).then((result)=>{
        res.send({restaurants : result[0], longueurCyclable : result[1] })
    }).catch((err)=>{
        console.log(err)
    })
})

app.listen(PORT, () => {
    console.log(`App listening on port ${PORT}`)
})