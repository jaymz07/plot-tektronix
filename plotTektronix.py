# -*- coding: utf-8 -*-
"""
Created on Tue May  2 22:45:01 2017

@author: jaymz
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os


fileInputs = []
pngOutput = False


for i in range(1,len(sys.argv)):
    if(sys.argv[i] == '-png'):
        pngOutput=True
    elif(sys.argv[i] == '*'):
        for f in os.listdir('.'):
            fileInputs.append(f)
    else:
        fileInputs.append(sys.argv[i])
if(len(sys.argv)==1):
    fileInputs = ['/home/jaymz/Documents/RA Stuff/vernier/oscData/FT3/tek0000CH4.csv']
    
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
    for key in dataOut.keys():
        dataOut[key]=np.array(dataOut[key])
    return dataOut
    
for f in fileInputs:
    dat = getFileData(f)
    labels = dat.keys()
    labels.remove('time')
    for l in labels:
        plt.plot(dat['time'],dat[l],label=l)
    plt.title(f)
    plt.legend()
    plt.show()
    
