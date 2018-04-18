import datetime
import argparse
import collections
import operator
import importlib
import logging
import os
import sys
# import datetime_truncate
from math import log10, floor
from dateutil.parser import parse as dt_parser
import seaborn as sns
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.dates as mdates
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt
import seaborn as sns
from .time_bucket import TimeBucket
import random

def multi_plot(input_generators,config, styles=[]):
    """
    input_generators is a list and each element is a  generator of tuples with the following structure:
        (time_interval_start, count, eta, trend)
    """

    # if this throws a configparser.NoSectionError,
    # then let it rise uncaught, since nothing will work
    plot_config = config['plot']

    # get parameters and set defaults
    logscale_eta = plot_config.getboolean('logscale_eta',fallback=False)
    use_x_var = plot_config.getboolean('use_x_var',fallback=True)
    do_plot_parameters = plot_config.getboolean('do_plot_parameters',fallback=False)
    legend = plot_config.getboolean('legend',fallback=False)
    start_tm = dt_parser( plot_config.get("start_time","1900-01-01") )
    stop_tm = dt_parser( plot_config.get("stop_time","2050-01-01") )
    rebin_factor = plot_config.getint("rebin_factor",fallback=1)

    rebin_config = dict(config.items("rebin"))
    plot_config["x_unit"] = "{0:d} {1:s}" .format( int(rebin_config["n_binning_unit"]) * rebin_factor, rebin_config["binning_unit"])


    """
    # only useful if we revive 'counter_name' parameter
    if 'counter_name' in rebin_config:
        if plot_config["plot_title"] == "":
            plot_config["plot_title"] = rebin_config["counter_name"]
        if plot_config["plot_file_name"] == "":
            plot_config["plot_file_name"] = rebin_config["counter_name"]
    """

    # build the plotting surface

    fig,(ax1, ax2, ax3) = plt.subplots(3,sharex=True)
    max_cts = 0
    min_cts = sys.maxsize
    max_eta = 0
    min_eta = sys.maxsize
    used_colors = []

    for index, input_generator in enumerate(input_generators):

        data = [(dt_parser(tup[0]),float(tup[1]),float(tup[2]), float(tup[3])) for tup in input_generator if dt_parser(tup[0]) > start_tm and dt_parser(tup[0]) < stop_tm ]

        if rebin_factor <= 1:
            tbs = [tup[0] for tup in data]
            cts = [tup[1] for tup in data]
            eta = [tup[2] for tup in data]
            # trends:
            #  -1 = 'decreasing'
            #   0 = 'no trend'
            #   1 = 'increasing'
            trends = [random.uniform(0.5, 1.0) if tup[3] == 1 else 0 for tup in data]
        else:
            tbs = []
            cts = []
            eta = []
            trends = []
            tbs_tmp = None
            cts_tmp = 0
            eta_tmp = 0
            trend_tmp = 0
            counter = 0
            for tbs_i, cts_i, eta_i, trend_i in data:
                tbs_tmp = tbs_i
                cts_tmp += cts_i
                eta_tmp += eta_i
                trend_tmp += 1 if trend_i == 1 else 0

                counter += 1
                if counter == rebin_factor:
                    counter = 0
                    tbs.append(tbs_tmp)
                    cts.append(cts_tmp)
                    eta.append(eta_tmp/float(rebin_factor))
                    trends.append(trend_tmp)
                    tbs_tmp = None
                    cts_tmp = 0
                    eta_tmp = 0
                    trend_tmp = 0


        if cts == []:
            sys.stderr.write("'cts' list is empty\n")
            continue
            # return -1
        max_cts = max(max_cts, max(cts))
        min_cts = min(min_cts, min(cts))

        ## PLOTTING PART

        color = styles[index][1]

        # plot the counts
        if use_x_var:
            ax1.plot(tbs, cts, color, alpha=0.7)
        else:
            ax1.plot(cts, color, alpha=0.7)
            ax1.set_xlim(0,len(cts))

        # plot the etas
        plotter="plot"
        if logscale_eta:
            plotter="semilogy"
        if use_x_var:
            getattr(ax2,plotter)(tbs,eta, color, alpha=0.7)
        else:
            getattr(ax2,plotter)(eta, color, alpha=0.7)
            ax2.set_xlim(0,len(eta))

        max_eta = max(max_eta, max(eta))
        min_eta = min(min_eta, min(cts))


        # plot the trends
        if use_x_var:
            ax3.plot(tbs,trends, color+'.', alpha=0.7,label=styles[index][0])
        elif trends != []:
            ax3.plot(trends, color+'.', alpha=0.7, label=styles[index][0])
            ax3.set_xlim(0,len(trends))

        for i,t in enumerate(trends):
            if t > 0:
                ax1.axvline(x=tbs[i], color=color, linewidth=0.5, linestyle='--', alpha=0.7)
                ax2.axvline(x=tbs[i], color=color, linewidth=0.5, linestyle='--', alpha=0.7)
                ax3.axvline(x=tbs[i], color=color, linewidth=0.5, linestyle='--', alpha=0.7)

    # adjust spacing
    ax1.set_ylim(min_cts*0.9,max_cts*1.7)
    min_eta = 0
    if min_eta > 0:
        min_eta = min_eta * 0.9
    ax2.set_ylim(min_eta, max_eta*1.1)

    # remove the horizintal space between plots
    plt.subplots_adjust(hspace=0)


    # modify ticklabels
    plt.xticks(rotation=30)
    for tl in ax1.get_yticklabels():
        tl.set_color('k')
        tl.set_fontsize(10)
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
        tl.set_fontsize(10)
    for tl in ax3.get_yticklabels():
        tl.set_color('b')
        tl.set_fontsize(10)
    for tl in ax3.get_xticklabels():
        tl.set_color('k')
        tl.set_fontsize(7)


    # y labels
    y_label = plot_config.get('y_label','counts')
    ax1.set_ylabel(y_label,color='k',fontsize=12)
    ax2.set_ylabel("eta",color='r',fontsize=12)
    ax3.set_ylabel("trend",color='b',fontsize=12)

    ax1.yaxis.set_major_locator(plticker.MaxNLocator(4))
    ax2.yaxis.set_major_locator(plticker.MaxNLocator(5))

    # x date formatting
    # if use_x_var:
    #     day_locator = mdates.DayLocator()
    #     hour_locator = mdates.HourLocator()
    #     day_formatter = mdates.DateFormatter('%Y-%m-%d')
    #     ax2.xaxis.set_major_formatter( day_formatter )
    #     ax2.xaxis.set_major_locator( day_locator )
    #     ax2.xaxis.set_minor_locator( hour_locator )
    #     fig.autofmt_xdate()
    # ax2.set_xlabel("time ({} bins)".format(plot_config["x_unit"].rstrip('s')))

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)

    # build text box for parameter display
    if do_plot_parameters:
        props = dict(boxstyle='round',facecolor='white', alpha=0.5)
        model_name = config['analyze']['model_name']
        model_pars = ""
        for k,v in config[model_name + '_model'].items():
            model_pars += "{}: {}\n".format(k,v)
        text_str = "model: {}\n{}".format(model_name,str(model_pars))
        text_str += 'topics_count: '+str(len(input_generators))
        text_str += '\nrebin_factor: '+ str(rebin_factor)
        ax1.text(0.05,0.95,
                text_str,
                bbox=props,
                verticalalignment='top',
                fontsize=8,
                transform=ax1.transAxes
                )
    if legend:
        ax3.legend(fontsize=5.8, fancybox=True, loc='lower left', title='Topics')

    plt.suptitle(u"{}".format( plot_config.get("plot_title","SET A PLOT TITLE")))

    ## write the image

    plot_file_name = u"{}/{}.{}".format(
            plot_config.get("plot_dir",".").rstrip('/'),
            plot_config.get("plot_file_name","output"),
            plot_config.get("plot_file_extension","png")
            )
    # print("Saved at: " + plot_file_name)
    plt.savefig(plot_file_name)
    plt.close()


