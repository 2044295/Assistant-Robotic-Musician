#!/usr/bin/env node

const express = require('express');
const path = require('path');
const fs = require('file-system');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // check to see if PORT variable is defined, otherwise use 8888
const app = express();

// Define an "ls" method to list files in a directory
app.get('/ls/*', (req, res) => {
  // turn request URL into useful Path
  var lsURL;
  lsURL = req.url.split(path.sep);
  lsURL = lsURL.slice(2, lsURL.length);

  var lsPath = './Public/';
  lsURL.forEach(partial => {
    if (partial !== '') lsPath += partial + '/';
  });

  console.log(`Files list request for ${lsPath}`);

  // get list of files in requested directory
  var filesObj = {
    url: lsPath.slice(8, lsPath.length),
    directories: ['.', '..'],
    files: []
  };

  fs.readdir(lsPath, (err, dir) => {
    // error handling
    if (err) {
      res.status(500).jsonp({error: err});
      res.end();
      return 1;
    }

    // processing files
    dir.forEach(file => {
      var relative = path.join(lsPath, file);
      if (fs.lstatSync(relative).isDirectory()) {
        filesObj.directories.push(file);
      } else {
        filesObj.files.push(file);
      }
    });

    // send out found information
    console.log(filesObj);
    res.status(200)
      .jsonp(filesObj)
      .end();

    return 0;
  });
});

// Create the Static Path to Public, and make / redirect to /Public
app.use('/', express.static('Public'));

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
