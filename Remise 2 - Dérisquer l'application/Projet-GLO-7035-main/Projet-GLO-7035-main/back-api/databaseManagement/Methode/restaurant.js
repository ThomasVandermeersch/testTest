const mongoose = require('mongoose');
const Restaurant = mongoose.model('Restaurant');

function count(){
    return new Promise(function(resolve,reject){        
        Restaurant.countDocuments({}, function(err,count ){
            if(err) reject(err)
            else{
                resolve(count)
            } 
        })
    })
}

function count_by_type(){
    return new Promise(function(resolve,reject){ 
        query = [{
            $group: {
                _id: '$cuisineType',
                count: { $count: { } }
            }
        }]

        Restaurant.aggregate(query, function(err,result ){
            if(err) reject(err)
            else{
                transformed_result = {}
                result.forEach(element => {
                    transformed_result[element._id] = element.count
                });
                resolve(transformed_result)
            } 
        })
    })
}

exports.count = count
exports.count_by_type = count_by_type

// exports.search = search