const mongoose = require("mongoose");
const con = require('../database');

var Schema = mongoose.Schema;
//creating a Schema
var rssFeedSchema =   new Schema({
    Description: String,
    Link : String,
    PubDate: String,
    Title : String,
    Image : String
})
//creating index
rssFeedSchema.index({Description: 'text', Title:'text'},{
weights: {
Description: 5,
Title:10
} 
} );

//exporting the model
var rssFeedModel = mongoose.model('rss_feed_info',rssFeedSchema);

module.exports = rssFeedModel;