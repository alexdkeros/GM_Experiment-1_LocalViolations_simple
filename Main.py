'''
@author: ak
'''
import uuid
from GM_localViolations.Coordinator import Coordinator
from GM_localViolations.Node import Node
from GM_localViolations import Config

if __name__ == '__main__':
    print('--------------experiment start-------------------')
    
    #custom config data
    nodeNum=10
    nodes={}
    for i in range(nodeNum):
        nodeId=uuid.uuid4()
        nodes[nodeId]=(1,Node(nodeId))
        
    Coord=Coordinator(nodes)
    
    Coord.monitor()
    
    