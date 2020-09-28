#!/usr/bin/env node

/*
Explanation:

NodeJS is built on an asynchronus design. This means that, while the process is
single-threaded (has only one thread processing instructions), it can set up
functions to run on their own and call it back when they're done (kind of like a
waiter) to perform some sort of function. Typically, what this means is that our
code has to define how the app is going to respond to certain stimuli.

The 'get' function checks that a received request match the given URL or Regular
Expression ('/*' matches anything with a '/'), and if it does, supplies the
Request and Response objects to the callback function (generally, a function to
be run when a process is done) that then processes them appropriately.

This 'get' function is exceedingly, stupidly simple. This is intentional, as
this isn't meant to be any sort of useful app, but rather a tool for
frontloading the GUI development. All this structure means a few things:

01. All HTML should be developed as individual files in the 'HTML' directory
02. Structure should be kept at a bare minimum; this function can naturally
    process subdirectories but is really just a tool to display files by name
03. This structure is open to discussion but I'm picturing that we just build a
    set of files that make up the different "screens" we'll need, and then we
    can set up ways to switch between them and subsequently functionts within
    each (when the backend is ready)
04. CSS and JavaScript files should function normally
05. MAKE SURE you write URLs with 'HTML' being the root directory (the '/')
06. Once you've installed NodeJS, you can run the app by typing "npm start,"
    or "npm test" (if you have node-dev installed, it provides a more forgiving
    development with auto-restarts) and typing the url you want

I think that, for now at least, that is all you need to know. Please don't
hesitate to complain to me if this app is completely broken or if what I say
makes no sense; I'll be happy to correct my oversights and errors. Now, get to
designing! And, as always, may the odds be ever in your favor.

- Queen "Evan" Victory
*/

/* Initial Setup */
const express = require('express'); // a basic request/response for early tests
const fs = require('file-system');  // a simple filesystem API
const path = require('path');       // a tool for manipulating directory paths

/* *** */
/* And now, to set up the app */
// We start by defining the port ('localhost:PORT/URL') and the app object
const PORT = process.env.port || 8888;  // set PORT to 8888 if not env variable
const app = express();                  // runs a setup that returns the object

// Defining the 'get' routine - how we use RegEx to respond to various requests
app.get('/*', (req, res) => {
  // Adjust path and, for debugging, log the received request
  let relative = path.join('HTML', req.url);
  console.log(`Request received for ${relative}`);

  // Now we feed file stats to the callback
  fs.stat(relative, (err, stats) => {
    // stupidly simple error handling, for now
    if (err) { throw err; }

    // now we assume that only files will be requested
    fs.readFile(relative, (err, data) => {
      if (err) { throw err; }

      let type = relative.split('.').reverse()[0];
      res.status(200)
         .type(type)
         .end(data);
    });
  });
});

/* *** */
/* And at last, we start listening on appropriate PORT */
app.listen(PORT, () => {
  console.log(`Listening on localhost:${PORT}`);
  console.log();
});
