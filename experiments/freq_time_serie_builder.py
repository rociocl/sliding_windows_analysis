import json
from datetime import datetime
import csv
import os
from path import Path
from utils import get_topic_name

tformat = '%Y-%m-%d %H:%M:%S'
tformat2 = '%Y%m%d%H%M%S'

def read(name,path):
    data=[]
    with open(path+'/'+name) as f:
        for i in f:
            t = json.loads(i)
            t["postedTime_t"] = datetime.strptime(t["postedTime"], tformat)
            t["nameID"]=os.path.splitext(name)[0]
            data.append(t)
    #return list(sorted(data, key=lambda x: x["postedTime_t"]))
    return data

def read_all(path='.'):
    l=list(filter(lambda x: os.path.splitext(x)[1]=='.json',os.listdir(path)))
    data=[]
    for i in l:
        data+=read(i,path)
    return list(sorted(data, key=lambda x: x["postedTime_t"]))

def build_intervals(data,k):
    gap = data[-1]["postedTime_t"]-data[0]["postedTime_t"]
    interv=gap/k
    ptr = data[0]["postedTime_t"]+interv
    intervals=[]
    add=[]
    for i in range(len(data)-1):
        if data[i]["postedTime_t"]<ptr:
            add.append(data[i])
        else:
            intervals.append(add)
            add=[data[i]]
            ptr+=interv
    if ptr<data[-1]["postedTime_t"]:
        intervals.append([data[-1]])
    else:
        intervals[-1].append(data[-1])
    return intervals,interv

def process(k,path='.',out='.'):
    k+=1
    data=read_all(path)
    data,interv=build_intervals(data,k)
    beg = data[0][0]["postedTime_t"]
    names={}
    cont=[]
    for n,i in enumerate(data):
        cont_file = {}
        for j in i:
            if not(j["nameID"] in names):
                names[j["nameID"]]=[]
            if j["nameID"] in cont_file:
                cont_file[j["nameID"]]+=1
            else:
                cont_file[j["nameID"]]=1
        cont.append(cont_file)


    for n,i in enumerate(cont):
        for key in names.keys():
            if key in i:
                names[key].append(i[key])
            else:
                names[key].append(0)
    Path(out).makedirs_p()
    for key,inf in names.items():
        with open(out+'/'+'ts_'+key+'.csv','w') as f:
            for n,j in enumerate(inf):
                strt=[(beg+n*interv).strftime(tformat2),str(int(interv.total_seconds())),str(j),get_topic_name(key)]
                f.write(','.join(strt)+'\n')


if __name__ == '__main__':
    import fire
    fire.Fire()