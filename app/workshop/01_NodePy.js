#!/usr/bin/env node

// STILL NEEDS: examples, full explanation

/* Python Shell: https://www.npmjs.com/package/python-shell */
/*
 * Documentation (https://www.npmjs.com/package/python-shell#api-reference)
 * - Options
 *   - args: array of arguments, effectively sys.argv---DOES SCRIPT NAME COUNT??
 *   - scriptPath: string, path prefix for accessing scripts, if necessary
 *   - pythonPath: string, python executable, if not specified in the script
 *   - pythonOptions: array of command-line options for the executable
 *   - mode: string text/json/binary: data mode, in text, json, or terminal std
 *     - encoding: string, text encoding
 *     - formatter: method for formatting transmitted data
 *     - parser: method acting on and emitting transmitted data
 *     - stderrParser: method acting on and emitting transmitted logs (stderr)
 *
 * - PythonShell.run[Script](script/code, options, callback)
 *   - Synchronous function that runs Python and returns errors or results
 *   - script/code: a string, indicating the code that is to be run. run
 *     accesses the file by that nume; runString runs the code
 *   - options: see "options" above
 *   - callback: the callback function, running when the script is complete
 *
 * - new PythonShell(script, options)
 *   - Object Constructor: Useful but complicated
 *
 */

console.log('Welcome to the PythonShell demonstration script!\n');

/* Setup */
// IMPORT: PythonShell is a class within the `python-shell` package
const PythonShell = require('python-shell').PythonShell;

// Displaying the `console.log` for more details
console.log('Displaying the `PythonShell` class, for more information')
console.log('-', PythonShell);
console.log();

/* Basic */
// DEMO 1: Running runString as a demonstrative method
PythonShell.runString("x = 2 + 2; print(x); print(2*x)", null, (err, res) => {
  if (err) { throw err; }
  console.log('Results of `runString` method');
  console.log('-', res);
  console.log();
});

/* Standard */
// Ideally, insert an example showing specifity of programming language
// DEMO 3: "BASIC TEXT", the most basic run demonstration
PythonShell.run('01_NodePy.py', null, (err, res) => {
  if (err) { throw err; }
  console.log('[BASIC TEXT] Results of `run` method');
  console.log('- Returns an array of strings, separated at newlines');
  console.log('-', res);
  console.log('- For complex data, strings must be manually processed');
  console.log();
});

// DEMO 4: "ARGUMENTS I", demonstrating some basic flags
PythonShell.run('01_NodePy.py', {args: ['-b', '-s']}, (err, res) => {
  if (err) { throw err; }
  console.log('[ARGUMENTS I] Running with simple flags: 01_NodePy.py -b -s');
  console.log('- `-b` deactivates basic text; `-s` activates sample flag');
  console.log('- Order doesn\'t matter, as these are just flags');
  console.log('-', res);
  console.log();
});

// DEMO 5: "ARGUMENTS II", demonstrating flags with arguments
let options = {
  args: [
    'foo bar',
    '-b', '-a',
    '-one', 'three',
    '-two', 'forty', 'two',
    '-n', 'foo', 'bar',
    '--manipulate', 'foo.bar'
  ]
}
PythonShell.run('01_NodePy.py', options, (err, res) => {
  if (err) { throw err; }
  console.log('[ARGUMENTS II]: Running with a laundry list of arguments');
  console.log(`- 01_NodePy.py ${options.args}`);
  console.log('- Order doesn\'t matter greatly; see argparse for details');
  console.log('- Note that output is still just text; input is only strings:');
  console.log('-', res);
  console.log('- Observe that arguments can have spaces and be one unit');
  console.log('  and that multiple entries for an argument must be separate');
  console.log();
});

// DEMO 6: "JSON", because maybe what we have to do is print entirely in JSON?
PythonShell.run('01_NodePy.py', {args: ['--json'], mode: 'json'}, (err, res) => {
  if (err) { throw err; }
  console.log('[JSON] Running with simple flags: 01_NodePy.py --json');
  console.log("- The `mode: 'json'` option causes PythonShell to try to");
  console.log("  parse all printed output as JSON - so Python must output");
  console.log("  only JSON (see the Python Example + python.json for details)");
  console.log('-', res);
  console.log();
});

// Perhaps something with more options - show the default options?
// IF THERE'S TIME: Experiment more with stdin/stdout
   // That might be better-suited for Advanced, though

/* Advanced */
// let shell = new PythonShell('01_NodePy.py', {mode: "text"});
// console.log(shell.stderr.text)
// console.log('As you can see, the script fails quite dramatically');
