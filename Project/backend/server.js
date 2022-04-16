const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

//const uri = process.env.ATLAS_URI;
// mongoose.connect('mongodb://localhost:27017', { useNewUrlParser: true, useCreateIndex: true }
// );
const URI = process.env.MONGODB_URL;

mongoose.connect(URI, {useNewUrlParser: true, useUnifiedTopology: true }, 
    err => {
        if(err) throw err;
        console.log('Connected to MongoDB!!!')
    });
const connection = mongoose.connection;
connection.once('open', () => {
  console.log("MongoDB database connection established successfully");
})

//const exercisesRouter = require('./routes/exercises');
//const usersRouter = require('./routes/users');

// app.use('/exercises', exercisesRouter);
// app.use('/users', usersRouter);

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});