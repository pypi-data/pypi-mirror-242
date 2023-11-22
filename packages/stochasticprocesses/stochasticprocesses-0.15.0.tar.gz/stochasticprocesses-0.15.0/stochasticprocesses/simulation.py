
import pandas as pd  
import numpy as np
from random import sample





class StochasticSimulation:
      
    def __init__(self, steps=100, n_times=1, t=1):
        self.steps = steps
        self.n_times = n_times 
        self.dt = t  / steps
    
    
    def SimpleRandomWalk(self, p):
        # creating array
        rw = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(rw.shape[1]-1):
            for i in range(rw.shape[0]):
                rw[i][j+1] = rw[i][j] + np.random.choice([-1,1], p=[1-p, p])#sample([-1,1], 1)
    
        df = pd.DataFrame(rw) 
        return df 
    
    def BrownianMotion(self):
        # creating array
        bm = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(bm.shape[1]-1):
            for i in range(bm.shape[0]):
                bm[i][j+1] = bm[i][j] + np.random.normal(size=1)
    
        df = pd.DataFrame(bm)  
        return df

    def BrownianBridge(self):
        # creating Brownian motion
        bm = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(bm.shape[1]-1):
            for i in range(bm.shape[0]):
                bm[i][j+1] = bm[i][j] + np.random.normal(size=1)
        # array of Brownian Bridge
        bb = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(bb.shape[1]-1):
            for i in range(bb.shape[0]):
                bb[i][j+1] = bm[i][j] + -(j/self.steps)*bm[i][self.steps]
    
        df = pd.DataFrame(bb)  
        return df

    def BrownianMotionDrift(self, mu, sigma):
        # creating array
        bmd = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(bmd.shape[1]-1):
            for i in range(bmd.shape[0]):
                bmd[i][j+1] = bmd[i][j] + mu*self.dt  + sigma*np.sqrt(self.dt)*np.random.normal(size=1)
    
        df = pd.DataFrame(bmd)  
        return df
        
    def GeometricBrownianMotion(self, S0, alpha, beta):
        # creating array
        gbm = np.zeros( (self.n_times, self.steps+1))
        # initiate the loop
        for j in range(gbm.shape[1]):
            for i in range(gbm.shape[0]):
              if(j == 0):
                gbm[i][j] = S0
              else:
                gbm[i][j] = gbm[i][j-1]*np.exp(np.random.normal(loc=(alpha - (beta**2)/2)*self.dt, scale=np.sqrt(self.dt)*beta, size=1)) 
    
        df = pd.DataFrame(gbm)  
        return df