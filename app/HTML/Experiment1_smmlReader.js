#!/usr/bin/env node

/*
 * The sample code for SMML-String conversion -- to be embedded in any app
 *
 * For whatever reason, I decided to write the SMML Reader in Python (probably
 * because it was easier for me) so we have to interface with the Python Script
 * in order to run it and get output. This should be a minor detail -- a task
 * for a few lines of code outlined below -- that is not at all CPU intense and
 * only has to occur once. However, if for any reason I need to rewrite the
 * packge in NodeJS, or if you encounter any bugs, please let me know so that
 * I may address the issues promptly.
 *
 */

// IMPORTANT: Must include the 'python-shell' package (generally at the
// beginning of a NodeJS file) in order to interact with the Python Script
const PythonShell = require('python-shell').PythonShell;

// THE ACTUAL FUNCTION
// This is what you call any time you need to process a given SMML file
let options = {args: ['Experiment1_SampleSMML.smml']}
PythonShell.run('smmlReader.py', options, (err, res) => {
  if (err) { throw err; }
  console.log(res);
  console.log();
});

/*
 * DOCUMENTATION:
 *   PythonShell.run('smmlReader.py', {args: ['FILENAME']}, callback)
 *
 * Runs the SMML Reader script on the file name that is supplied via
 * {args: ['FILENAME']}, and, when the SMML Reader script finishes, passes
 * the received data to the "callback" function. Note that the "callback"
 * function doesn't necessarily run before lines that occur later in the file,
 * depending on how long the process takes. (Ask me if you want a more in-depth
 * explanation of callback functions.)
 *
 * Note that, as I did, you can absolutely use a separate line to create an
 * "options" object that contains the filename -- just make sure that it is in
 * the format I have outlined. I just did it to minimize line length in this
 * example.
 *
 */
