import pandas
import json
import math
from path import Path
import random
import argparse
from dateutil.parser import parse as dt_parser

from dateutil.parser import parse as dt_parser20110307

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
lines = ['--', '-.', ':', '.', ',']
CORPUS_DATE_FORMAT = '%Y%m%d'

CORPUS_PATH = './TT-annotations.csv'
CORPUS_CSV =  pandas.read_csv(CORPUS_PATH, sep=';', header=None)

def get_topic_info(topic_id):
    return CORPUS_CSV[CORPUS_CSV.iloc[:,0] == topic_id].values[0]

def get_topic_name(topic_id):
    return get_topic_info(topic_id)[2]

def evaluation(input_folder, output_file):

    analyzed_files = (Path(input_folder)).listdir('*analyzed.csv')
    REL = len(analyzed_files)
    REC = 0
    RR = 0
    ARI = 0
    BRI = 0
    for f_path in analyzed_files:
        topic_id = f_path.basename()[3:-13]

        topic_row = get_topic_info(topic_id)

        detection_time = dt_parser( str(topic_row[1]))
        RR_temp = 0

        for i, wind_time ,count, eta, trend_analysis in pandas.read_csv(f_path, sep=',', header=None).itertuples():
            if trend_analysis == 1:
                REC += 1
                current_time = dt_parser(wind_time)
                if current_time.strftime(CORPUS_DATE_FORMAT) == detection_time.strftime(CORPUS_DATE_FORMAT):
                    RR_temp = 1
                elif current_time < detection_time:
                    BRI +=1
                else:
                    ARI += 1
        RR +=  RR_temp
    NR = REL - RR
    if not Path(output_file).exists():
        header = 'folder,rel,rec,rr,nr,bri,ari,recobrado\n'
        with open(output_file, 'x') as out:
            out.write(header)

    with open(output_file, 'a') as out:
        csv_output = f'{input_folder},{REL},{REC},{RR},{NR},{BRI},{ARI},{RR/float(REL):1.3f}\n'
        out.write(csv_output)


def get_trends(folder, output_file):
    files = (Path(folder)).listdir('*.json')
    trends = []
    styles = {}
    used_colors = []
    with open(output_file, "w") as output:
        for f in files:
            topic_id  = f.basename()[:-5]

            topic_row = get_topic_info(topic_id)

            name = topic_row[2]
            keywords= [name.lower()]
            if len(name.split(' '))> 1:
                keywords.append(name.lower().replace(" ", ""))
            # Color selector
            color = None
            while True:
                color = random.choice(colors)
                if len(used_colors) == len(colors):
                    break
                if not color in used_colors:
                    used_colors.append(color)
                    break

            trends.append( {'id': topic_row[0], 'postedTime':topic_row[1], 'type': topic_row[3] , 'topic': name , 'keywords': keywords})
            styles[topic_row[0]] = {'topic': name, 'color': color}

        output.write(json.dumps({'info': {'trends': trends ,'styles': styles } }))



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Utils functions for trend detection system")
    parser.add_argument('-f','--function',dest='function', default= '', help="function to be used")
    args = parser.parse_args()

    if args.function == 'trends':
        # EXPERIMENT_1
        # get_trends('experiment_1/20110301', 'experiment_1/trend_sample.csv', 'experiment_1/20110301_trends.json')
        # get_trends('experiment_1/20110302', 'experiment_1/trend_sample.csv', 'experiment_1/20110302_trends.json')
        # get_trends('experiment_1/20110303', 'experiment_1/trend_sample.csv', 'experiment_1/20110303_trends.json')
        # get_trends('experiment_1/20110304', 'experiment_1/trend_sample.csv', 'experiment_1/20110304_trends.json')
        # get_trends('experiment_1/20110305', 'experiment_1/trend_sample.csv', 'experiment_1/20110305_trends.json')
        # get_trends('experiment_1/20110306', 'experiment_1/trend_sample.csv', 'experiment_1/20110306_trends.json')
        # get_trends('experiment_1/20110307', 'experiment_1/trend_sample.csv', 'experiment_1/20110307_trends.json')
        pass


    if args.function == 'eval':
        evaluation('experiment_2/201103/k_values/10', 'experiment_2/201103/')
