#!/usr/bin/env node

// node modules
const express = require('express');

// my modules
const ls = require('ls');
const respond = require('respond');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // set PORT to 8888 if not env variable
const app = express();

app.get('/*', (req, res) => {
  console.log(`Request for ${req.url}`);

  if (req.url.slice(0, 4) == '/ls/') {
    ls(req, res); // if request is an "ls" request, respond accordingly
  } else {
    respond(req, res); // else it is a real request, respond accordingly
  }
});

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
  console.log();
});
