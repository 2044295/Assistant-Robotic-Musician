#!/usr/bin/env node

// STILL NEEDS: documentation, examples, full explanation

/* Python Shell: https://www.npmjs.com/package/python-shell */
/*
 * Documentation (https://www.npmjs.com/package/python-shell#api-reference)
 * - PythonShell(script, options)
 *
 */

const PythonShell = require('python-shell').PythonShell

console.log(PythonShell)

// Run-String: Mostly a demonstrative method
PythonShell.runString("x = 2 + 2; print(x); print(2*x)", null, (err, res) => {
  if (err) { throw err; }
  console.log(res);
});
