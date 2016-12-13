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
# -----------------------------------------------------------------------------
def init_model(params, t, limb_dark="nonlinear"):
    """
    arguments: list of transit parameters, times
    returns: batman transit parameter object, batman transit model object, 
             initial light curve
    """
    t0,per,rp,a,inc,ecc,w,u0,u1,u2,u3 = params    
    p = batman.TransitParams()  #object to store transit parameters 
    p.t0 = t0                   #time of inferior conjunction 
    p.per = per                 #orbital period 
    p.rp = rp                   #planet radius (in units of stellar radii) 
    p.a = a                     #semi-major axis (in units of stellar radii) 
    p.inc = inc                 #orbital inclination (in degrees) 
    p.ecc = ecc                 #eccentricity 
    p.w = w                     #longitude of periastron (in degrees) 
    p.limb_dark = limb_dark     #limb darkening model 
    p.u = [u0, u1, u2, u3]      #limb darkening coefficients 
    m = batman.TransitModel(p, t)  #initializes model 
    flux = m.light_curve(p)        #calculates white light curve  
    return p, m, flux

def wl_channel_flux(wl_params, m, p):
    """
    arguments: list of wl-specific transit parameters, 
               batman transit model object, batman tansit parameter object
    returns: light curve for that wavelength
    """
    rp,u0,u1,u2,u3 = wl_params    
    p.rp = rp                    #planet radius (in units of stellar radii) 
    p.u = [u0, u1, u2, u3]       #limb darkening coefficients  
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
    return np.sum((a_params.T*slopes).T, axis=0)

def generate_a_params(level, N):
    """
    arguments: level of red noise, length of light curve
    returns: 8 x N array of auxiliary parameter values over time
    """
    slopes = np.zeros(8) + level*np.random.randn(8)
    phase = np.linspace(0,0.25,N)
    airmass = np.linspace(1.2,0.5,N)
    x1 = np.arange(N)*(1.0/N)
    x2 = np.arange(N)*(1.0/N)
    y1 = np.arange(N)*(1.0/N)
    y2 = np.arange(N)*(1.0/N)
    fwhm = np.random.rand(N)*2.25
    skynoise = fwhm*10.0
    return slopes, np.array([phase, airmass, x1, x2, y1, y2, fwhm, skynoise])

def generate_data_gp(params, N, rng=(-0.025, 0.025)):
    """
    arguments:
    returns:
    """
    gp = george.GP(0.1 * kernels.ExpSquaredKernel(3.3))
    #to-do: fix to regular cadence instead...
    t = rng[0] + np.diff(rng) * np.sort(np.random.rand(N)) 
    y = gp.sample(t)
    y += model(params, t)
    yerr = 0.001 + 0.001 * np.random.rand(N)
    y += yerr * np.random.randn(N)
    return t, y, yerr

def write_lc(t, f, ferr, a_params, fname, m, w_level, r_level):
    """
    arguments: times, flux, flux error, auxliary parameter array
               correlation coefficients, white noise level, red noise level
    returns: 0 if successfully saved a light curve to fname 
    """
    ofile = open(fname,"w")
    ofile.write("# time (phase), flux, ferr, fwhm, skynoise\n")
    # add header with more info
    ofile.write("# fwhm corr. coeff.: %f, skynoise corr. coeff.: %f, white level: %f,"
          "red level: %f\n" % (m[6],m[7],w_level,r_level))
    for k in range(len(t)):
        ofile.write("%f\t%f\t%f\t%f\t%f\n" % (t[k], f[k], ferr[k], a_params[6][k], 
                                        a_params[7][k]))
    ofile.close()
    return 0

