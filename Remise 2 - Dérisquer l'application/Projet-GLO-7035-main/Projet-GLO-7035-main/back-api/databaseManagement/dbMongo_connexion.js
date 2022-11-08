//Connexion to MongoDB

const mongoose = require('mongoose');
require('dotenv').config();


module.exports = function connect(){
    user = process.env.MONGO_INITDB_ROOT_USERNAME
    password = process.env.MONGO_INITDB_ROOT_PASSWORD
    host = "mongodb"
    port = process.env.MONGO_DB_PORT ?? 27017
    db_name = process.env.MONGO_INITDB_DATABASE

    connection_string = "mongodb://" + user + ":" +  password +"@" + host + ":" + port + "/" + db_name + "?authSource=admin"
    console.log(connection_string)
    mongoose.connect(connection_string, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });

    mongoose.connection
        .on('open', () => {
            console.log('Mongoose connection open');
        })
        .on('error', (err) => {
            console.log(`Connection error: ${err.message}`);
        });
}