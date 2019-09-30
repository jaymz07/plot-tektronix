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
dumpMode = None


for i in range(1,len(sys.argv)):
    if(sys.argv[i] == '-png'):
        pngOutput=True
    elif(sys.argv[i-1] == '-c'):
        print('Settting plot chunksize to ' + sys.argv[i])
        matplotlib.rcParams['agg.path.chunksize'] = int(sys.argv[i])
    elif(sys.argv[i] == '-d'):
        print('Dumping data\n')
        dumpMode = 'tab'
    elif(sys.argv[i] == '--help'):
        print("\nOptions:\n\n-png\n\tWrite directly to png file\n-d\n\tDump directly to tab separated file.\n-c [chunk size]\n\tPlot every [chunk size] points.")
        sys.exit()
    elif(sys.argv[i] not in ['-c','-png','-d']):
        fileInputs.append(sys.argv[i])

#Default file input if run without arguments
if(len(sys.argv)==1):
    fileInputs = ['tek0000.csv']

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
                if(channelLabels[j-1] in dataOut):
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

def dumpFileData(data, fName):
    fHandle = open(fName, 'w')
    keys = list(data.keys())
    keys.remove('time')
    fHandle.write('#time')
    for key in keys:
        fHandle.write('\t' + key.replace('\n',''))
    fHandle.write('\n')
    for i in range(0, len(data['time'])):
        fHandle.write('%0.12f' % data['time'][i])
        for key in keys:
            fHandle.write('\t%0.12f' % data[key][i])
        fHandle.write('\n')
    fHandle.close()

for f in fileInputs:
    print('---------------------------------------\n--> Opening file :' + f )
    dat = getFileData(f)
    if(dumpMode is not None):
        if(dumpMode == 'tab'):
            ds = f.split('.')
            ext = None
            if(len(ds) > 1):
                ext = '.' + ds[-1]
            if(ext is None):
                fName = f + '_tabSep'
            else:
                fName = f.replace(ext,'_tabSep'+ext)
            print("Mode set to tab separated. Dumping data to " + fName)
            dumpFileData(dat,fName)
        print("\n\nExiting :)\n\n")
        sys.exit()
    print("--> Plotting %d points" % len(dat['time']))
    labels = list(dat.keys())
    labels.remove('time')
    fig, axes = plt.subplots(len(labels),sharex=True)
    if(not isinstance(axes,np.ndarray)):
        axes.plot(dat['time'],dat[labels[0]],label=labels[0])
        axes.legend()
    else:
        for i in range(0,len(labels)):
            axes[i].plot(dat['time'],dat[labels[i]],label=labels[i])
            axes[i].legend()
    plt.title(f)
    if(not pngOutput):
        plt.show()
    else:
        outFig = f.replace('.csv','.png')
        print('Saving file to : ' + outFig)
        plt.savefig(outFig)
