class HashtagCounter(object):
    def __init__(self, topic_dict, **kwargs):
        self.counter = 0
        self.name = topic_dict['topic']
        self.keywords = topic_dict['keywords']
        self.topic_dict = topic_dict

    def add_tweet(self,tweet):
        if 'trendID' in tweet.keys() and 'id' in self.topic_dict.keys():
            if tweet['trendID'] == self.topic_dict['id']:
                self.counter += 1
                return
        for k in self.keywords:
            if k in tweet['body'].lower():
                self.counter += 1
                break

    def get(self):
        return [(self.counter,self.get_name())]
    def get_name(self):
        return (self.topic_dict['id'], self.name)
    def combine(self,new):
        self.counter += new.counter

measurement_class_list = [HashtagCounter]
