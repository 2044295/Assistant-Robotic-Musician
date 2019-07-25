#!/usr/bin/env node

const express = require('express');
const path = require('path');
const fs = require('file-system');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // set PORT to 8888 if not env variable
const app = express();

// Define an "ls" method to list files in a directory
app.get('/ls/*', (req, res) => {
  // turn request URL into useful Path
  let lsURL;
  lsURL = req.url.split(path.sep);
  lsURL = lsURL.slice(2, lsURL.length);

  let lsPath = './Public/';
  lsURL.forEach((partial) => {
    if (partial !== '') lsPath += partial + '/';
  });

  console.log(`Files list request for ${lsPath}`);

  // get list of files in requested directory
  let filesObj = {
    url: lsPath.slice(8, lsPath.length),
    directories: ['.', '..'],
    files: [],
  };

  fs.readdir(lsPath, (err, dir) => {
    // error handling
    if (err) {
      res.status(500).jsonp({error: err});
      res.end();
      return 1;
    }

    // processing files
    dir.forEach((file) => {
      let relative = path.join(lsPath, file);
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

    console.log();

    return 0;
  });
});

// Create the Static Path to Public, and make / redirect to /Public
app.use('/', express.static('Public'));

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
