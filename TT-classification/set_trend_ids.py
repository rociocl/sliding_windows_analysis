
import sys
import re
import os
import time
import json
import datetime


path = sys.argv[1]

names = [d for d in os.listdir(path) if d.endswith('.json')]
dirs = [path+d for d in os.listdir(path) if d.endswith('.json')]

for i, trend_path in enumerate(dirs):
    trend_id = names[i][2:][:-5]
    with open(path+trend_id+'.json', 'w') as output:
        for line in open(trend_path):
            tweet = json.loads(line)
            tweet["trendID"] = trend_id
            output.write(json.dumps(tweet)+'\n')

