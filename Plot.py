'''
Plots user specified exp number, plane, ROI, time frame (in sec), with each stimuli shaded with user specified colors (at the 3rd column of the Stimulus.csv)
Make sure stimulus names don't include ","
'''

import Utility_working as Utility #custom-made utility file, contains lengthy functions
from constant import *
from gettext import install
import numpy as np
import matplotlib.pyplot as plt
import csv
import plotly.express as px
import matplotlib.pyplot as plt
import sys
import os

# if want to customize some varibles, can enter them in terminal (see Unit Test.txt for example)
try:
    planeNumber = sys.argv[1]
    stimStart = sys.argv[2]
    stimEnd = sys.argv[3]
    print(planeNumber,stimStart,stimEnd)
    splPrefix = expNumber + "_" + planeNumber + "_"
    prefix = expNumber + "_" + planeNumber+ " _frm" + str(stimStart) + "-"+ str(stimEnd)+ "_" 
    pathToRaw = "../"+parentFolder+"/Data/"+parentFolder+"_"+planeNumber+"_"
    print("using constants from terminal input: INPUT: ",pathToOutputData + splPrefix +"Smoothed.csv","OUTPUT:",pathToFigure + expNumber+"_" + planeNumber)
except:
    print("Starting Plot.py with variables in constant.py")

# if have a csv. file with ROIs to remove, it will be included in plotting
try:
    AllROIsToRemove = np.loadtxt(pathToData +"BadROIs.csv",delimiter=',',dtype=str)
except:
    AllROIsToRemove = np.zeros((3, 6))
    print("plotting all ROIs specified in constant.py")

# if Figure folder do not exist, create one
if not os.path.exists(pathToFigure[:-1]):
    os.makedirs(pathToFigure[:-1])

# import raw data, normalized data, and smoothed data
splPATH = pathToOutputData + splPrefix
smoothed = np.loadtxt(splPATH +"Smoothed.csv",delimiter=',',dtype=str)
stimulus = np.loadtxt(pathToData +"Stimulus.csv",delimiter=',',dtype=str,usecols = (0,1,2,3))
AllThresholds = np.loadtxt(pathToOutputData + splPrefix +"AllThresholds.csv",delimiter=',',dtype=str)

TotalTime = smoothed.shape[0]-1
TotalROIs = smoothed.shape[1]-1
print("plotting experiment ",expNumber, "plane ",planeNumber,"with ",TotalROIs,"ROIs")

if str(ROIs) == "all":
    # arrange(x,y) -> [x,y), so end has to be TotalROIs+1 to include the last ROI
    ROIs = np.arange(1,TotalROIs+1)
if str(stimEnd) == "all" or str(stimStart) == "all":
    stimStart = 1
    stimEnd = TotalTime
elif int(stimEnd) > TotalTime:
    stimEnd = TotalTime

stimStart = int(stimStart)
stimEnd = int(stimEnd)

# remove unwanted ROIs, trim to only a time window of interest
ROIsToRemove=Utility.getROIsToRemove(debug, AllROIsToRemove, plane = planeNumber)
# extract only the wanted ROIs and crop recording to desired time frames
ROIsmoothed = Utility.extractData(debug, smoothed, ROIs, stimStart = stimStart, stimEnd = stimEnd)
ROIs = ROIsmoothed[0,1:]

# range(x,y) -> [x,y), so end has to be len(ROI)+1 to include the last ROI
for i in range(1,len(ROIs)+1):
    ROI = str(ROIs[i-1])[4:]

    # rawROIdata = ROIdata[1:,i].astype(float, copy=False)
    # rawNormalized = ROInormalized[1:,i].astype(float,copy=False)
    rawSmoothed = ROIsmoothed[1:,i].astype(float,copy=False)
    try:
        thisThreshold = AllThresholds[i]
    except:
        thisThreshold = 0.5
    if debug:
        print("ROI =",ROI)
        print("i =",i)

    fig = plt.figure() 
    ax = fig.add_subplot()
    fig.set_size_inches(25, 3)
    plt.title(expNumber + " "+planeNumber +" ROI=" + ROI)
    plt.xlabel("Time (sec)")
    plt.plot(np.arange(stimStart, stimEnd, step = 1)/fps,rawSmoothed)
    plt.tight_layout()

    #draw a line at y = 0.5 for threshold
    plt.axhline(y=float(thisThreshold), color='r', linestyle='-')

    if debug:
        print("plotting with threshold =",thisThreshold)
    
    #makr each stimulus with shadings
    for i in range(0,stimulus.shape[0]):
        stimName = stimulus[i,0]
        start = int(float(stimulus[i,1]))/fps
        end = int(float(stimulus[i,2]))/fps
        #try to find color in Stimulus.csv
        #if fail (not provided), default to grey
        try:
            color = stimulus[i,3]
        except:
            color = "grey"
            if debug:
                print("no color provided in Stimulus.csv. Color defaulted to grey")
        stimNum = stimulus.shape[0]

        if debug:
            print("for stimulus:",stimName ,", stimStart =",start,"stimEnd =",end,"color is",color)
        if start >= stimStart/fps and end <= stimEnd/fps:
            plt.axvspan(start, end, alpha=0.3, color=color) 

    plt.savefig(pathToFigure + expNumber+"_" + planeNumber + "_ROI" + ROI + "_Frm"+str(stimStart) + "-" + str(stimEnd) + ".png")
    plt.grid()
    # plt.show()
    plt.close("all")