#!/usr/bin/env node

const express = require('express');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // check to see if PORT variable is defined, otherwise use 8888
const app = express();

// Define basic Hello World response
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
