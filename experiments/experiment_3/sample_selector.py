import pandas
import json
import math
from path import Path

def sample_selector(folder, sample_csv):
    files = (Path(folder)).listdir('*.json')
    csv = pandas.read_csv(sample_csv, sep=';')
    for (i, trendID, postedTime, name, clasif) in csv.itertuples():
        out_folder = folder/Path(clasif)
        if not out_folder.exists():
            out_folder.mkdir()
        (Path(folder)/Path(trendID+'.json')).move(out_folder)

if __name__ == '__main__':
    # jsonconvert('content_polluters_tweets.txt')
    sample_selector('201103', 'trend_sample.csv')
