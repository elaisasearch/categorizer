import os
import json

"""
Load the global configurations for Categorizer.
    - source: https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
"""
scriptDir = os.path.dirname(__file__) 
relPath = '../../bin/globals.json'
with open(os.path.join(scriptDir, relPath)) as f: 
    GLOBALS = json.load(f)

API_KEY = GLOBALS['api']['x-api-key']