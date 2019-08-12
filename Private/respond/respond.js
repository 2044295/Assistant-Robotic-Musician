#!/usr/bin/env node

const path = require('path');
const fs = require('file-system');

/**
 *
 * Responds to a regular request (NOT "/ls/*"), given the request & response
 *
 * @param{http.ClientRequest} req The URL requested
 * @param{http.ServerResponse} res The response object to write to
 * @return{int} Returns status code - 0 if no errors, 1 if path does not exist
 *
 */
function respond(req, res) {
  let relative = path.join('Public/', req.url);
  console.log(`Looking at file ${relative}`);

  fs.stat(relative, (err, stats) => {
    // error handling - directory or file does not exist
    if (err) {
      res.status(500)
          .jsonp({error: err})
          .end();

      console.log(`File or directory ${relative} does not exist!`);
      console.log();
      return 1;
    }

    // if it is a directory, respond accordingly
    if (stats.isDirectory()) {
      let index = path.join(relative, 'index.html');
      console.log(`Checking for ${index}`);

      fs.readFile(index, (err, data) => {
        // if error, index.html does not exist - use file_explorer.html
        if (err) {
          index = 'Public/assets/html/file_explorer.html';
          console.log(`Switching to ${index}`);
          res.status(200)
              .type('html')
              .end(fs.readFileSync(index));
        } else {
          res.status(200)
              .type('html')
              .end(data);
        }

        console.log(`Served ${index}`);
        console.log();
      });
    } else if (stats.isFile()) {
      fs.readFile(relative, (err, data) => {
        let type = relative.split('.').reverse()[0];
        res.status(200)
            .type(type)
            .end(data);

        console.log(`Serving ${relative}`);
        console.log();
      });
    }
  });

  return 0;
}

module.exports = respond;
