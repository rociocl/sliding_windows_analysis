#!/usr/bin/env python

import sys
import csv
import importlib
import argparse
import logging
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from gnip_trend_detection.analysis import analyze
from gnip_trend_detection import models
from path import Path

# logging
logger = logging.getLogger("analyze")
if logger.handlers == []:
    fmtr = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
    hndlr = logging.StreamHandler()
    hndlr.setFormatter(fmtr)
    logger.addHandler(hndlr)

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i","--input-file",dest="input_file_name",default=None)
parser.add_argument("-o","--analyzed-file",dest="analyzed_data_file",default=None)
parser.add_argument("-c","--config-file",dest="config_file_name",default="config.cfg",help="get configuration from this file")
parser.add_argument("-v","--verbose",dest="verbose",action="store_true",default=False)
parser.add_argument("-f","--input-folder",dest="input_folder",default=None)
args = parser.parse_args()

# read config file
config = configparser.SafeConfigParser()
config.read(args.config_file_name)
model_name = config.get("analyze","model_name")
model_config = dict(config.items(model_name + "_model"))

if args.verbose:
    logger.setLevel(logging.DEBUG)

model = getattr(models,model_name)(config=model_config)

# set up input
generators = {}

## if the .csv files ar in a folder (-f)
if args.input_folder:
    folder_path = '.'/Path(args.input_folder)
    for csv_path in [f for f in folder_path.listdir('*.csv') if not f.endswith('_analyzed.csv')]:
        generator = csv.reader(open(csv_path))
        new_file_path = csv_path[:-4] + '_analyzed.csv'
        generators[new_file_path] = generator

## if the .csv file is only one (-i)
elif args.input_file_name:
    generator = csv.reader(open(args.input_file_name))
    new_file_path = args.analyzed_data_file if args.analyzed_data_file else args.input_file_name[:-4] + '_analyzed.csv'
    generators[new_file_path] = generator

else:
    generator = [csv.reader(sys.stdin)]
    new_file_path = args.analyzed_data_file if args.analyzed_data_file else 'stdin_analyzed.csv'
    generators[new_file_path] =  generator

for output_file, generator in generators.items():

    # do the analysis
    plotable_data = analyze(generator,model)

    # output
    output = open(output_file,'w')
    writer = csv.writer(output)
    for row in plotable_data:
        writer.writerow(row)
