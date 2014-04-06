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

    def __init__(self, nodeId, inputGen=InputStream().getData(), weight=Config.defWeight, threshold=Config.threshold, initialV=Config.defV):
        '''
        Constructor
        args:
            nodeId: the node id
            weight: the node weight
            initialV: the initial local statistics vector
        '''

        #node data initialization
        self.id=nodeId
        self.inputGenerator=inputGen
        self.thresh=threshold    #monitoring threshold
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
        @return: dictionary {"nodeId":id,"v":local stats vector}
        '''
        #DBG
        print('init signal received at node %s'%self.id)
        
        self.vLast=self.v
        return({"nodeId":self.id,"v":self.vLast})
        
        
    def req(self):
        '''
        "req" method
        @return: dictionary {"nodeId":id,"v":local stats vector,"u":drift vector}
        '''
        
        #DBG
        print('req signal received at node %s'%self.id)
        
        return ({"nodeId":self.id,"v":self.v,"u":self.u})
    
    def rep(self):
        '''
        "rep" method
        @return: dictionary {"nodeId":id,"v":local stats vector,"u":drift vector}
        '''
    
        #DBG
        print('reporting local violation at node %s, u:%0.2f'%(self.id,self.u))
        
        return ({"nodeId":self.id,"v":self.v,"u":self.u})

        
    def adjSlk(self,dDelta):
        '''
        "adj-slk" method
        '''

        #DBG
        print('adjSlk signal received at node %s, dDelta: %0.2f'%(self.id,dDelta))
        
        #adjusting current slack vector
        self.delta+=dDelta
    
    
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
        
        #check for local violation
        if self.u>=self.thresh:
            return self.rep(self)
        else:
            return None
        
        
        
        
        
        
        