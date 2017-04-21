'''
Created on 21 avr. 2017

@author: Adnene
'''
#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import colors,markers
import six
import ntpath
from os.path import basename, splitext, dirname


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# The test result file contains is a csv file containing 4 columns
# progName
# nbObject
# nbDistinctObject
# nbClosed
# execTimes separated by ';'
# plot by numObjects ignoring the filenames
FONTSIZE = 27
LEGENDFONTSIZE = 20
MARKERSIZE = 10
LINEWIDTH = 8
FIGSIZE=(12, 5.3)
BAR_LOG_SCALE=False
TIME_LOG_SCALE=False
LEGEND=True

optNames={(True,True,1):"DSC+UB1",(True,True,2):"DSC+UB2",(True,False):"CLOSED",(False,True,1):"UB1",(False,True,2):"UB2",(False,False):"BASELINE"}
optNamesReversed={v:k for k,v in optNames.iteritems()}
colorByOpt =  {"DSC+UB1":"green","DSC+UB2":"cyan", "CLOSED" : "blue", "UB1":"red","UB2":"magenta", "BASELINE":"orange"}
markerByOpt = {"DSC+UB1":"D","DSC+UB2":"D", "CLOSED" : "^", "UB1":"o","UB2":"o", "BASELINE":"o"}
lineTypeByOpt = {"DSC+UB1":"-","DSC+UB2":"-", "CLOSED" : "-", "UB1":"--","UB2":"--", "BASELINE":"-"}
hatchTypeByOpt = {"DSC+UB1":"","DSC+UB2":"", "CLOSED" : "....", "UB1":"///","UB2":"///", "BASELINE":"x"}

dict_map={'attr_items':'#attr_items','attr_users':'#attr_users','attr_aggregate':'#attr_group','#attr_items':'#attr_objects','#items':'#objects','#users1':'#users' ,'#users2':'#users','sigma_context':'thres_objects','sigma_u1':'thres_users','sigma_u2':'thres_users','sigma_quality':'thres_quality'}


def PlotPerf(testResultFile, var_column, activated = list(optNames.values()), plot_bars = True, plot_time = True) :
    if not plot_bars and not plot_time : raise Exception("Are you kidding me ?")
    fileparent = dirname(testResultFile)
    filename = splitext(basename(testResultFile))[0]
    exportPath = (fileparent+"/" if len(fileparent) > 0 else "")+filename+".pdf"
    basedf = pd.read_csv(testResultFile,sep='\t',header=0)
    xAxis = np.array(sorted(set(basedf[var_column])))
    xAxisFixed = range(1,len(xAxis)+1)
    xAxisMapping = {x:i for (x,i) in zip(xAxis,xAxisFixed)}
    optCount = len(activated)
    barWidth = np.float64(0.7/optCount)
    offset = -barWidth*(optCount-1)/2
    fig, baseAx = plt.subplots(figsize=FIGSIZE)
    baseAx.set_xlabel(dict_map.get(var_column,var_column),fontsize=FONTSIZE)
    baseAx.set_xlim([0,max(xAxisFixed)+1])
    baseAx.tick_params(axis='x', labelsize=FONTSIZE)
    baseAx.tick_params(axis='y', labelsize=FONTSIZE)

    
    
    if plot_bars : 
        barsAx = baseAx
        barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
        barsAx.set_ylabel("#Explored",fontsize=FONTSIZE)
        if BAR_LOG_SCALE : barsAx.set_yscale("log")
        barsAx.set_xlabel(dict_map.get(var_column,var_column),fontsize=FONTSIZE)
        #barsAx.set_ylim([0,1.2*np.amax(basedf["#all_visited_context"])])
        barsAx.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

    if plot_time :
        if plot_bars :
            timeAx = baseAx.twinx()
            timeAx.yaxis.tick_left()
            timeAx.yaxis.set_label_position("left")
            barsAx.yaxis.tick_right()
            barsAx.yaxis.set_label_position("right")
        else :
            timeAx = baseAx  
        timeAx.set_ylabel("Execution time (s)",fontsize=FONTSIZE)    
        if TIME_LOG_SCALE : timeAx.set_yscale("log")
        timeAx.tick_params(axis='y', labelsize=FONTSIZE)
        timeAx.set_xlim([0,max(xAxisFixed)+1])

    plt.xticks(xAxisFixed,xAxis)

    for optName in activated:
        optConstraint = optNamesReversed[optName]
        df = basedf[basedf["closed"]==optConstraint[0]]
        df = df[df["prune"]==optConstraint[1]]
        if len(optConstraint) > 2 :
            df = df[df["upperbound_type"]==optConstraint[2]]
        varVector = np.array(df[var_column])
        distinctVarVector = sorted(set(varVector))
        distinctVarVectorFixed = [xAxisMapping[x] for x in distinctVarVector]
        nbVisitedVector = np.array(map(np.mean, [df[df[var_column]==element]["#all_visited_context"] for element in distinctVarVector]))
        execTimeVector = np.array(map(np.mean, [df[df[var_column]==element]["#timespent"] for element in distinctVarVector]))
        execMeanTimeVector = execTimeVector
        execErrorTimeVector = 0
        if len(distinctVarVectorFixed)>0:
            if plot_bars : barsAx.bar(distinctVarVectorFixed+offset, np.array([x for x in nbVisitedVector]), hatch= hatchTypeByOpt[optName], width = barWidth, align='center', color= colorByOpt[optName],label=optName)
            if plot_time : timeAx.errorbar(distinctVarVectorFixed, execMeanTimeVector, yerr = execErrorTimeVector,fmt = lineTypeByOpt[optName]+markerByOpt[optName], linewidth=LINEWIDTH,markersize=MARKERSIZE,label=optName, color= colorByOpt[optName])
            if LEGEND : 
                legend = timeAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE) if plot_time else barsAx.legend(loc='upper left', shadow=True, fontsize=LEGENDFONTSIZE)
        offset+=barWidth
    fig.tight_layout()
    plt.savefig(exportPath)
    #plt.show()

if __name__ == "__main__" :
    PlotPerf(sys.argv[1],sys.argv[2],plot_bars=sys.argv[3]=="True",plot_time=sys.argv[4]=="True",activated=sys.argv[5:])
    #plot("nb_items.csv","#items",activated = ["DSC+UB1", "CLOSED"], plot_bars = True, plot_time = True)