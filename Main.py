'''
@author: ak
'''
import uuid
import numpy as np
import matplotlib.pyplot as plt
from GM_localViolations.Coordinator import Coordinator
from GM_localViolations.Node import Node
from GM_localViolations.InputStream import InputStream

if __name__ == '__main__':
    print('--------------experiment start-------------------')
    #experimental results init
    lvsInNodeRange=[]
    itersInNodeRange=[]
    reqsInNodeRange=[]
    lvsPerIterInNodeRange=[]
    reqPerBalanceInNodeRange=[]
    
    #custom config data
    nodeNum=5
    
    #init experiment
    nodes={}
    for i in range(nodeNum):
        nodeId=uuid.uuid4()
        nodes[nodeId]=(1,Node(nodeId))
    Coord=Coordinator(nodes)
    
    #run experiment
    exp=Coord.monitor()
    
    #print experimental results
    print('--------experimental results---------')
    print(exp)
    print('velocities:')
    print(InputStream.velArray)
    
    lvsInNodeRange.append(exp['total_lv'])
    itersInNodeRange.append(exp['total_iterations'])
    reqsInNodeRange.append(exp['total_request_msgs'])
    lvsPerIterInNodeRange.append(exp['lvs_per_iter'])
    reqPerBalanceInNodeRange.append(exp['req_per_balance'])
    
    #plot experimental results
    
    
    
    