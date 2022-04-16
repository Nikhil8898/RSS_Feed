const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const {fetch_rss_feed} = require('../controllers/rss_feed_controller');
const rssFeedModel = require('../model/Rss_feed_model');
 
 
/* GET home page. */
router.post('/Rss_Feed_route/', fetch_rss_feed);
module.exports = router;