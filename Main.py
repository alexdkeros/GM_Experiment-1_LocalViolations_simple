'''
@author: ak
'''
import matplotlib
matplotlib.use('Agg')
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
            
            #init experiment
            nodes={}
            for i in range(nodeNum):
                nodeId=uuid.uuid4()
                nodes[nodeId]=(Config.defWeight,Node(nodeId))
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
    lvFig.savefig('LocalViolationsInNodeRangePlot.png')
    #lvFig.show()
    #time.sleep(5)
    
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
    lvsPerIterAxes.view_init(70, 30)
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
    ReqsPerBalanceAxes.view_init(70, 30)
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
            nodes={}
            for i in range(Config.defNodeNum):
                nodeId=uuid.uuid4()
                nodeInputGen=InputStream(mean=meanVal)
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=nodeInputGen))
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

    #local violation plot
    lvFig,lvAxes=pl.subplots()
    lvAxes.plot(meanRange,lvsInMeanRange,'r')
    lvAxes.grid(True)
    lvAxes.set_xlim([Config.meanStart,Config.meanEnd])
    lvAxes.set_xlabel('Mean')
    lvAxes.set_ylabel('Local Violations')
    lvAxes.set_title('Local Violations in Mean Range')
    lvFig.tight_layout()
    #lvFig.savefig('LocalViolationsInMeanRangePlot.png')
    lvFig.show()
    time.sleep(10)
    
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
    p=lvsPerIterAxes.plot_surface(X[0:Config.meanLvsPerIterPlotLim,:],Y[0:Config.meanLvsPerIterPlotLim,:],Config.toNdArray(lvsPerIterInMeanRange).transpose()[0:Config.meanLvsPerIterPlotLim,:],rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    lvsPerIterAxes.view_init(40, 40)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
    lvsPerIterAxes.set_ylim3d([Config.meanStart,Config.meanEnd])
    lvsPerIterAxes.set_xlim3d([0,Config.meanLvsPerIterPlotLim])
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
    p=ReqsPerBalanceAxes.plot_surface(X[0:Config.meanReqPerBalPlotLim,:],Y[0:Config.meanReqPerBalPlotLim,:],Config.toNdArray(reqPerBalanceInMeanRange).transpose()[0:Config.meanReqPerBalPlotLim,:],rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(40, 40)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    ReqsPerBalanceAxes.set_xlim3d([0,Config.meanReqPerBalPlotLim])
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
            nodes={}
            for i in range(Config.defNodeNum):
                nodeId=uuid.uuid4()
                nodeInputGen=InputStream(std=stdVal)
                nodes[nodeId]=(Config.defWeight,Node(nodeId,inputGen=nodeInputGen))
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
    p=lvsPerIterAxes.plot_surface(X,Y,Config.toNdArray(lvsPerIterInStdRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    lvsPerIterAxes.view_init(40, 40)
    cb = lvsPerIterFig.colorbar(p, shrink=0.5)
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
    p=ReqsPerBalanceAxes.plot_surface(X,Y,Config.toNdArray(reqPerBalanceInStdRange).transpose(),rstride=1, cstride=1, cmap=cm.get_cmap('coolwarm', None), linewidth=0, antialiased=True)
    ReqsPerBalanceAxes.view_init(40, 40)
    cb = ReqsPerBalanceFig.colorbar(p, shrink=0.5)
    ReqsPerBalanceAxes.set_ylim3d([Config.stdStart,Config.stdEnd+1])
    ReqsPerBalanceAxes.set_xlabel('Balances')
    ReqsPerBalanceAxes.set_ylabel('Standard Deviation')
    ReqsPerBalanceAxes.set_zlabel('Requests')
    ReqsPerBalanceAxes.set_title('Average Requests per Balancing Process')
    ReqsPerBalanceFig.savefig('ReqsPerBalanceInStdRangePlot.png')
    #ReqsPerBalanceFig.show()
    #time.sleep(10)
