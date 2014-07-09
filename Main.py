'''
@author: ak
'''
from __future__ import division
import matplotlib
# matplotlib.use('Agg')
import uuid
import time
import pylab as pl
from matplotlib import rc
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
from GM_localViolations.Coordinator import Coordinator
from GM_localViolations.Node import Node
from GM_localViolations.InputStream import InputStream
from GM_localViolations.InputStreamFactory import InputStreamFactory
from GM_localViolations import Config


if __name__ == '__main__':
    
    
    #-------------------------------------------------------------------------------------
    #---------------------------------EXPERIMENT:-----------------------------------------
    #---------------------------------NODE RANGE------------------------------------------
    #-------------------------------------------------------------------------------------

    print('--------------experiment start:NODES-------------------')
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
            
            #---init experiment
            
            #create input streams
            factory=InputStreamFactory(nodeNum)
            streamFetcher=factory.getInputStream()
            
            #create nodes
            nodes={}
            for i in range(nodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=streamFetcher.next()))
            
            #create coordinator
            Coord=Coordinator(nodes,inputStreamControl=factory)
            
            
            #---run experiment
            expData=Coord.monitor()
            
            #DBG
            print(expData)
            
            #---collect data
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
    print('MAIN:avgReqsPerLv')
    print(pl.divide(reqsInNodeRange,lvsInNodeRange))
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
    
    #requests/vls plot
    rlvFig,rlvAxes=pl.subplots()
    rlvAxes.plot(nodeRange,pl.divide(reqsInNodeRange,lvsInNodeRange),'r')
    rlvAxes.grid(True)
    rlvAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    rlvAxes.set_xlabel('Nodes')
    rlvAxes.set_ylabel('Avg Requests per Local Violation')
    rlvAxes.set_title('Avg Requests per Local Violation in Node Range')
    rlvFig.tight_layout()
    rlvFig.savefig('AvgRequestsPerLocalViolationInNodeRangePlot.png')
    #rlvFig.show()
    #time.sleep(5)

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(nodeRange,lvsInNodeRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    lvAxes.set_xlabel('Nodes')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Node Range')
    lvFig.tight_layout()
    lvFig.savefig('LocalViolationsInNodeRangePlot.png')
    #lvFig.show()
    #time.sleep(5)
    
    #iterations plot
    iterFig,iterAxes=pl.subplots()
    iterAxes.plot(nodeRange,itersInNodeRange,'r')
    iterAxes.grid(True)
    iterAxes.set_xlim([Config.nodeStart,Config.nodeEnd])
    #iterAxes.set_ylim([0,100])
    iterAxes.set_xlabel('Nodes')
    iterAxes.set_ylabel('Iterations')
    iterAxes.set_title('Iterations until Global Violation in Node Range')
    iterFig.tight_layout()
    iterFig.savefig('IterationsInNodeRangePlot.png')
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
    reqFig.savefig('RequestsInNodeRangePlot.png')
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
    lvsPerIterAxes.view_init(60, 35) #70,30
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    lvsPerIterAxes.set_ylim3d(Config.nodeStart,Config.nodeEnd)
    lvsPerIterAxes.set_xlabel('Iterations')
    lvsPerIterAxes.set_ylabel('Nodes')
    lvsPerIterAxes.set_zlabel('Local Violations')
    lvsPerIterAxes.set_title('Average Local Violations per Iteration')
    lvsPerIterFig.savefig('VlsPerIterInNodeRangePlot.png')
    #lvsPerIterFig.show()
    #time.sleep(20)
    
    #reqs per balance plot
    ReqsPerBalanceFig=pl.figure()
    ReqsPerBalanceAxes=ReqsPerBalanceFig.add_subplot(1,1,1,projection='3d')
    nodes = range(Config.nodeStart,Config.nodeEnd+1)
    balances = range(0,max(map(len,reqPerBalanceInNodeRange)))
    Y,X = pl.meshgrid(nodes,balances)
    p=ReqsPerBalanceAxes.plot_surface(X,Y,Config.toNdArray(reqPerBalanceInNodeRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(60, 35)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    ReqsPerBalanceAxes.set_ylim3d(Config.nodeStart,Config.nodeEnd)
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Nodes')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceAxes.set_title('Average Requests per Balancing Process')
    ReqsPerBalanceFig.savefig('ReqsPerBalanceInNodeRangePlot.png')
    #ReqsPerBalanceFig.show()
    #time.sleep(20)
    
  
   
    
    
    
    
    
    
    
    
    
    
    
    
    #-------------------------------------------------------------------------------------
    #---------------------------------EXPERIMENT:-----------------------------------------
    #---------------------------------THRESHOLD RANGE-------------------------------------
    #-------------------------------------------------------------------------------------

    print('--------------experiment start:THRESHOLD-------------------')
    #experimental results init
    lvsInThresRange=[]
    itersInThresRange=[]
    reqsInThresRange=[]
    lvsPerIterInThresRange=[]
    reqPerBalanceInThresRange=[]
    
    #node experimental range
    for thresh in range(Config.thresStart,Config.thresEnd+1):
        
        #node specific experimental data over iterations
        exp={'total_lv':0, 'total_iterations':0, 'total_request_msgs':0, 'lvs_per_iter':[], 'req_per_balance':[]}

        #iterations to avg over
        for iterations in range(Config.defIterations):
            
            #init experiment
            
            #create input streams
            factory=InputStreamFactory(Config.defNodeNum)
            streamFetcher=factory.getInputStream()
            
            nodes={}
            for i in range(Config.defNodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=streamFetcher.next(),threshold=thresh))
            Coord=Coordinator(nodes,inputStreamControl=factory, threshold=thresh)
            
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
        lvsPerIterInThresRange.append(Config.avgListsOverIters(exp['lvs_per_iter']))
        reqPerBalanceInThresRange.append(Config.avgListsOverIters(exp['req_per_balance']))
        lvsInThresRange.append(exp['total_lv'])
        itersInThresRange.append(exp['total_iterations'])
        reqsInThresRange.append(exp['total_request_msgs'])
        
        #DBG
        print('MAIN:data for Threshold %d'%thresh)
        print(exp)
            
    
    #----------------------print experimental results
    print('--------experimental results---------')
    #DBG
    print('MAIN:lvs:')
    print(lvsInThresRange)
    print('MAIN:iters:')
    print(itersInThresRange)
    print('MAIN:reqs:')
    print(reqsInThresRange)
    print('MAIN:avgReqsPerLv')
    print(pl.divide(reqsInThresRange,lvsInThresRange))
    print('MAIN:lvsPerIter:%d'%max(map(len,lvsPerIterInThresRange)))
    print(lvsPerIterInThresRange)
    print('MAIN:ReqPerBalance:%d'%max(map(len,reqPerBalanceInThresRange)))
    print(reqPerBalanceInThresRange)
    
    #DBG
    #print('velocities:')
    #print(InputStream.velArray)
    
    
    #---------------------plot experimental results
    
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)
    
    #2Dplots
    thresRange = pl.arange( Config.thresStart, Config.thresEnd+1)
    
    #requests/vls plot
    rlvFig,rlvAxes=pl.subplots()
    rlvAxes.plot(thresRange,pl.divide(reqsInThresRange,lvsInThresRange),'r')
    rlvAxes.grid(True)
    rlvAxes.set_xlim([Config.thresStart,Config.thresEnd])
    rlvAxes.set_xlabel('Threshold')
    rlvAxes.set_ylabel('Avg Requests per Local Violation')
    rlvAxes.set_title('Avg Requests per Local Violation in Threshold Range')
    rlvFig.tight_layout()
    rlvFig.savefig('AvgRequestsPerLocalViolationInThresRangePlot.png')
    #rlvFig.show()
    #time.sleep(5)

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(thresRange,lvsInThresRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.thresStart,Config.thresEnd])
    lvAxes.set_xlabel('Threshold')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Threshold Range')
    lvFig.tight_layout()
    lvFig.savefig('LocalViolationsInThresholdRangePlot.png')
    #lvFig.show()
    #time.sleep(5)
    
    #iterations plot
    iterFig,iterAxes=pl.subplots()
    iterAxes.plot(thresRange,itersInThresRange,'r')
    iterAxes.grid(True)
    iterAxes.set_xlim([Config.thresStart,Config.thresEnd])
    #iterAxes.set_ylim([0,100])
    iterAxes.set_xlabel('Threshold')
    iterAxes.set_ylabel('Iterations')
    iterAxes.set_title('Iterations until Global Violation in Threshold Range')
    iterFig.tight_layout()
    iterFig.savefig('IterationsInThresholdRangePlot.png')
    #iterFig.show()
    #time.sleep(5)
    
    #requests plot
    reqFig,reqAxes=pl.subplots()
    reqAxes.plot(thresRange,reqsInThresRange,'r')
    reqAxes.grid(True)
    reqAxes.set_xlim([Config.thresStart,Config.thresEnd])
    reqAxes.set_xlabel('Threshold')
    reqAxes.set_ylabel('Requests')
    reqAxes.set_title('Requests until Global Violation in Threshold Range')
    reqFig.tight_layout()
    reqFig.savefig('RequestsInThresholdRangePlot.png')
    #reqFig.show()
    #time.sleep(10)
    
    #3d plots
    #vls per iteration plot
    lvsPerIterFig=pl.figure()
    lvsPerIterAxes=lvsPerIterFig.add_subplot(1,1,1,projection='3d')
    nodes = range(Config.thresStart,Config.thresEnd+1)
    iters = range(0,max(map(len,lvsPerIterInThresRange)))
    Y,X = pl.meshgrid(nodes,iters)
    p=lvsPerIterAxes.plot_surface(X,Y,Config.toNdArray(lvsPerIterInThresRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    lvsPerIterAxes.view_init(60, 35)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    lvsPerIterAxes.set_ylim3d(Config.thresStart,Config.thresEnd)
    lvsPerIterAxes.set_xlabel('Iterations')
    lvsPerIterAxes.set_ylabel('Threshold')
    lvsPerIterAxes.set_zlabel('Local Violations')
    lvsPerIterAxes.set_title('Average Local Violations per Iteration')
    lvsPerIterFig.savefig('VlsPerIterInThresholdRangePlot.png')
    #lvsPerIterFig.show()
    #time.sleep(20)
    
    #reqs per balance plot
    ReqsPerBalanceFig=pl.figure()
    ReqsPerBalanceAxes=ReqsPerBalanceFig.add_subplot(1,1,1,projection='3d')
    thresholds = range(Config.thresStart,Config.thresEnd+1)
    balances = range(0,max(map(len,reqPerBalanceInThresRange)))
    Y,X = pl.meshgrid(thresholds,balances)
    p=ReqsPerBalanceAxes.plot_surface(X,Y,Config.toNdArray(reqPerBalanceInThresRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(60, 35)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    ReqsPerBalanceAxes.set_ylim3d(Config.thresStart,Config.thresEnd)
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Threshold')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceAxes.set_title('Average Requests per Balancing Process')
    ReqsPerBalanceFig.savefig('ReqsPerBalanceInThresholdRangePlot.png')
    #ReqsPerBalanceFig.show()
    #time.sleep(20)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    #-------------------------------------------------------------------------------------
    #---------------------------------EXPERIMENT:-----------------------------------------
    #---------------------------------MEAN RANGE------------------------------------------
    #-------------------------------------------------------------------------------------

    print('--------------experiment start:MEAN-------------------')
    #experimental results init
    lvsInMeanRange=[]
    itersInMeanRange=[]
    reqsInMeanRange=[]
    lvsPerIterInMeanRange=[]
    reqPerBalanceInMeanRange=[]
    
    #mean experimental range
    for meanVal in pl.arange(Config.meanStart,Config.meanEnd+1,Config.meanStep):
        
        #DBG
        print('MAIN:mean is %f'%meanVal)
        
        #node specific experimental data over iterations
        exp={'total_lv':0, 'total_iterations':0, 'total_request_msgs':0, 'lvs_per_iter':[], 'req_per_balance':[]}

        #iterations to avg over
        for iterations in range(Config.defIterations):
            
            #init experiment
            
            #create input streams
            factory=InputStreamFactory(Config.defNodeNum, mean=meanVal)
            streamFetcher=factory.getInputStream()
            
            
            nodes={}
            for i in range(Config.defNodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=streamFetcher.next()))
            Coord=Coordinator(nodes,inputStreamControl=factory)
            
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
        lvsPerIterInMeanRange.append(Config.avgListsOverIters(exp['lvs_per_iter']))
        reqPerBalanceInMeanRange.append(Config.avgListsOverIters(exp['req_per_balance']))
        lvsInMeanRange.append(exp['total_lv'])
        itersInMeanRange.append(exp['total_iterations'])
        reqsInMeanRange.append(exp['total_request_msgs'])
        
        #DBG
        print('MAIN:data for Mean %f'%meanVal)
        print(exp)
            
    
    #----------------------print experimental results
    print('--------experimental results---------')
    #DBG
    print('MAIN:lvs:')
    print(lvsInMeanRange)
    print('MAIN:iters:')
    print(itersInMeanRange)
    print('MAIN:reqs:')
    print(reqsInMeanRange)
    print('MAIN:avgReqsPerLv')
    print(pl.divide(reqsInMeanRange,lvsInMeanRange))
    print('MAIN:lvsPerIter:%d'%max(map(len,lvsPerIterInMeanRange)))
    print(lvsPerIterInMeanRange)
    print('MAIN:ReqPerBalance:%d'%max(map(len,reqPerBalanceInMeanRange)))
    print(reqPerBalanceInMeanRange)
    
    #DBG
    #print('velocities:')
    #print(InputStream.velArray)
    
    
    #---------------------plot experimental results
    
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)
    
    #2Dplots
    meanRange = pl.arange( Config.meanStart, Config.meanEnd+1,Config.meanStep)
    
    #requests/vls plot
    rlvFig,rlvAxes=pl.subplots()
    rlvAxes.plot(meanRange,pl.divide(reqsInMeanRange,lvsInMeanRange),'r')
    rlvAxes.grid(True)
    rlvAxes.set_xlim([Config.meanStart,Config.meanEnd])
    rlvAxes.set_xlabel('Mean')
    rlvAxes.set_ylabel('Avg Requests per Local Violation')
    rlvAxes.set_title('Avg Requests per Local Violation in Mean Range')
    rlvFig.tight_layout()
    rlvFig.savefig('AvgRequestsPerLocalViolationInMeanRangePlot.png')
    #rlvFig.show()
    #time.sleep(5)

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(meanRange,lvsInMeanRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.meanStart,Config.meanEnd])
    lvAxes.set_xlabel('Mean')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Mean Range')
    lvFig.tight_layout()
    lvFig.savefig('LocalViolationsInMeanRangePlot.png')
    #lvFig.show()
    #time.sleep(10)
    
    #iterations plot
    iterFig,iterAxes=pl.subplots()
    iterAxes.plot(meanRange,itersInMeanRange,'r')
    iterAxes.grid(True)
    iterAxes.set_xlim([Config.meanStart,Config.meanEnd])
    #iterAxes.set_ylim([0,50])
    iterAxes.set_xlabel('Mean')
    iterAxes.set_ylabel('Iterations')
    iterAxes.set_title('Iterations until Global Violation in Mean Range')
    iterFig.tight_layout()
    iterFig.savefig('IterationsInMeanRangePlot.png')
    #iterFig.show()
    #time.sleep(10)
    
    #requests plot
    reqFig,reqAxes=pl.subplots()
    reqAxes.plot(meanRange,reqsInMeanRange,'r')
    reqAxes.grid(True)
    reqAxes.set_xlim([Config.meanStart,Config.meanEnd])
    reqAxes.set_xlabel('Mean')
    reqAxes.set_ylabel('Requests')
    reqAxes.set_title('Requests until Global Violation in Mean Range')
    reqFig.tight_layout()
    reqFig.savefig('RequestsInMeanRangePlot.png')
    #reqFig.show()
    #time.sleep(10)
    
    
    #3d plots
    #vls per iteration plot
    lvsPerIterFig=pl.figure()
    lvsPerIterAxes=lvsPerIterFig.add_subplot(1,1,1,projection='3d')
    means = pl.arange(Config.meanStart,Config.meanEnd+1,Config.meanStep)
    iters = range(0,max(map(len,lvsPerIterInMeanRange)))
    Y,X = pl.meshgrid(means,iters)
    p=lvsPerIterAxes.plot_surface(X[0:Config.meanLvsPerIterPlotLim,:],Y[0:Config.meanLvsPerIterPlotLim,:],Config.toNdArray(lvsPerIterInMeanRange)[:,0:Config.meanLvsPerIterPlotLim].transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    lvsPerIterAxes.view_init(40, 40)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    lvsPerIterAxes.set_ylim3d([Config.meanStart,Config.meanEnd])
    #lvsPerIterAxes.set_xlim3d([0,Config.meanLvsPerIterPlotLim])
    lvsPerIterAxes.set_xlabel('Iterations')
    lvsPerIterAxes.set_ylabel('Mean')
    lvsPerIterAxes.set_zlabel('Local Violations')
    lvsPerIterAxes.set_title('Average Local Violations per Iteration')
    lvsPerIterFig.savefig('LvsPerIterInMeanRangePlot.png')
    #lvsPerIterFig.show()
    #time.sleep(10)


    #reqs per balance plot
    ReqsPerBalanceFig=pl.figure()
    ReqsPerBalanceAxes=ReqsPerBalanceFig.add_subplot(1,1,1,projection='3d')
    means = pl.arange(Config.meanStart,Config.meanEnd+1,Config.meanStep)
    balances = range(0,max(map(len,reqPerBalanceInMeanRange)))
    Y,X = pl.meshgrid(means,balances)    
    p=ReqsPerBalanceAxes.plot_surface(X[0:Config.meanReqPerBalPlotLim,:],Y[0:Config.meanReqPerBalPlotLim,:],Config.toNdArray(reqPerBalanceInMeanRange)[:,0:Config.meanReqPerBalPlotLim].transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(40, 40)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    #ReqsPerBalanceAxes.set_xlim3d([0,Config.meanReqPerBalPlotLim])
    ReqsPerBalanceAxes.set_ylim3d([Config.meanStart,Config.meanEnd])
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Mean')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceAxes.set_title('Average Requests per Balancing Process')
    ReqsPerBalanceFig.savefig('ReqsPerBalanceInMeanRangePlot.png')
    #ReqsPerBalanceFig.show()
    #time.sleep(10)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    #-------------------------------------------------------------------------------------
    #---------------------------------EXPERIMENT:-----------------------------------------
    #---------------------------------STD RANGE------------------------------------------
    #-------------------------------------------------------------------------------------

    print('--------------experiment start:STD-------------------')
    #experimental results init
    lvsInStdRange=[]
    itersInStdRange=[]
    reqsInStdRange=[]
    lvsPerIterInStdRange=[]
    reqPerBalanceInStdRange=[]
    
    #std experimental range
    for stdVal in pl.arange(Config.stdStart,Config.stdEnd+1,Config.stdStep):
        
        #DBG
        print('MAIN:std is %f'%stdVal)
        
        #node specific experimental data over iterations
        exp={'total_lv':0, 'total_iterations':0, 'total_request_msgs':0, 'lvs_per_iter':[], 'req_per_balance':[]}

        #iterations to avg over
        for iterations in range(Config.defIterations):
            
            #init experiment
            
            #create input streams
            factory=InputStreamFactory(Config.defNodeNum, std=stdVal)
            streamFetcher=factory.getInputStream()
            
            
            nodes={}
            for i in range(Config.defNodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=streamFetcher.next()))
            Coord=Coordinator(nodes,inputStreamControl=factory)
            
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
        lvsPerIterInStdRange.append(Config.avgListsOverIters(exp['lvs_per_iter']))
        reqPerBalanceInStdRange.append(Config.avgListsOverIters(exp['req_per_balance']))
        lvsInStdRange.append(exp['total_lv'])
        itersInStdRange.append(exp['total_iterations'])
        reqsInStdRange.append(exp['total_request_msgs'])
        
        #DBG
        print('MAIN:data for Std %f'%stdVal)
        print(exp)
            
    
    #----------------------print experimental results
    print('--------experimental results---------')
    #DBG
    print('MAIN:lvs:')
    print(lvsInStdRange)
    print('MAIN:iters:')
    print(itersInStdRange)
    print('MAIN:reqs:')
    print(reqsInStdRange)
    print('MAIN:avgReqsPerLv')
    print(pl.divide(reqsInStdRange,lvsInStdRange))
    print('MAIN:lvsPerIter:%d'%max(map(len,lvsPerIterInStdRange)))
    print(lvsPerIterInStdRange)
    print('MAIN:ReqPerBalance:%d'%max(map(len,reqPerBalanceInStdRange)))
    print(reqPerBalanceInStdRange)
    
    #DBG
    #print('velocities:')
    #print(InputStream.velArray)
    
    
    #---------------------plot experimental results
    
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)
    

    #2Dplots
    stdRange = pl.arange( Config.stdStart, Config.stdEnd+1,Config.stdStep)
    
    #requests/vls plot
    rlvFig,rlvAxes=pl.subplots()
    rlvAxes.plot(stdRange,pl.divide(reqsInStdRange,lvsInStdRange),'r')
    rlvAxes.grid(True)
    rlvAxes.set_xlim([Config.stdStart,Config.stdEnd])
    rlvAxes.set_xlabel('Standard Deviation')
    rlvAxes.set_ylabel('Avg Requests per Local Violation')
    rlvAxes.set_title('Avg Requests per Local Violation in Standard Deviation Range')
    rlvFig.tight_layout()
    rlvFig.savefig('AvgRequestsPerLocalViolationInStdRangePlot.png')
    #rlvFig.show()
    #time.sleep(5)

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(stdRange,lvsInStdRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.stdStart,Config.stdEnd])
    lvAxes.set_xlabel('Standard Deviation')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Standard Deviation Range')
    lvFig.tight_layout()
    lvFig.savefig('LocalViolationsInStdRangePlot.png')
    #lvFig.show()
    #time.sleep(10)
    
    #iterations plot
    iterFig,iterAxes=pl.subplots()
    iterAxes.plot(stdRange,itersInStdRange,'r')
    iterAxes.grid(True)
    iterAxes.set_xlim([Config.stdStart,Config.stdEnd])
    #iterAxes.set_ylim([0,50])
    iterAxes.set_xlabel('Standard Deviation')
    iterAxes.set_ylabel('Iterations')
    iterAxes.set_title('Iterations until Global Violation in Standard Deviation Range')
    iterFig.tight_layout()
    iterFig.savefig('IterationsInStdRangePlot.png')
    #iterFig.show()
    #time.sleep(10)
    
    #requests plot
    reqFig,reqAxes=pl.subplots()
    reqAxes.plot(stdRange,reqsInStdRange,'r')
    reqAxes.grid(True)
    reqAxes.set_xlim([Config.stdStart,Config.stdEnd])
    reqAxes.set_xlabel('Standard Deviation')
    reqAxes.set_ylabel('Requests')
    reqAxes.set_title('Requests until Global Violation in Standard Deviation Range')
    reqFig.tight_layout()
    reqFig.savefig('RequestsInStdRangePlot.png')
    #reqFig.show()
    #time.sleep(10)
    

    
    
    #3d plots
    #vls per iteration plot
    lvsPerIterFig=pl.figure()
    lvsPerIterAxes=lvsPerIterFig.add_subplot(1,1,1,projection='3d')
    stds = pl.arange(Config.stdStart,Config.stdEnd+1,Config.stdStep)
    iters = range(0,max(map(len,lvsPerIterInStdRange)))
    Y,X = pl.meshgrid(stds,iters)
    p=lvsPerIterAxes.plot_surface(X[0:Config.stdLvsPerIterPlotLim,:],Y[0:Config.stdLvsPerIterPlotLim,:],Config.toNdArray(lvsPerIterInStdRange)[:,0:Config.stdLvsPerIterPlotLim].transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    lvsPerIterAxes.view_init(40, 40)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    #lvsPerIterAxes.set_xlim3d([0,Config.stdLvsPerIterPlotLim])
    lvsPerIterAxes.set_ylim3d([Config.stdStart,Config.stdEnd+1])
    lvsPerIterAxes.set_xlabel('Iterations')
    lvsPerIterAxes.set_ylabel('Standard Deviation')
    lvsPerIterAxes.set_zlabel('Local Violations')
    lvsPerIterAxes.set_title('Average Local Violations per Iteration')
    lvsPerIterFig.savefig('LvsPerIterInStdRangePlot.png')
    #lvsPerIterFig.show()
    #time.sleep(10)


    #reqs per balance plot
    ReqsPerBalanceFig=pl.figure()
    ReqsPerBalanceAxes=ReqsPerBalanceFig.add_subplot(1,1,1,projection='3d')
    stds = pl.arange(Config.stdStart,Config.stdEnd+1,Config.stdStep)
    balances = range(0,max(map(len,reqPerBalanceInStdRange)))
    Y,X = pl.meshgrid(stds,balances)    
    p=ReqsPerBalanceAxes.plot_surface(X[0:Config.stdReqPerBalPlotLim,:],Y[0:Config.stdReqPerBalPlotLim,:],Config.toNdArray(reqPerBalanceInStdRange)[:,0:Config.stdReqPerBalPlotLim].transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(40, 40)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    #ReqsPerBalanceAxes.set_xlim3d([0,Config.stdReqPerBalPlotLim])
    ReqsPerBalanceAxes.set_ylim3d([Config.stdStart,Config.stdEnd+1])
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Standard Deviation')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceAxes.set_title('Average Requests per Balancing Process')
    ReqsPerBalanceFig.savefig('ReqsPerBalanceInStdRangePlot.png')
    #ReqsPerBalanceFig.show()
    #time.sleep(10)
