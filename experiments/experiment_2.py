from freq_time_serie_builder import process
from utils import get_trends, evaluation
from path import Path
import subprocess
import enlighten


def experiment_2(min_k=10, max_k=1500, input_folder='experiment_2/201103', config_file='../Gnip-Trend-Detection/config_files/config_k.cfg'):

    print('Step1: generate trends dict and styles')
    get_trends(input_folder, f'{input_folder}_trends.json')

    print(f'Step2: generate freq and eta time series from {min_k} to {max_k} k values')
    manager =  enlighten.Manager()
    counter = manager.counter()
    for i in range(min_k,max_k):
        out_folder = f'{input_folder}/k_values/{i}'

        if Path(out_folder).exists():
            continue

        process(i, input_folder, out_folder)
        print(f'... generated {i} FTS' )

        subprocess.run(['python','../Gnip-Trend-Detection/trend_analyze.py','-c',config_file,'-f', out_folder])
        print(f'... generated {i} ETS' )

        subprocess.run(['python','../Gnip-Trend-Detection/trend_plot.py','-c',config_file,'-f', out_folder, '-s', f'{input_folder}_trends.json'])
        print(f'... plotting {i}' )

        evaluation(out_folder, f'{input_folder}/k_values/evaluation.csv')
        print(f'... evaluation {i}' )

        counter.update()



if __name__ == '__main__':
    import fire
    fire.Fire()