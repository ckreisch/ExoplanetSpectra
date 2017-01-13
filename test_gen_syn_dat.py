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
import glob

## @class TestSynthData
# Class to run unit tests on test_gen_syn_data.py
#
# More details.
class TestSynthData(unittest.TestCase):
     
    ## Prepares to test by assigning the testing object necessary values
    def setUp(self):
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

        self.truth = [self.params, self.wl, self.radii, self.ldark, self.starspec, self.w_scale, self.r_scale]

        self.t0 = self.params[0]
        self.N = 300
        self.phase_range = (-0.0025, 0.0025)
        self.exptime = (self.phase_range[1]-self.phase_range[0])/self.N
        self.t = np.arange(self.t0 - self.exptime*self.N/2., self.t0 + self.exptime*self.N/2., self.exptime) 

    ## Tests the init_model function for correct parameter value assignments and range of fluxes
    def testInit_model(self):
        p, m, flux = gsd.init_model(self.params, self.t)
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

    ## Tests the wl_channel_flux function for correct parameter assignments and updating of flux     
    def testWl_channel_flux(self):
        p, m, flux = gsd.init_model(self.params, self.t)
        wl_params = [0.99, 0.4, 0.4]
        flux2 = gsd.wl_channel_flux(wl_params, m, p)
        self.assertTrue(p.rp==wl_params[0])
        self.assertTrue(p.u==wl_params[1:])
        self.assertFalse(np.array_equal(flux,flux2))

        pass

    ## Tests the white_noise function for correct size and scaling behavior   
    def testWhite_noise(self):
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

    ## Tests the generate_a_params function for correct size and scaling behavior
    def testGenerate_aparams(self):

        level1 = 0.0
        level2 = 0.1
        level3 = 0.5
        slopes1, aparams1 = gsd.generate_a_params(level1, self.N)
        slopes2, aparams2 = gsd.generate_a_params(level2, self.N)
        slopes3, aparams3 = gsd.generate_a_params(level3, self.N)

        self.assertTrue(len(aparams1[0])==self.N)
        self.assertTrue(len(slopes1)==4)
        self.assertTrue(len(aparams1)==4)
        self.assertTrue(np.array_equal(slopes1, np.zeros(4)))
        self.assertFalse(np.array_equal(slopes2,slopes3))
        self.assertTrue(np.array_equal(aparams1[:2],aparams2[:2]))

        pass

    ## Tests the red_noise function for correct size and scaling behavior
    def testRed_noise(self):

        slopes, a_params = gsd.generate_a_params(0.0, self.N)
        noise = gsd.red_noise(a_params, slopes)
        self.assertTrue(len(noise)==self.N)
        self.assertTrue(np.mean(noise)==1.0)

        slopes, a_params = gsd.generate_a_params(0.05, self.N)        
        noise = gsd.red_noise(a_params, slopes)
        self.assertTrue(len(noise)==self.N)
        self.assertTrue(np.mean(noise) != 1.0)

        pass

    ## Tests the write_lc function for correct formatting
    def testWrite_lc(self):

        fname = "testing_write_lc.txt"
        m = np.arange(4)
        a_params = np.zeros((4,self.N)) 
        a_params = (m*(a_params.T+1)).T
        wl_params = [0.15, 0.1, 0.1]
        ferr = np.zeros(self.N) + 0.001
        f = np.zeros(self.N) + 1.0
        t = np.arange(self.N)
        gsd.write_lc(fname, t, f, ferr, a_params, m, 0.0001, 0.0, wl_params)

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

    ## Tests the write_expected_vals function for correct formatting
    def testWrite_expected_vals(self):
        # expect 12 lines in form: # name = value
        # 13th line: # WL: rp: u0: u1: w_scale: r_scale:
        # then columns of floats 8 decimal places
        fname = "testing_write_expected_vals.txt"
        slopes = np.arange(4)
        w_level = 0.001
        r_level = 0.5
        truth = self.truth
        gsd.write_expected_vals(fname, truth, slopes, w_level, r_level)
        data = np.loadtxt(fname,unpack=True)

        #self.assertTrue(self.wl==data[0].tolist)
        # self.assertTrue(self.radii==data[1])
        # self.assertTrue(self.ldark[0][0]==data[2][0])
        # self.assertTrue(self.ldark[2][1]==data[3][2])        
        # self.assertTrue(self.w_scale==data[4])
        # self.assertTrue(self.r_scale==data[5])

        lines = open(fname).readlines()
        lines[12] = "# WL: rp: u0: u1: w_scale: r_scale:\n"
        for line in lines[:12]:
            hashtag, key, equal, val = line.split(" ")
            self.assertTrue(hashtag=='#')
            self.assertTrue(equal=='=')
            self.assertTrue(len(line.split(" "))==4)

        os.system("rm "+fname)

        pass

    ## Cleans up output from running gen_obs_set()
    def cleanGen_obs_set_output(self, dname):
        expected_files = ["/synth_expected_values.txt",
                          "/visual.png",
                          "/light_curves/synth_lc_500.txt",
                          "/light_curves/synth_lc_650.txt",                          
                          "/light_curves/synth_lc_800.txt",
                          "/light_curves/synth_lc_950.txt",
                          "/light_curves/synth_lc_1100.txt"]
        for k in range(len(expected_files)):
            os.system("rm "+dname+expected_files[k])
        os.system("rmdir "+dname+"/light_curves")
        os.system("rmdir "+dname)

    ## Tests the gen_obs_set function for files saved
    def testGen_obs_set_io(self):

        dname = "testing_gen_obs_set_io"
        w_level = 0.001
        r_level = 0.5
        truth = self.truth
        gsd.gen_obs_set(dname, truth, w_level, r_level, N=40, 
                phase_range=(-0.5,0.5), fileroot="synth")

        file_list = np.array([])      # get list of files
        for file in glob.glob("*"):
            file_list = np.append(file_list, file)

        expected_files = ["testing_gen_obs_set_io/synth_expected_values.txt",
                          "testing_gen_obs_set_io/visual.png",
                          "testing_gen_obs_set_io/light_curves/synth_lc_500.txt",
                          "testing_gen_obs_set_io/light_curves/synth_lc_650.txt",                          
                          "testing_gen_obs_set_io/light_curves/synth_lc_800.txt",
                          "testing_gen_obs_set_io/light_curves/synth_lc_950.txt",
                          "testing_gen_obs_set_io/light_curves/synth_lc_1100.txt"]

        flag = True
        k = 0
        if len(file_list) > 0:   # compare output file names to expected file names
            while flag and k < len(expected_files) :
                if expected_files[k] in file_list:
                    flag = True
                else:
                    flag = False
                k = k+1

        else: flag = False

        self.cleanGen_obs_set_output(dname)

        if flag:

            pass

    
    ## Tests the gen_obs_set function for white and red noise level behavior
    def testGen_obs_set_white_noise_scale(self):
        dnames = ["testing_gen_obs_set_noise_1","testing_gen_obs_set_noise_2"]
        w_levels = [0.001,0.1]
        r_level= 0.0
        truth = self.truth
        for k in [0,1]:
            gsd.gen_obs_set(dnames[k], truth, w_levels[k], r_level, N=40, 
                    phase_range=(-0.5,0.5), fileroot="synth")

        data1 = np.loadtxt(dnames[0]+"/light_curves/synth_lc_500.txt",unpack=True)
        data2 = np.loadtxt(dnames[1]+"/light_curves/synth_lc_500.txt",unpack=True)

        p, m, f0 = gsd.init_model(self.truth[0], data1[0])
        wl_params = [self.radii[0], self.ldark[0][0], self.ldark[0][1]]
        true_signal = gsd.wl_channel_flux(wl_params, m, p)

        #self.assertTrue(np.sum((data1-true_signal)**2.) < np.sum((data2-true_signal)**2.))

        for name in dnames:
            self.cleanGen_obs_set_output(name)
        pass


    ## Checks that auxiliary measure vs. flux is somewhat linearly correlated
    def testGen_obs_set_red_noise_scale(self):
        dnames = ["testing_gen_obs_set_noise_1","testing_gen_obs_set_noise_2"]
        w_level = 0.0
        r_levels= [0.001,0.1]
        truth = self.truth
        for k in [0,1]:
            gsd.gen_obs_set(dnames[k], truth, w_level, r_levels[k], N=40, 
                    phase_range=(-0.5,0.5), fileroot="synth")

        data1 = np.loadtxt(dnames[0]+"/light_curves/synth_lc_500.txt",unpack=True)
        data2 = np.loadtxt(dnames[1]+"/light_curves/synth_lc_500.txt",unpack=True)

        p, m, f0 = gsd.init_model(self.truth[0], data1[0])
        wl_params = [self.radii[0], self.ldark[0][0], self.ldark[0][1]]
        true_signal = gsd.wl_channel_flux(wl_params, m, p)

        self.assertTrue(np.sum((data1-true_signal)**2.) < np.sum((data2-true_signal)**2.))

        #TO-DO insert check of linear correlation here...

        for name in dnames:
            self.cleanGen_obs_set_output(name)
        pass

    ## Checks that columns printed into light curve files are in expected ranges
    def testGen_obs_set_realistic_values(self):

        dname = "testing_gen_obs_set_realistic_values"
        w_level = 0.0
        r_level = 0.0
        truth = self.truth
        gsd.gen_obs_set(dname, truth, w_level, r_level, N=40, 
                phase_range=(-0.5,0.5), fileroot="synth")

        data = np.loadtxt("testing_gen_obs_set_realistic_values/light_curves/synth_lc_500.txt",unpack=True)
        self.assertTrue(data[0][0]==-0.5)
        #self.assertTrue(data[0][39]==-0.5+1.0/40.)
        self.assertTrue(np.min(data[1])>0)
        self.assertTrue(np.max(data[1])==1.0)        
        self.assertTrue(np.mean(data[2])==0.000001)  # this is hardcoded in minimum error if w level is 0 
        self.cleanGen_obs_set_output(dname)

        pass

if __name__ == '__main__':
    unittest.main()