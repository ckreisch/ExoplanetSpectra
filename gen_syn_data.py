#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as pl
import emcee
import corner
import batman
import george
from   george import kernels
import os
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
def init_model(params, t, limb_dark="quadratic"):
    """
    arguments: list of transit parameters, times
    returns: batman transit parameter object, batman transit model object, 
             initial light curve
    """
    t0,per,rp,a,inc,ecc,w,u0,u1 = params    
    p = batman.TransitParams()  #object to store transit parameters 
    p.t0 = t0                   #time of inferior conjunction 
    p.per = per                 #orbital period 
    p.rp = rp                   #planet radius (in units of stellar radii) 
    p.a = a                     #semi-major axis (in units of stellar radii) 
    p.inc = inc                 #orbital inclination (in degrees) 
    p.ecc = ecc                 #eccentricity 
    p.w = w                     #longitude of periastron (in degrees) 
    p.limb_dark = limb_dark     #limb darkening model 
    p.u = [u0, u1]      #limb darkening coefficients 
    m = batman.TransitModel(p, t)  #initializes model 
    flux = m.light_curve(p)        #calculates white light curve  
    return p, m, flux

def wl_channel_flux(wl_params, m, p):
    """
    arguments: list of wl-specific transit parameters, 
               batman transit model object, batman tansit parameter object
    returns: light curve for that wavelength
    """
    rp,u0,u1 = wl_params    
    p.rp = rp                    #planet radius (in units of stellar radii) 
    p.u = [u0, u1]       #limb darkening coefficients  
    flux = m.light_curve(p)      #calculates light curve  
    return flux

def white_noise(level, N):
    """
    arguments: level of white noise, length of light curve 
    returns: white noise curve to be ADDED
    """
    return level + level*np.random.rand(N)

def red_noise(a_params, slopes):	
    """
    arguments: array of auxiliary parameters, list correlation 
               coefficients/slopes
    returns: red noise curve to be MULTIPLIED
    """
    red_superposition = np.sum((a_params.T*slopes).T, axis=0) + 1.
    norm = np.median(red_superposition)
    return red_superposition/norm

def generate_a_params(level, N):
    """
    arguments: level of red noise, length of light curve
    returns: len 4 array of slopes to use in linear correlation
             and a 4 x N array of auxiliary parameter value measures 
    """
    slopes = np.zeros(4) + level*np.random.randn(4)
    # approximate change in  airmass over course of observation with a quadratic
    airmass = -0.001*np.arange(-0.1*N/4., 0.3*N/4.,0.1)**2. + 1.6  
    # approximate change in position on detector over course of observation
    # with cube root 
    pos = np.concatenate((-1.*np.arange(0., N/2.,1.)[::-1]**(1./3.),  
                         np.arange(1., N/2.+1,1.)**(1./3.)))*0.05 + 10.0      

    # approximate full-width-half-maximum size of psf with sine wave        
    fwhm = np.sin(np.arange(N)/(25.0*np.pi))*2.25  

    # random skynoise levels but also related to fhwm
    skynoise = fwhm + np.random.randn(N)*0.00001    


    return slopes, np.array([airmass, pos, skynoise, fwhm])

def write_lc(t, f, ferr, a_params, fname, m, w_level, r_level, wl_params):
    """
    arguments: times, flux, flux error, auxliary parameter array
               correlation coefficients, white noise level, red noise level
    returns: 0 if successfully saved a light curve to fname 
    """
    ofile = open(fname,"w")
    ofile.write("# time (phase), flux, ferr, fwhm, skynoise, position, airmass\n")
    # add header with more info
    ofile.write("# white scalel: %f, red scale: %f, fwhm corr. coeff.: %f, skynoise corr. coeff.: %f, position corr. coeff.: %f, airmass corr. coeff.: %f\n" % (w_level,r_level,m[3],m[2],m[1],m[0]))
    ofile.write("# transit parameters: rp = %f, u0 = %f, u1 = %f\n" % (wl_params[0],wl_params[1],wl_params[2]))
    for k in range(len(t)):
        ofile.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (t[k], f[k], ferr[k], a_params[3][k], a_params[2][k], a_params[1][k], a_params[0][k]))
    ofile.close()
    return 0

def write_expected_vals(fname, t_params, radii, slopes, w_level, r_level,
                        w_scale, r_scale):
    """
    arguments:
    returns: 0 if successfully saved file with table of expected values

    """
    airmass, pos, skynoise, fwhm = slopes
    t0,per,rp,a,inc,ecc,w,u0,u1 = t_params
    dic = {'airmass': airmass, 'pos' : pos, 'skynoise' : skynoise,
           'fwhm' : fwhm, 't0' : t0, 'per' : per, 'a' : a, 'inc' : inc,
           'ecc' : ecc, 'w' : w, 'w_level' : w_level, 'r_level' : r_level}
    ofile = open(fname,"w")
    for key in dic.keys():
        ofile.write("# " + key + " = " + str(dic[key]) + "\n")
    ofile.write("# WL: rp: u0: u1: w_scale: r_scale:\n")
    for k in range(len(radii)):
        ofile.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (WL[k],rp[k],u0[k],u1[k],w_scale[k],r_scale[k]))

    return 0

