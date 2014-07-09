'''
@author: ak
'''
from scipy.stats import norm
from GM_localViolations import Config




class InputStream:
    '''
    class InputStream
    models a continuous input stream of data having velocities sampled from a normal distribution
    implements a generator of data
    configuration via Config module
    '''

    def __init__(self,status,initXData, mean, std, interval):
        '''
        Constructor
        args:
              status: "static" or "random" velocities
              mean: mean of normal distribution
              std: standard deviation of normal distribution
              interval: update interval in case of changing velocities
        '''
        self.status=status
        self.initXData=initXData
        self.mean=mean
        self.std=std
        self.interval=interval
        self.velocity=norm.rvs(self.mean,self.std)  
    
    def getVelocity(self):
        return self.velocity
    
    def correctVelocity(self,deltaV):  
        self.velocity+=deltaV
    
    def getData(self):
        '''
        Generator
        yields new data
        '''
        xData=self.initXData
        while 1:
            if self.status=="random":
                self.velocity=norm.rvs(self.mean,self.std)
            for i in range(self.interval):
                yield xData
            xData=xData+self.velocity
                
                
                
                
                
if __name__=="__main__":
    '''simple test'''

    streams=[]
    for i in range(10):
        stream=InputStream("random",0,5,1,1)
        streams.append((stream,stream.getData()))
    print(streams)
    
    avgV=0
    for stream in streams:
        avgV+=stream[0].getVelocity()
    print("avgVel:%f"%(avgV/10))
    
    for stream in streams:
        stream[0].correctVelocity(5-avgV/10)
    
    avgV=0
    for stream in streams:
        avgV+=stream[0].getVelocity()
    print("avgVel:%f"%(avgV/10))
    
    for i in range(10):
        avgV=0
        print("-------iter:%d--------"%i)
        for stream in streams:
            avgV+=stream[0].getVelocity()
            print("vel:%f, data:%f"%(stream[0].getVelocity(),stream[1].next()))
        print("avgVel:%f"%(avgV/10))

    