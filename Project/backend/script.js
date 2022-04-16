const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const express = require('express')
const path = require('path')
const model = require('./model/Rss_Feed_model')
const Rss_feed_model = require('./model/Rss_Feed_model')
const { router } = require('./app')
const app = express()
  
//const app = require('./app')
console.log('Rss_Feed require =>', Rss_feed_model)
console.log('Rss Feed from mongoose =>', mongoose.model('Rss_Feed_Model'))
mongoose.connect('mongodb://localhost/Rss_Feed',
() =>{
    console.log("connected")
},
e => console.error(e))
app.use('/',express.static(path.resolve(__dirname, 'assets')))
app.use(bodyParser.json())
app.use('/',router)
// app.post('/api/create', async(req,res) => {
//     const record = req.body
//     console.log(record)
//     res.json({status:'ok'})

// })



