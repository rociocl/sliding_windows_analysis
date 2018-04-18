#!/usr/bin/env python

import pprint
import sys
import argparse
import importlib
import logging
import csv
import json
from path import Path

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from gnip_trend_detection.analysis import analyze
from gnip_trend_detection.analysis import plot
from gnip_trend_detection.new_plot import multi_plot

logger = logging.getLogger("plot")
if logger.handlers == []:
    fmtr = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
    hndlr = logging.StreamHandler()
    hndlr.setFormatter(fmtr)
    logger.addHandler(hndlr)

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input-file",dest="input_file_name",default=None)
parser.add_argument("-f","--input-folder",dest="input_folder_name",default=None)
parser.add_argument("-c","--config-file",dest="config_file_name",default="config.cfg",help="get configuration from this file")
parser.add_argument("-t","--plot-title",dest="plot_title",default=None)
parser.add_argument("-o","--output_file_name",dest="output_file_name",default=None)
parser.add_argument("-v","--verbose",dest="verbose",action="store_true",default=False)
parser.add_argument("-s","--styles_file",dest="styles_file", default=None)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config_file_name)

# manage config parameters that can be overwritten with cmd-line options
if args.plot_title is not None:
    config.set("plot","plot_title",args.plot_title)
if args.output_file_name is not None:
    # strip off extension
    if len(args.output_file_name.split('.')) > 1:
        args.output_file_name = '.'.join( args.output_file_name.split('.')[:-1] )
    config.set("plot", 'plot_dir', args.output_file_name)


if args.verbose is True:
    logger.setLevel(logging.DEBUG)

input_generators = []
styles = []

if args.input_folder_name:
    folder_path = '.'/Path(args.input_folder_name)
    config.set("plot", 'plot_dir', folder_path)

    fd = open(args.styles_file, "r")
    dic = json.load(fd)
    styles_info = dic['info']['styles']
    fd.close()

    for csv_path in folder_path.listdir('*_analyzed.csv'):
        input_generators.append(csv.reader(open(csv_path)))

        trend_id = csv_path.basename()[3:-13]
        styles.append((styles_info[trend_id]['topic'],
                       styles_info[trend_id]['color']))

elif args.input_file_name:
    input_generators.append(csv.reader(open(args.input_file_name)))
else:
    input_generators.append(csv.reader(sys.stdin))

multi_plot(input_generators, config, styles)
