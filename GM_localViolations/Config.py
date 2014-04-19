'''
@author: ak
'''
from __future__ import division
import math
import numpy as np

#- NODE RANGE
nodeStart=2
nodeEnd=50 #20

#- THRESHOLD RANGE
thresStart=10
thresEnd=1000

#- MEAN RANGE
meanStart=0 #0
meanEnd=20 #20
meanStep=0.5
meanLvsPerIterPlotLim=30
meanReqPerBalPlotLim=100

#- STD RANGE
stdStart=0.5
stdEnd=9 #9
stdStep=0.2
stdLvsPerIterPlotLim=100
stdReqPerBalPlotLim=200





#--------------default values---------------------
#exp config
defIterations=30

#runtime limit(in sec)
timeLimit=5

#default InputStream data
defStatus='static'
defInitXData=0
defInterval=1

#default vel distribution params
defMean=5
defStd=1

#default Node values
defNodeNum=10
defV=0
defWeight=1

#default geometric monitoring params
threshold=1000
defMonFunc= lambda x: x**2



def avgListsOverIters(array2d):
    '''
    function to average list data into a single list
    args:
        array2d: 2d array, rows=experimental iterations to average over
                            columns=iterations till global violation
    '''
    avgList=np.zeros(max(map(len,array2d)))
    for l in array2d:
        for i in range(len(l)):
            avgList[i]+=l[i]
    
    avgList=[x/np.shape(array2d)[0] for x in avgList]
    
    return avgList

def toNdArray(array2d):
    nda=np.zeros(shape=(np.shape(array2d)[0],max(map(len,array2d))))
    for i in range(np.shape(nda)[0]):
        for j in range(np.shape(nda)[1]):
            if j<len(array2d[i][:]):
                nda[i][j]=array2d[i][j]
            else:
                nda[i][j]=0
    return nda

if __name__=='__main__':
    a=[[2,2,2,2,2],[5,5,5],[1,1,1,1,1,1,1],[4,4,4,4]]
    print(avgListsOverIters(a))
    print(type(toNdArray(a)))
        