def write_aparams(t, a_params, m, w_level, r_level, fname):
    """
    arguments: times, auxiliary parameters, correlation coefficients,
               white noise level, red noise level
    returns: 0 if saved to fname successfully
    """
    ofile = open(fname,"w")
    ofile.write("# time (phase), phase, airmass, x1, x2, y1, y2\n")
    # add header with more info
    ofile.write("phase corr. coeff.: %f, airmass corr. coeff.: %f, x1 corr. coeff.: %f,"
          "x2 corr. coeff.: %f, y1 corr. coeff.: %f, y2 corr. coeff.: %f,"
          "white level: %f, red level: %f\n"
          %(m[0],m[1],m[2],m[3],m[4],m[5],w_level,r_level))
    for k in range(len(t)):
        ofile.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (t[k],a_params[0][k],
              a_params[1][k], a_params[2][k], a_params[3][k], 
              a_params[4][k], a_params[6][k]))
    ofile.close()
    return 0

def gen_obs_set(fileroot, t_params, radii, limb_darkening, wl,   
                w_scale, r_scale, w_level, r_level, N, exptime):
    """
    arguments: transit parameter list, radii for each wavelength,
               list of limb darkening coefficients for each wavelength
               scales of white noise, scales of red noise
    returns:
    """
    # initialize model
    t0 = t_params[0]
    t = np.arange(t0 - exptime*N/2., t0 + exptime*N/2., exptime) 
    p, model, signal_0 = init_model(t_params, t)

    # write_aparams 
    slopes, a_params = generate_a_params(r_level, N)
    write_aparams(t, a_params, slopes, w_level, r_level, 
                  fileroot+".aparams.dat")

    # for each radii: 
    for k in range(len(radii)):   
        # pure transit signal
        wl_params = [radii[k], limb_darkening[k][0], limb_darkening[k][1],
                     limb_darkening[k][2], limb_darkening[k][3]]
        signal = wl_channel_flux(wl_params, model, p)
        # white noise to be added
        ferr = white_noise(w_level, N)*w_scale[k]    
        # scale the fwhm and sky noise correlated rednoise for that wl
        fwhm, skynoise = r_scale[k]*a_params[6], r_scale[k]*a_params[7]
        wl_a_params = np.concatenate((a_params[:6],np.array([fwhm,skynoise])))
        # put  it all together
        f = signal*red_noise(wl_a_params, slopes) + ferr*np.random.randn(N)
        # write to a file
        write_lc(t, f, ferr, wl_a_params, fileroot+"."+str(radii[k])+".dat",
                 slopes*r_scale[k], w_level, r_level)


# -----------------------------------------------------------------------------
if __name__ == "__main__":

    np.random.seed(1234)
    truth = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1, 0.1, -0.1]
    # t, y, yerr = generate_data_gp(truth, 1000)
    # 10 wl channels (probably read this from a file, so have a record)
    wl = [0.1,2.0]        # central wavelength
    radii = [0.5,0.1]     # effective radius of the planet
    ldark = [[0.5, 0.1, 0.1, -0.1],[0.5, 0.1, 0.1, -0.1]]     # limb darkening coefficients for the star
    starspec = [0.2,0.3]  # flux level coming from star (to scale white noise)
    fwhm = [0.3,0.4]      # fwhm of psf for that wavelength (to scale red noise)
    skyspec = [0.5,0.6]   # sky flux level (to scale red noise)

    # convert to starspec, fwhm, skyspec  to w_scale, r_scale
    w_scale = [1./starspec[k] for k in range(len(starspec))]
    r_scale = [np.sqrt(fwhm[k]**2.+skyspec[k]**2.) for k in range(len(fwhm))]

    # generate data:
    fileroot = "testing"
    w_level, r_level = 0.001, 0.001
    gen_obs_set(fileroot, truth, radii, ldark, wl, 
                w_scale, r_scale, w_level, r_level, 500, 0.005)

    # tests/checks:
    # no nans, all files saved with right # of rows and columns
    #
    # plots:
    # each a_param over time 
    # each a_param vs. flux & the slope it is supposed to have...
    # all the light curves
    # light curve + known model



#fileroot, t_params, radii, limb_darkening, wl, w_scale, r_scale, w_level, r_level, N, exptime = fileroot, truth, radii, ldark, wl, w_scale, r_scale, w_level, r_level, 500, 0.005
