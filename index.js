#!/usr/bin/env node

const express = require('express');
const path = require('path');
const fs = require('file-system');

// Define PORT & create app
const PORT = process.env.PORT || 8888; // check to see if PORT variable is defined, otherwise use 8888
const app = express();

// Define basic Hello World response
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Define an "ls" method to list files in a directory
app.get('/ls/*', (req, res) => {
  // turn request URL into useful Path
  var lsURL;
  lsURL = req.url.split(path.sep);
  lsURL = lsURL.slice(2, lsURL.length);

  var lsPath = './';
  lsURL.forEach(partial => {
    lsPath += partial + '/';
  });

  console.log(`Files list request for ${lsPath}`);

  // ensure that Path is legal to request
  if (lsPath.slice(0, 11) !== './Projects/' && lsPath.slice(0, 9) !== './Public/') {
    console.log(`Error: Request for ls of ${lsPath} is illegal!`);
    res.status(500)
      .jsonp({error: `You do not have permission to acces this path!`})
      .end();
    return 1;
  }

  // get list of files in requested directory
  var filesObj = {
    url: lsPath.slice(1, lsPath.length),
    directories: [],
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

// Create the Static Path to Project Files
app.use('/projects', express.static('Projects'));

// Tell app to listen on appropriate PORT
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
