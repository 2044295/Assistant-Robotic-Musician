#!/usr/bin/env python3

# STILL NEEDS: JSON output, stdin/stdout, stderr
# - Make sure that this is an *comprehensive* example of cross-app communication

import sys
import argparse
import json

""""""
"""Setting up argparse: https://docs.python.org/3/library/argparse.html"""
# Initializing the Parser Object
parser = argparse.ArgumentParser(
    description='A comprehensive Python3 I/O example')

# Demo: Setting up a simple flag - in this case, (de)activating output
parser.add_argument('-b', '--no-basic', action='store_const', const=True,
                    default=False, help='deactivate basic text output')
parser.add_argument('-s', '--sample', action='store_const', const=True,
                    default=False, help='activate to test a sample flag')
parser.add_argument('-a', '--arguments', action='store_true',
                    help='activate the arguments ii demo')

# Demo: Setting up an argument - many options; note, variable is always a list
parser.add_argument('positional', action='store', nargs='*', default=[],
                    help="a sample positional argument; a sample `nargs='*'``")
parser.add_argument('-one', '--one-arg', action='store', nargs=1,
                    help="a demonstration of a flag with a single argument")
parser.add_argument('-two', '--two-arg', action='store', nargs=2,
                    help="a demonstration of a flag with two arguments")
parser.add_argument('-n', '--n-arg', action='store', nargs='+',
                    help="a demonstration of a flag `nargs='+'`")
parser.add_argument('--manipulate', action='store', nargs=1, default='',
                    type=str, help='sample text manipulation: splitting by `.`')

# Adding a JSON flag to active JSON Output
parser.add_argument('--json', action='store_true',
                    help='activate the JSON demo')

# And Lastly, Parsing the Args - Except the Script Name, Obviously
argv = parser.parse_args(sys.argv[1:])

if argv.json:
    argv.no_basic = True
    argv.sample = False
    argv.arguments = False

""""""
# BASIC TEXT: With no arguments, output a few demonstrative lines
if not(argv.no_basic):
    print(42 + 27)

    some_list = ['foo', 'bar', 'hello world']

    for item in some_list: print(item)
    print(some_list)

# ARGUMENTS I: If the sample flag is received, say so
if argv.sample:
    print('Sample flag received and processed!')
    print('Original Input: {}'.format(sys.argv))
    print('Processed Args: {}'.format(argv))

# ARGUMENTS II: Working with arguments that store input values
if argv.arguments:
    print('Argument Demo Request Received!')
    print('Positional Argument(s): {}'.format(argv.positional))
    print('Single Argument: {}; Double Argument: {}'.format(argv.one_arg,
        argv.two_arg))
    print('n-arg Argument: {}'.format(argv.n_arg))
    print('Manipulation: {}'.format(argv.manipulate[0].split('.')))

# JSON: Sample JSON Output
if argv.json:
    sample_json_dic = {
        'int': 420,
        'float': 1.618,
        'string': "hello world",
        'list': [420, 1.618, "hello world"],
        # 'function': lambda x: x + 5, - fails
    }
    print(json.dumps(sample_json_dic))
