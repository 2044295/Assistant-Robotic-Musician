#!/usr/bin/env node

const fs = require('file-system');

/**
 *
 * Turns a source HTML file and body HTML text into a single HTML response
 *
 * @param{string} source The path to the source HTML file
 * @param{string} body The path to the body HTML file
 * @param{string} matchString the string to find the lines to be replaced
 * @return{string} Returns a string that is the sum of the body and source
 */
function makeHTML(source, body, matchString = '<!-- !PAGE CONTENT HERE! -->') {
  let match = new RegExp('[ ]*' + matchString);
  let output = '';

  let data = fs.readFileSync(source, 'utf-8');
  let lines = data.split('\n');

  for (let i = 0; i < lines.length; i++) {
    if (match.test(lines[i])) {
      let padding = lines[i].slice(0, lines[i].length - matchString.length);

      let bodyLines = body.split('\n');
      for (let j = 0; j < bodyLines.length; j++) {
        output += padding + bodyLines[j] + '\n';
      }

      console.log(`Replaced line ${i} with BODY`);
    } else {
      output += lines[i] + '\n';
    }
  }

  console.log(`Joined file ${source} with BODY`);
  // console.log(output);

  return output;
}

module.exports = makeHTML;
