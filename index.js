#!/usr/bin/env node

// node modules
const express = require('express');

// my modules
const ls = require('ls');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // set PORT to 8888 if not env variable
const app = express();

// Define an "ls" method to list files in a directory
app.get('/ls/*', (req, res) => {
  ls(req, res);
});

// Create the Static Path to Public, and make / redirect to /Public
app.use('/', express.static('Public'));

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
