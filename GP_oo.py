
# coding: utf-8

# In[1]:

#%matplotlib inline
import numpy as np
from matplotlib import pyplot as plt
import emcee
import george
from george import kernels

import batman


# In[3]:

class TransitModel(object):
    
    def __init__(self, rp0, u0):
        # initialize batman 
        self.params = batman.TransitParams() 
        self.params.t0 = 0.                        #time of inferior conjunction
        self.params.per = 1.                       #orbital period
        self.params.rp = rp0                       # 0.1 !!!! planet radius (in units of stellar radii)  - prior [0, 1]
        self.params.a = 15.                        #semi-major axis (in units of stellar radii)
        self.params.inc = 87.                      #orbital inclination (in degrees)
        self.params.ecc = 0.                       #eccentricity
        self.params.w = 90.                        #longitude of periastron (in degrees)
        self.params.limb_dark = "nonlinear"        # !!!! quadratic limb darkening model
        self.params.u = u0                         # [0.5, 0.1, 0.1, -0.1]  !!!! limb darkening coefficients   prior [ -1, 1   
        self.model_initialized = True
        
        # initialize the data
        self.t = np.linspace(0,0,1)
        self.y = None
        self.err = None
        self.data_initialized = False
        
        #initialize empty model
        self.batman_model = batman.TransitModel(self.params, self.t) 
        
        # initialize the result variables 
        self.lnprob = None
    
    def update_data(self, time, obs, errors):
        '''Update the data for the given parameters'''
        self.t = time
        self.y = obs
        self.err = errors
    
    def update_params(self, rp_new, u_new):
        '''Update the parameters of the model'''
        self.params.rp = rp_new
        self.params.u = u_new
            
    def model(self):
        '''Returns the flux values array'''
        return self.batman_model.light_curve(self.params)    
    
    def lnlike_gp(self):
        a, tau = self.params.a, self.params.u
        #TODO: update the kernel for the GP
        gp = george.GP(a * kernels.Matern32Kernel(tau))
        gp.compute(t, yerr)
        return gp.lnlikelihood(y - self.model())

    def lnprior_base(self, rp0, u0, sig20 = 0):
        #TODO: what is sig2 in Batman 
        rp, u, sig2 = rp0, u0, sig20
        if not 0 < rp < 1:
            return -np.inf
        if not -1 < u < 1:
            return -np.inf
        if not 0 < sig2 < 3.0:
            return -np.inf
        return 0.0

    def lnprior_gp(self):
        #TODO: what is lna and ltau in Batman 
        lna, lntau = 0,0 
        if not -5 < lna < 5:
            return -np.inf
        if not -5 < lntau < 5:
            return -np.inf
        return self.lnprior_base()

    def lnprob_gp(self):
        ''' Function used in emcee fitting proocess, the key result of the class, the result stored in self.lnpob'''
        lp = self.lnprior_gp()
        if not np.isfinite(lp):
            return -np.inf
        self.lnprob = lp + self.lnlike_gp()
        return self.lnprob


# In[ ]:



