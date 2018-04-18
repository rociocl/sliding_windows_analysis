
# $ python2 uh_stream_download.py 0_tweets/


# Variables that contains the user credentials to access Twitter API
CONSUMER_KEY = "OkLbVQj3sjL8i7Sn4HuUZgwK2"
CONSUMER_SECRET = "iG6SvX4XbHBnB3PMdpeps0jDuGmFxtehnBOER5R1G6dTjBPD3P"
ACCESS_TOKEN = "892872231092711424-iGPDALOcH1IAtTXl78C61rMIUrgEz2h"
ACCESS_SECRET = "DWfCsfMsl88SPJKaEEicZM4TZuYu4BiuohprCBUVwbQNY"

from  twython import Twython
import sys
import re
import os
import time
import json
import datetime


def get_json_tweet(tweet_id, user_id, twitter):
    tweet = twitter.show_status(id=tweet_id)
    text = tweet['text']
    text = text.replace('\n', ' ',)
    text = re.sub(r'\s+', ' ', text)
    date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    json_tweet = {}
    json_tweet['postedTime'] = date_str
    json_tweet['body'] = text
    json_tweet["userID"] = user_id
    json_tweet["tweetID"] = tweet_id
    return json_tweet


twitter = Twython( CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
path = sys.argv[1]


dirs = [path+d for d in os.listdir(path) if not d.endswith('.json')]

for trend_path in dirs:
    print('\n[STARTING] '+ trend_path)
    cache = []
    errors_count = 0
    lines_count = 0
    output_file = open(trend_path + '.json','w')

    for line in open(trend_path):
        lines_count += 1
        fields = line.rstrip('\n').split('\t')
        tweet_id = fields[0]
        user_id = fields[2]

        if not tweet_id in cache:
            json_tweet = {}
            cache.append(json_tweet)

            while True:
                try:
                    json_tweet = get_json_tweet(tweet_id, user_id, twitter)
                    json_tweet['trendID'] = os.path.basename(trend_path)
                    output_file.write(json.dumps(json_tweet)+'\n')
                    break

                except Exception as e:
                    if str(e) == 'Twitter API returned a 429 (Too Many Requests), Rate limit exceeded':
                        print('[WAITING] [LINE '+ str(lines_count) +']....Too Many Requests ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                        time.sleep(300)
                        print('[RESUMING] ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                    else:
                        errors_count +=1
                        json_tweet = {}
                        break


    output_file.close()
    print('[REMOVING] '+ trend_path)
    os.remove(trend_path)
    print('[COMPLETED] '+trend_path+': '+ str(errors_count)+'/'+str(lines_count))

