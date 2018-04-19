import pandas
import json
import math
from path import Path
import random
import argparse
from dateutil.parser import parse as dt_parser
import os
import matplotlib.pyplot as plt


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
        header = 'k,folder,rel,rec,rr,nr,bri,ari,recobrado,precision\n'
        with open(output_file, 'x') as out:
            out.write(header)

    with open(output_file, 'a') as out:
        csv_output = f'{Path(input_folder).basename()},{input_folder},{REL},{REC},{RR},{NR},{BRI},{ARI},{RR/float(REL):1.3f},{RR/float(RR + BRI):1.3f}\n'
        out.write(csv_output)

def f1(precision,recall):
    return 2*(precision*recall)/(precision+recall)

def f2(precision, recall):
    return 5*(precision*recall)/4*(precision+recall)


def eval_file(eval_file):
    csv = pandas.read_csv(eval_file)
    ks = csv['k']
    pre = csv['precision']
    rca = csv['recobrado']
    f1_values = f1(pre,rca)
    f2_values = f2(pre,rca)
    max_index = f1_values.argmax()
    return {'file': eval_file, 'precision': pre, 'recall': rca, 'f1': f1_values, 'f2': f2_values, 'k':ks, 'better_k':ks[max_index], 'better_index':max_index}

def evaluation_analysis(root_dir='experiment_2/'):
    eval_csvs = []
    for root, subdirs, files in os.walk(root_dir):
        eval_csvs.extend([os.path.join(root, x) for x in files if x.startswith('evaluation.csv')])
    cols = 2 if len(eval_csvs)>1 else 1
    rows = len(eval_csvs)/cols if len(eval_csvs)%cols == 0 else len(eval_csvs)/cols +1
    fig1 = plt.figure()
    fig2 = plt.figure()
    fig3 = plt.figure()
    box = {'facecolor' : '.75', 'edgecolor' : 'k','boxstyle': 'round'}

    for i, csv in enumerate(eval_csvs):

        title = Path(csv).dirname().split('/')
        title= f'{title[len(title)-3]}: {title[len(title)-2]}'

        analysis = eval_file(csv)
        # F1 and F2 plot
        ax1 = fig1.add_subplot(rows, cols, i + 1)
        ax1.set_title(title)

        ax1.plot(analysis['k'],analysis['f1'], 'm', label='f1', alpha=0.5)
        ax1.plot(analysis['k'],analysis['f2'], 'g', label='f2', alpha=0.5)
        ax1.axvline(x=analysis['better_k'], color='k', label='k')
        ax1.set_ylim(0,3)
        ax1.text(analysis['better_k'], 0, str(analysis['better_k']), bbox = box, horizontalalignment='center')


        # Pre and Rca plot
        ax2 = fig2.add_subplot(rows, cols, i + 1)
        ax2.set_title(title)

        ax2.plot(analysis['k'],analysis['recall'], 'b', label='recall', alpha=0.5)
        ax2.plot(analysis['k'],analysis['precision'], 'r', label='precision', alpha=0.5)
        ax2.axvline(x=analysis['better_k'], color='k')
        ax2.set_ylim(0,1.2)
        ax2.text(analysis['better_k'], 0, str(analysis['better_k']), bbox = box, horizontalalignment='center')


        # Pre vs. Rca curve plot
        ax3 = fig3.add_subplot(rows, cols, i + 1)
        ax3.set_title(title)

        ax3.plot(analysis['recall'],analysis['precision'], '.--b', label='pres vs. recall', alpha=0.5)
        ax3.set_ylim(0,1.2)
        ax3.set_xlim(0,1)

    pos = 'lower center' if len(eval_csvs) ==1 or len(eval_csvs)%2 == 0 else 'lower right'

    fig1.subplots_adjust(wspace=0.3, hspace=1.0)
    fig1.legend(['f1 score', 'f2 score', 'better k' ], loc=pos, ncol=3)
    fig1.savefig(Path(root_dir)/Path('eval_fscores.png'))

    fig2.subplots_adjust(wspace=0.3, hspace=1.0)
    fig2.legend(['recall', 'precision'], loc=pos, ncol=2)
    fig2.savefig(Path(root_dir)/Path('eval_pre&rca.png'))

    fig3.subplots_adjust(wspace=0.8, hspace=1.0)
    fig3.legend(['recall(x) precision(y) curve'], loc=pos, ncol=1)
    fig3.savefig(Path(root_dir)/Path('eval_preVSrca.png'))


# def update_evaluation(input_file):
#     csv = pandas.read_csv(input_file, sep=',')
#     rr = csv['rr']
#     bri = csv['bri']
#     pre = rr / (rr+bri)
#     csv.insert(8, 'precision', pre)
#     csv.to_csv(input_file, columns=['folder','rel','rec','rr','nr','bri','ari','recobrado','precision' ], float_format='%1.3f', index=False)


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
    import fire
    fire.Fire()