def gen_obs_set(fileroot, t_params, radii, limb_darkening, wl,   
                w_scale, r_scale, w_level, r_level, N=300, phase_range=(-0.025,0.025)):
    """
    arguments: transit parameter list, radii for each wavelength,
               list of limb darkening coefficients for each wavelength
               scales of white noise, scales of red noise
    returns: 0 if successful, saves data generated into text files
    """
    # initialize model
    t0 = t_params[0]
    exptime = (phase_range[1]-phase_range[0])/N
    t = np.arange(t0 - exptime*N/2., t0 + exptime*N/2., exptime) 
    p, model, signal_0 = init_model(t_params, t)

    # generate auxiliary parameters
    slopes, a_params = generate_a_params(r_level, N)

    # for each radii: 
    for k in range(len(radii)):   
        # pure transit signal
        wl_params = [radii[k], limb_darkening[k][0], limb_darkening[k][1]]
        signal = wl_channel_flux(wl_params, model, p)
        # white noise to be added
        ferr = white_noise(w_level, N)*w_scale[k]    
        # scale the fwhm and sky noise correlated rednoise for that wl
        fwhm, skynoise = r_scale[k]*a_params[3], r_scale[k]*a_params[2]
        wl_a_params = np.concatenate((a_params[:2],np.array([fwhm,skynoise])))
        # put  it all together
        f = signal*red_noise(wl_a_params, slopes) + ferr*np.random.randn(N)
        # write to a file
        fname = fileroot+"_lc_"+str(wl[k])+".txt"
        write_lc(t, f, ferr, wl_a_params, fname ,
                 slopes*r_scale[k], w_level, r_level, wl_params)

    fname = fileroot+"expected_values.txt"   
    write_expected_vals(fname, t_params, radii, slopes, w_level, r_level,
                        w_scale, r_scale)
    return 0

# -----------------------------------------------------------------------------
# Define some global constants, all data generated will take on these
# root parameters, with noise added on top
#
# transit parameters in order: t0,per,rp,a,inc,ecc,w,u0,u1
# see def init_model() for physical meanings
truth = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1]
# central wavelengths in microns for each channel
wl = [500, 650, 800, 950, 1100, 1350]  
# fractional radius of planet       
radii = [0.05, 0.08, 0.1, 0.12, 0.15, 0.09]   
# limb darkening coefficients for the star
ldark = [[0.45, 0.1],[0.55, 0.1],[0.45, 0.11],[0.35,0.16],[0.5,0.1],[0.3,0.2]]    
# flux level coming from star normalized to channel with maximum flux (to scale white noise)
starspec = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  
# fwhm of psf for that wavelength normalized to channel with maximum psf size (to scale red noise)
fwhm = [np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), 
        np.sqrt(1./2.)]      
# sky flux level normalized to maximum sky flux level (to scale red noise)
skyspec = [np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), 
           np.sqrt(1./2.)] 
# convert starspec, fwhm, skyspec  to w_scale, r_scale
w_scale = [1./starspec[k] for k in range(len(starspec))] # brighter channels will have lower white noise levels
r_scale = [np.sqrt(fwhm[k]**2.+skyspec[k]**2.) for k in range(len(fwhm))]

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv)!=5:
        raise ValueError("Run as python gen_syn_data.py <output_directory> " +\
                "<N data in lightcurve> <white noise level> <red noise level>")

    output_dir, N, w_level, r_level = sys.argv[1:]

    try:
        N = int(N)
        w_level = float(w_level)
        r_level = float(r_level)
    except ValueError:
        print "command line arguments need to be convertable to string" +\
              " integer float float"
        raise

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # for reproducability seed the numpy random number generator
    np.random.seed(1234)
  
    # generate one set of data and look at it:
    gen_obs_set(output_dir, truth, radii, ldark, wl, 
                w_scale, r_scale, w_level, r_level, N=N)

    plt.figure(1)
    for wavelength in wl:
        check = np.loadtxt(output_dir+'lc_'+str(wavelength)+'.txt',unpack=True)
        plt.plot(check1[0],check1[1])
    plt.show()


    # # generate suite of data, 
    # # 3 red levels and 3 white levels saved in their own directories
    # rootname = ""
    # descriptors = ["none","low","some"]
    # w_levels = [0.0, 0.0001, 0.0005]
    # r_levels = [0.0, 0.00008, 0.0002]

    # for i in range(3):
    #     w_level = w_levels[i]
    #     for j in range(3):
    #         r_level = r_levels[j]
    #         dname = rootname + '_white_' + descriptors[i] + '_red_' + descriptors[j]
    #         os.system('mkdir '+ dname)
    #         fileroot = dname+"/"+rootname
    #         gen_obs_set(fileroot, truth, radii, ldark, wl,
    #                     w_scale, r_scale, w_level, r_level, N=150)  