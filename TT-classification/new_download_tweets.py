import sys
import urllib.request
import re
import json

from bs4 import BeautifulSoup

cache = {}
for line in open(sys.argv[1]):
    fields = line.rstrip('\n').split('\t')
    sid = fields[0]
    uid = fields[2]

    #url = 'http://twitter.com/%s/status/%s' % (uid, sid)
    #print "debug: "+uid+"  "+sid+"\n" 

    tweet = None
    text = "Not Available"
    if sid in cache.keys():
        text = cache[sid]
        #print "debug1"+text+"\n"
    else:
        try:
            # get status page
            f = urllib.request.urlopen("http://twitter.com/%s/status/%s" % (uid, sid))
            # parse with Beautiful soup
            html = f.read().replace("</html>", "") + "</html>"
            soup = BeautifulSoup(html)
            #small elements contain the status ids
            small = soup.select("small > a")
            #p elements next to small elements have the tweet content
            p = soup.find_all("p", attrs={'class' : "js-tweet-text"})
            # search for the tweet with the correct status id.
            for i in range(len(small)):
                #print small[i]
                regex=re.escape(sid)
                if re.search(regex,str(small[i])):
                    text= p[i].get_text()
                    cache[sid]=text
                    break
        except Exception as e:
            print("ERROR:", str(e))
            continue
    text = text.replace('\n', ' ',)
    text = re.sub(r'\s+', ' ', text)
    #print json.dumps(tweet, indent=2)
    print( "\t".join(fields + [text]).encode('utf-8'))

