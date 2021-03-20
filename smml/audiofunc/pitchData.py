#!/usr/bin/env python3

import json
import os

mypath = os.path.join(os.path.dirname(__file__), 'pitchData.json')
with open(mypath, 'r') as myfile:
    pitchData = json.loads(myfile.read())
