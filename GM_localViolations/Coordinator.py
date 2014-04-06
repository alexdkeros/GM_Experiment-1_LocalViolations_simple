'''
@author: ak
'''
import random
from GM_localViolations.Node import Node
from GM_localViolations import Config

class Coordinator:
    '''
    class Coordinator
    models the Coordinator at a Geometric Monitoring network
    configuration via Config module
    '''


    def __init__(self, nodes, balancing="random", threshold=Config.threshold):
        '''
        Constructor
        args:
            nodes: network node dictionary
            balancing: the balancing method
            threshold: monitoring threshold
        '''

        
        #coordinator data initialization
        self.nodes=nodes   #network node dictionary {"nodeId" : (weight ,node instance)}
        self.thresh=threshold    #monitoring threshold
        self.v=0    #global statistics vector
        self.e=0    #estimate vector
        self.sumW=0 #sum of node weights
        self.balancing=balancing    #balancing method

        
        #experimental results
        self.expCounter=0
        
    def monitor(self):
        '''
        main monitoring method of coordinator
        control data income at nodes by calling their function run()
        checks for global violation
        calls balancing method
        @return: experimental data
        '''
        #-----init
        #computing initial estimation vector
        for node in self.nodes.values():
            nodeV=node[1].init()[1]
            w=node[0]
            self.e+=w*nodeV
            self.sumW+=w
        self.e=self.e/self.sumW
        
        #sending initial estimation vector to nodes
        for node in self.nodes.values():
            node[1].newEst(self.e)
            
        #DBG
        print("sum of weights is: %0.2f, new e is:%0.2f"%(self.sumW,self.e))

        gv=False
        while 1:
            #-----monitoring
            for node in self.nodes.values():
                rep=node[1].run()
                
                if rep:
                    #local violation occured, rep msg received
                    
                    #DBG
                    print("!local violation!")
                    print(rep)
                    
                    gv=self.__balance(rep)
                    
                    if gv:
                        #global violation occured
                        print("!!global violation, end simulation!!")
                        break
            if gv:
                break
        
        
    def __balance(self, data):
        '''
        balancing method
        args:
            data:tuple (nodeId, v, u)
        @return: if global violation:
                    return True
                else:
                    return False
        '''
        
        balancingSet=set() #set containing tuples (nodeId,v,u)
        balancingSet.add(data)
       

        b=0 #balancing vector
        setW=0
       
        while 1:
            #computing balancing vector b
            for node in balancingSet:
                w=self.nodes[node[0]][0]
                u=node[2]
                b+=w*u
                setW+=w
            b=b/setW
            
            #evaluating monochromaticity   
            if b<self.thresh:
                #DBG
                print('balance success, b=%0.2f'%b)
                
                #adjust slack vector
                for node in balancingSet:
                    w=self.nodes[node[0]][0]
                    u=node[2]
                    noderef=self.nodes[node[0]][1]
                    dDelta=w*b-w*u
                    noderef.adjSlk(dDelta)
                
                #break balancing loop
                return False
            
            else:
                diffSet=set(self.nodes.keys())-set(d[0] for d in balancingSet)
                
                if len(diffSet):
                    #request new node data at random
                    reqNodeId=random.sample(diffSet,1)[0]
        
                    balancingSet.add(self.nodes[reqNodeId][1].req())
                   
                else:
                    #no nodes to balance, global violation
                    for node in self.nodes.values():
                        node[1].globalViolation()
                    
                    #break balancing loop
                    return True
                    
                
       
        