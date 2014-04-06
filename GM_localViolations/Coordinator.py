'''
@author: ak
'''

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
            nodeNum: the number of nodes
        '''

        
        #coordinator data initialization
        self.nodes=nodes   #network node dictionary {"nodeId" : node instance}
        self.thresh=threshold    #monitoring threshold
        self.v=0    #global statistics vector
        self.e=0    #estimate vector
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
        
        
        