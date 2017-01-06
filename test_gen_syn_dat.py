from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as pl
import emcee
import corner
import batman
import george
from   george import kernels
import os
import gen_syn_data as gsd
import unittest
 
class TestFunctions(unittest.TestCase):
    """Sample test case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        np.random.seed(1234)
        # transit parameters in order: t0,per,rp,a,inc,ecc,w,u0,u1
        # see def init_model() for physical meanings
        self.params = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1]
        # central wavelengths in microns for each channel
        self.wl = [500, 650, 800, 950, 1100]  
        # fractional radius of planet       
        self.radii = [0.05, 0.08, 0.1, 0.12, 0.15]   
        # limb darkening coefficients for the star
        self.ldark = [[0.45, 0.1],[0.55, 0.1],[0.45, 0.11],[0.35,0.16],[0.5,0.1]]    
        # flux level coming from star normalized to channel with maximum flux (to scale white noise)
        self.starspec = [1.0, 1.0, 1.0, 1.0, 1.0]  
        # fwhm of psf for that wavelength normalized to channel with maximum psf size (to scale red noise)
        self.fwhm = [np.sqrt(2.), np.sqrt(2.), np.sqrt(2.), np.sqrt(2.), np.sqrt(2.)]      
        # sky flux level normalized to maximum sky flux level (to scale red noise)
        self.skyspec = [np.sqrt(2.), np.sqrt(2.), np.sqrt(2.), np.sqrt(2.), np.sqrt(2.)]   

        # convert starspec, fwhm, skyspec  to w_scale, r_scale
        self.w_scale = [1./self.starspec[k] for k in range(len(self.starspec))] # brighter channels will have lower white noise levels
        self.r_scale = [np.sqrt(self.fwhm[k]**2.+self.skyspec[k]**2.) for k in range(len(self.fwhm))]

        self.t0 = self.params[0]
        self.N = 300
        self.phase_range = (-0.0025, 0.0025)
        self.exptime = (self.phase_range[1]-self.phase_range[0])/self.N
        self.t = np.arange(self.t0 - self.exptime*self.N/2., self.t0 + self.exptime*self.N/2., self.exptime) 
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

     
    def testInit_model(self):
        """Test routine A"""

        p, m, flux = gsd.init_model(self.params, self.t, limb_dark="quadratic")
        t0,per,rp,a,inc,ecc,w,u0,u1 = self.params 
        self.assertTrue(p.t0 == t0)                   
        self.assertTrue(p.per == per)                 
        self.assertTrue(p.rp == rp)                   
        self.assertTrue(p.a == a)                     
        self.assertTrue(p.inc == inc)                 
        self.assertTrue(p.ecc == ecc)             
        self.assertTrue(p.w == w)            
        self.assertTrue(p.limb_dark == "quadratic")   
        self.assertTrue(p.u[0] == u0)
        self.assertTrue(p.u[1] == u1)          
        self.assertTrue(len(flux)==len(self.t))
        self.assertTrue(np.min(flux)>=0.0)
        self.assertTrue(np.max(flux)<=1.0)

        pass
     
    def testWl_channel_flux(self):
        """Test routine B"""
        p, m, flux = gsd.init_model(self.params, self.t, limb_dark="quadratic")
        wl_params = [0.99, 0.4, 0.4]
        flux2 = gsd.wl_channel_flux(wl_params, m, p)
        self.assertTrue(p.rp==wl_params[0])
        self.assertTrue(p.u==wl_params[1:])
        self.assertFalse(np.array_equal(flux,flux2))

        pass
    
    def testWhite_noise(self):
        """Test routine B"""
        level1 = 0.0
        level2 = 0.1
        level3 = 0.5
        noise1 = gsd.white_noise(level1, self.N)
        noise2 = gsd.white_noise(level2, self.N)
        noise3 = gsd.white_noise(level3, self.N)

        self.assertTrue(np.std(noise1)==0.0)
        self.assertTrue(np.mean(noise1)==0.0)
        self.assertTrue(np.std(noise2) < np.std(noise3))
        self.assertTrue(len(noise1)==self.N)

        pass

    def testGenerate_aparams(self):
        """Test routine B"""
        level1 = 0.0
        level2 = 0.1
        level3 = 0.5
        slopes1, aparams1 = gsd.generate_a_params(level1, self.N)
        slopes2, aparams2 = gsd.generate_a_params(level2, self.N)
        slopes3, aparams3 = gsd.generate_a_params(level3, self.N)

        self.assertTrue(len(aparams1[0])==self.N)
        self.assertTrue(len(slopes1)==4)
        self.assertTrue(len(aparams1)==4)
        self.assertTrue(np.array_equal(slopes1, np.zeros(4.0)))
        self.assertFalse(np.array_equal(slopes2,slopes3))
        self.assertTrue(np.array_equal(aparams1[:2],aparams2[:2]))

        pass

    def testRed_noise(self):
        """Test routine B"""
        slopes, a_params = gsd.generate_a_params(0.0, self.N)
        noise = gsd.red_noise(a_params, slopes)
        self.assertTrue(len(noise)==self.N)
        self.assertTrue(np.mean(noise)==1.0)

        slopes, a_params = gsd.generate_a_params(0.05, self.N)        
        noise = gsd.red_noise(a_params, slopes)
        self.assertTrue(len(noise)==self.N)
        self.assertTrue(np.mean(noise) != 1.0)

        pass

    def testWrite_lc(self):
        """Test routine B"""
        fname = "testing_write_lc.txt"
        m = np.arange(4)
        a_params = np.zeros((4,self.N)) 
        a_params = (m*(a_params.T+1)).T
        wl_params = [0.15, 0.1, 0.1]
        ferr = np.zeros(self.N) + 0.001
        f = np.zeros(self.N) + 1.0
        t = np.arange(self.N)
        gsd.write_lc(t, f, ferr, a_params, fname, m, 0.0001, 0.0, wl_params)

        data = np.loadtxt("testing_write_lc.txt", unpack=True)

        time, flux, flux_err, fwhm, skynoise, position, airmass = data

        self.assertTrue(np.array_equal(t, time))
        self.assertTrue(np.array_equal(f, flux))
        self.assertTrue(np.array_equal(flux_err, ferr))
        self.assertTrue(np.array_equal(a_params[3],fwhm))
        self.assertTrue(np.array_equal(a_params[2],skynoise))
        self.assertTrue(np.array_equal(a_params[1],position))
        self.assertTrue(np.array_equal(a_params[0],airmass))

        self.assertTrue(len(time)==self.N)

        os.system("rm "+fname)

        pass

    def testGen_obs_et(self):
        """Test routine B"""

        

        pass

    def testCheck_linear_corr_slope(self):
        """Test routine """
        pass


if __name__ == '__main__':
    unittest.main()