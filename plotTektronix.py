# -*- coding: utf-8 -*-
"""
Created on Tue May  2 22:45:01 2017

@author: jaymz
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys, os


fileInputs = []
pngOutput = False


for i in range(1,len(sys.argv)):
    if(sys.argv[i] == '-png'):
        pngOutput=True
    elif(sys.argv[i-1] == '-c'):
        print 'Settting plot chunksize to ' + sys.argv[i]
        matplotlib.rcParams['agg.path.chunksize'] = int(sys.argv[i])
    elif(sys.argv[i] not in ['-c','-png']):
        fileInputs.append(sys.argv[i])
        
#Default file input if run without arguments
if(len(sys.argv)==1):
    fileInputs = ['/home/jaymz/Documents/RA Stuff/vernier/oscData/FT_HeNeRef/tek0001ALL.csv']
    
def getFileData(fName):
    fHandle = open(fName,'r')
    channelLabels = []
    dataOut = { 'time':[] }
    foundHeader = False
    for line in fHandle:
        if(foundHeader and len(line) > 2):
            vals = line.split(',')
            dataOut['time'].append(float(vals[0]))
            for j in range(1,len(vals)):
                if(dataOut.has_key(channelLabels[j-1])):
                    dataOut[channelLabels[j-1]].append(float(vals[j]))
                else:
                    dataOut[channelLabels[j-1]] = [float(vals[j])]
        if('TIME,CH' in line):
            foundHeader = True
            lvals = line.split(',')
            channelLabels = [st.replace('\r\n','') for st in lvals[1:]]
    fHandle.close()
    for key in dataOut.keys():
        dataOut[key]=np.array(dataOut[key])
    return dataOut

for f in fileInputs:
    print('Opening file :' + f + '\n')
    dat = getFileData(f)
    labels = dat.keys()
    labels.remove('time')
    fig, axes = plt.subplots(len(labels),sharex=True)
    for i in range(0,len(labels)):
        axes[i].plot(dat['time'],dat[labels[i]],label=labels[i])
        axes[i].legend()
    plt.title(f)
    if(not pngOutput):
        plt.show()
    else:
        outFig = f.replace('.csv','.png')
        print('Saving file to : ' + outFig + '\n')
        plt.savefig(outFig)
