'''
@author: ak
'''
from GM_localViolations.InputStream import InputStream
from GM_localViolations import Config


class Node:
    '''
    class Node
    models a node at a Geometric Monitoring network
    configuration via Config module
    '''

    def __init__(self, nodeId, inputGen=InputStream().getData(), weight=Config.defWeight, monFunc=Config.defMonFunc, threshold=Config.threshold, initialV=Config.defV):
        '''
        Constructor
        args:
            nodeId: the node id
            inputGen: data input generator
            weight: the node weight
            monFunc: the monitored function
            threshold: the monitoring threshold
            initialV: the initial local statistics vector
        '''

        #node data initialization
        self.id=nodeId
        self.inputGenerator=inputGen
        self.thresh=threshold    #monitoring threshold
        self.monFunc=monFunc
        self.weight=weight  #node weight
        self.v=initialV    #local statistics vector
        self.vLast=0    #last sent local statistics vector
        self.u=0    #drift vector
        self.e=0   #estimate vector
        self.delta=0    #slack vector
        
        #DBG
        print('node %s created'%self.id)
       
       
        
    '''
    "signal" methods
    '''
    def init(self):
        '''
        "init" method
        @return: tuple (nodeId,local stats vector)
        '''
        #DBG
        print('init signal received at node %s'%self.id)
        
        self.vLast=self.v
        return((self.id,self.vLast))
        
        
    def req(self):
        '''
        "req" method
        @return: tuple (nodeId,local stats vector,drift vector)
        '''
        
        #DBG
        print('req signal received at node %s'%self.id)
        
        return ((self.id,self.v,self.u))
    
    def rep(self):
        '''
        "rep" method
        @return: tuple (nodeId,local stats vector,drift vector)
        '''
    
        #DBG
        print('reporting local violation at node %s, u:%0.2f'%(self.id,self.u))
        
        return ((self.id,self.v,self.u))

        
    def adjSlk(self,dDelta):
        '''
        "adj-slk" method
        '''

        #DBG
        print('adjSlk signal received at node %s, dDelta: %0.2f'%(self.id,dDelta))
        
        #adjusting current slack vector
        self.delta+=dDelta
        
        #recalculate last drift vector value with new slack vector
        self.u=self.u+dDelta/self.weight
 

    
    
    def newEst(self,newE):
        '''
        "new-est" method
        '''
        #DBG
        print('new-est signal received at node %s, new est: %0.2f'%(self.id,newE))
        
        self.e=newE
        self.vLast=self.v
        self.delta=0
        
    def globalViolation(self):
        '''
        "global-violation" method
        '''
        #DBG
        print('global-violation signal received at node %s'%self.id)


    
    '''
    monitoring operation
    ''' 
    def run(self):
        '''
        main node execution
        @return: if no local violation: 
                    return None
                else:
                    return rep method
        '''
        
        #normal operation
        self.v=self.inputGenerator.next()
        self.u=self.e+(self.v-self.vLast)+(self.delta/self.weight)
        
        #DBG
        print("node:%s, v=%0.2f, u=%0.2f, e=%0.2f, vLast=%0.2f, delta=%0.2f, w=%0.2f, monU=%0.2f"%(self.id, self.v, self.u, self.e, self.vLast, self.delta, self.weight, self.monFunc(self.u)))
        
        #check for local violation
        if self.monFunc(self.u)>=self.thresh:
            return self.rep()
        else:
            return None
        
        
        
        
        
        
        