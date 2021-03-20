#!/usr/bin/env python3

import json

def output(text):
    """
    output(text)

    Outputs given "text" as an individual data package readable by NodeJS (among
    others). Text must be given in a JSON serializable. Output will flush stdin
    after each package so that receiving scripts immediately detect the line.
    """
    print(json.dumps(text), flush=True)
