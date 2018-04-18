import pandas
import json
import math
from path import Path

def sample_selector(folder, sample_csv):
    files = (Path(folder)).listdir('*.json')
    csv = pandas.read_csv(sample_csv, sep=';')
    for (i, trendID, postedTime, name, clasif) in csv.itertuples():
        (Path(folder)/Path(trendID+'.json')).move( '.'/Path(postedTime))

if __name__ == '__main__':
    # jsonconvert('content_polluters_tweets.txt')
    sample_selector('./downloaded_tweets', './trend_sample.csv')
