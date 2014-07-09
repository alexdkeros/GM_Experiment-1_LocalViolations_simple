'''
@author: ak
'''
from GM_localViolations import Config
from GM_localViolations.InputStream import InputStream

class InputStreamFactory:
    '''
    A factory of InputStream Instances
    '''


    def __init__(self, count, status=Config.defStatus,initXData=Config.defInitXData, mean=Config.defMean, std=Config.defStd, interval=Config.defInterval):
        '''
        Constructor
        args:
              count: number of inputStreams to create
              status: "static" or "random" velocities
              mean: mean of normal distribution
              std: standard deviation of normal distribution
              interval: update interval in case of changing velocities
        '''
        self.count=count
        self.status=status
        self.initXData=initXData
        self.mean=mean
        self.std=std
        self.interval=interval
        
        self.inputStreams=[]
        for i in range(count):
            self.inputStreams.append(InputStream(status=self.status,initXData=self.initXData,mean=self.mean,std=self.std,interval=self.interval))
                                    
    def getInputStream(self):
        for stream in self.inputStreams:
            yield stream
    
    def avgVelocity(self):
        avgV=0
        for stream in self.inputStreams:
            avgV+=stream.getVelocity()
        return avgV/self.count
    
    def normalizeVelocities(self):
        deltaV=self.mean-self.avgVelocity()
        for stream in self.inputStreams:
            stream.correctVelocity(deltaV)

   
   
            
if __name__=="__main__":
    factory=InputStreamFactory(3, status="random")
    streamFetcher=factory.getInputStream()
    streams=[]
    for i in range(3):
        str=streamFetcher.next()
        streams.append((str,str.getData()))
    print(streams)
    


    
    for i in range(10):
        print("--iter:%d-----"%i)
        
        print("avgVelocity prior normalization")
        print(factory.avgVelocity())
        factory.normalizeVelocities()
        print("avgVelocity after normalization")
        print(factory.avgVelocity())
        gg=0
        for stream in streams:
            gg+=stream[0].getVelocity()
            print("velocity:%f, val:%f"%(stream[0].getVelocity(), stream[1].next()))
        print("avgVel for this iter:%f"%(gg/len(streams)))
        print("avgVelocity after data fetch")
        print(factory.avgVelocity())