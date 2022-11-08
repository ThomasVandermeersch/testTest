const mongoose = require('mongoose');


// Schéma d'un restaurant
const restaurantSchema = new mongoose.Schema({
  name: {
    type: String,
    trim: true,
  },
  
  borough: {
    type: String,
    trim: true,
  },
  
  building:{
    type: String,
    trim: true,
  },

  street:{
    type: String,
    trim: true,
  },

  zipcode:{
    type: Number,
  },  
  
  phone:{
    type: String,
    trim: true,
  },  
  
  cuisineType:{
    type: String,
    trim: true,
  },

  grade:{
    type:String,
    trim: true,
  },
  
  geometry: {
    type: {
      type: String, // Don't do `{ location: { type: String } }`
      enum: ['Point'], // 'location.type' must be 'Point'
      required: true
    },
    coordinates: {
      type: [Number],
      required: true
    }
  }
});





//Export the model to use it.
module.exports = mongoose.model('Restaurant', restaurantSchema);