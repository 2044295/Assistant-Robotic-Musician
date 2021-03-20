#!/usr/bin/env node

// IMPORT: PythonShell is a class within the `python-shell` package
const PythonShell = require('python-shell').PythonShell;
let options = {args: ['--test-json'], mode: 'json'}
function test_func(res) {
  console.log(res);
}
let n = 0; // counts the messages

// DEMO: Create an instance of PythonShell that responds to live updates
let pyshell = new PythonShell('06_audioProcessor.py', options);

// sends a message to the Python script via stdin
// pyshell.send('hello');

// receiving a "message" (text) via stdout from python
// note that this requires sys.stdout.flush() in python to activate properly
pyshell.on('message', (message) => {
  test_func(message);
  n++;
});

// end the input stream and allow the process to exit
pyshell.end(function (err,code,signal) {
  if (err) throw err;
  console.log(`Received ${n} messages`);
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('Finished');
});
