IDEAS BÁSICAS
======

* **Step1**: Tener una carpeta con los *<tweet_id>.json* que se desean analizar

* **Step2**: Generar el *<trends>.json* que contenga la información de cada una de las tendencias que contiene la carpeta

`[experiments] $ python utils.py -f trends`

* **Step1**: Generar las series de tiempo de frecuencia de cada tendencia (*dia/hora/minuto*)

`[Gnip-Analysis-Pipeline] $ python tweet_time_series_builder.py -c my_measurements.py -f <input_folder> -t <trends_file.json> -o <output_folder> -b <window_size>`

* **Step2**: Generar las series de tiempo de eta de cada tendencia con el trend analysis (*dia/hora/minuto*) cambiando el archivo de configuración

`[Gnip-Trend-Detection] $ python trend_analyze.py -c <config_file.cfg> -f <input_folder>`

* **Step3**: Plotear los resultados

`[Gnip-Trend-Detection] $  python trend_plot.py -c <config_file.cfg> -f <input_folder> -s <styles_file.json>`


EXPERIMENTO # 1: Análisis de los resultados de un SDT al variar el tamaño de la ventana de tiempo
======

El corpus abarca 7 días, con un total de 1036 tendencias. Se tomaron aleatoriamente 10 tendencias por día y se corrió el algoritmo con tamaños de ventana de 1 día, 1 hora y 1 minuto

**OBJETIVO**: Observar cómo varían los resultados al cambiar la configuración de la ventana de tiempo

EXPERIMENTO # 2: Determinar el K óptimo, siendo k el tamaño de ventana
======
Probar con el corpus total cual es el mejor tamaño de ventana
 python experiment_2.py experiment_2 100 1000 experiment_1/20110304 ../Gnip-Trend-Detection/config_files/config_k_days.cfg


**MIN**: 60 segundos - 1min
**MAX**: 86400 segundos - 1día

EXPERIMENTO # 3: Análisis de como K varía según las características del dataset
======

EXPERIMENTO # 3.1: Variación del K según el conjunto de tópicos seleccionados
------

python experiments.py experiment 10 1001 experiment_3/201103_meme ../Gnip-Trend-Detection/config_files/config_k_days.cfg


EXPERIMENTO # 3.2: Variación del K según el segemento de tiempo en que se analicen los tópicos
------
