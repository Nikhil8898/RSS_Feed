const mongoose = require('mongoose')
const express = require('express');
const bodyParser = require('body-parser');
mongoose.Promise = global.Promise;
const url = "mongodb://localhost:27017/rss_feed";
const route = require('./routes/Rss_feed_route');

const app = express();
var cors = require('cors')

var corsOptions = {
  origin: "*"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(bodyParser.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/',route)

const PORT = process.env.PORT || 8080;
mongoose.connect(url, { useNewUrlParser:true, useUnifiedTopology: true})
        .then(() => app.listen(PORT, () => console.log(`Server is running on port ${PORT}.`)))
        .catch

module.exports = app;