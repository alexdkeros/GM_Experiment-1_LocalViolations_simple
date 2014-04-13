'''
@author: ak
'''
import math
import numpy as np

#exp config
defIterations=20
nodeStart=1
nodeEnd=5

#runtime limit(in sec)
timeLimit=5

#default InputStream data
defStatus='static'
defInitXData=0
defMean=5
defStd=1
defInterval=1

#default Node values
defV=0
defWeight=1

threshold=100
defMonFunc= lambda x: x



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
    a=[[2,2,2,2,2],[5,5,5]]
    print(avgListsOverIters(a))
    print(type(toNdArray(a)))
        