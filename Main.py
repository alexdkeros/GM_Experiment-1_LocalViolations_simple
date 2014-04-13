'''
@author: ak
'''
import uuid
import time
import pylab as pl
from matplotlib import rc
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
from GM_localViolations.Coordinator import Coordinator
from GM_localViolations.Node import Node
from GM_localViolations.InputStream import InputStream
from GM_localViolations import Config


if __name__ == '__main__':
    print('--------------experiment start-------------------')
    #experimental results init
    lvsInNodeRange=[]
    itersInNodeRange=[]
    reqsInNodeRange=[]
    lvsPerIterInNodeRange=[]
    reqPerBalanceInNodeRange=[]
    
    #node experimental range
    for nodeNum in range(Config.nodeStart,Config.nodeEnd+1):
        
        #node specific experimental data over iterations
        exp={'total_lv':0, 'total_iterations':0, 'total_request_msgs':0, 'lvs_per_iter':[], 'req_per_balance':[]}

        #iterations to avg over
        for iterations in range(Config.defIterations):
            
            #init experiment
            nodes={}
            for i in range(nodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(1,Node(nodeId))
            Coord=Coordinator(nodes)
            
            #run experiment
            expData=Coord.monitor()
            
            #collect data
            exp['total_lv']+=expData['total_lv']
            exp['total_iterations']+=expData['total_iterations']
            exp['total_request_msgs']+=expData['total_request_msgs']
            exp['lvs_per_iter'].append(expData['lvs_per_iter'])
            exp['req_per_balance'].append(expData['req_per_balance'])
            
        #averaging data over iterations
        exp['total_lv']=exp['total_lv']/Config.defIterations
        exp['total_iterations']=exp['total_iterations']/Config.defIterations
        exp['total_request_msgs']=exp['total_request_msgs']/Config.defIterations
        lvsPerIterInNodeRange.append(Config.avgListsOverIters(exp['lvs_per_iter']))
        reqPerBalanceInNodeRange.append(Config.avgListsOverIters(exp['req_per_balance']))
        lvsInNodeRange.append(exp['total_lv'])
        itersInNodeRange.append(exp['total_iterations'])
        reqsInNodeRange.append(exp['total_request_msgs'])
        
        #DBG
        print('MAIN:data for NodeNum %d'%nodeNum)
        print(exp)
            
    
    #----------------------print experimental results
    print('--------experimental results---------')
    #DBG
    print('MAIN:lvs:')
    print(lvsInNodeRange)
    print('MAIN:iters:')
    print(itersInNodeRange)
    print('MAIN:reqs:')
    print(reqsInNodeRange)
    print('MAIN:lvsPerIter:%d'%max(map(len,lvsPerIterInNodeRange)))
    print(lvsPerIterInNodeRange)
    print('MAIN:ReqPerBalance:%d'%max(map(len,reqPerBalanceInNodeRange)))
    print(reqPerBalanceInNodeRange)
    
    #DBG
    #print('velocities:')
    #print(InputStream.velArray)
    
    
    #---------------------plot experimental results
    
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)
    
    #2Dplots
    nodeRange = pl.arange( Config.nodeStart, Config.nodeEnd+1)

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(nodeRange,lvsInNodeRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    lvAxes.set_xlabel('Nodes')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Node Range')
    lvFig.tight_layout()
    #lvFig.savefig('LocalViolationsInNodeRangePlot.png')
    #lvFig.show()
    #time.sleep(10)
    
    #iterations plot
    iterFig,iterAxes=pl.subplots()
    iterAxes.plot(nodeRange,itersInNodeRange,'r')
    iterAxes.grid(True)
    iterAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    #iterAxes.set_ylim([0,50])
    iterAxes.set_xlabel('Nodes')
    iterAxes.set_ylabel('Iterations')
    iterAxes.set_title('Iterations until Global Violation in Node Range')
    iterFig.tight_layout()
    #iterFig.savefig('IterationsInNodeRangePlot.png')
    #iterFig.show()
    #time.sleep(5)
    
    #requests plot
    reqFig,reqAxes=pl.subplots()
    reqAxes.plot(nodeRange,reqsInNodeRange,'r')
    reqAxes.grid(True)
    reqAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    reqAxes.set_xlabel('Nodes')
    reqAxes.set_ylabel('Requests')
    reqAxes.set_title('Requests until Global Violation in Node Range')
    reqFig.tight_layout()
    #reqFig.savefig('RequestsInNodeRangePlot.png')
    #reqFig.show()
    #time.sleep(10)
    
    #3d plots
    #vls per iteration plot
    lvsPerIterFig=pl.figure()
    lvsPerIterAxes=lvsPerIterFig.add_subplot(1,1,1,projection='3d')
    

    nodes = range(Config.nodeStart,Config.nodeEnd+1)
    iters = range(0,max(map(len,lvsPerIterInNodeRange)))
    Y,X = pl.meshgrid(nodes,iters)
    p=lvsPerIterAxes.plot_surface(X,Y,Config.toNdArray(lvsPerIterInNodeRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    lvsPerIterAxes.set_ylim3d(Config.nodeStart,Config.nodeEnd)
    lvsPerIterAxes.set_xlabel('Iterations')
    lvsPerIterAxes.set_ylabel('Nodes')
    lvsPerIterAxes.set_zlabel('Local Violations')
    #lvsPerIterFig.show()
    #time.sleep(20)
    
    #reqs per balance plot
    ReqsPerBalanceFig=pl.figure()
    ReqsPerBalanceAxes=ReqsPerBalanceFig.add_subplot(1,1,1,projection='3d')
    

    nodes = range(Config.nodeStart,Config.nodeEnd+1)
    balances = range(0,max(map(len,reqPerBalanceInNodeRange)))
    Y,X = pl.meshgrid(nodes,balances)
    p=ReqsPerBalanceAxes.plot_surface(X,Y,Config.toNdArray(reqPerBalanceInNodeRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    ReqsPerBalanceAxes.set_ylim3d(Config.nodeStart,Config.nodeEnd)
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Nodes')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceFig.show()
    time.sleep(20)
    
    