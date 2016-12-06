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
    """
    t0,per,rp,a,inc,ecc,w,u0,u1,u2,u3 = params    
    p = batman.TransitParams()       #object to store transit parameters 
    p.t0 = t0                        #time of inferior conjunction (0.0)
    p.per = per                      #orbital period (1.0)
    p.rp = rp                        #planet radius (in units of stellar radii) (0.1)
    p.a = a                          #semi-major axis (in units of stellar radii) (15.0)
    p.inc = inc                      #orbital inclination (in degrees) (87.0)
    p.ecc = ecc                      #eccentricity (0.0)
    p.w = w                          #longitude of periastron (in degrees) (90.0)
    p.limb_dark = limb_dark          #limb darkening model 
    p.u = [u0, u1, u2, u3]           #limb darkening coefficients (0.5) (0.1) (0.1) (-0.1)
    m = batman.TransitModel(p, t)    #initializes model 
    flux = m.light_curve(p)          #calculates white light curve  
    return p, m, flux

def wl_channel_flux(wl_params, m, p):
    """
    """
    rp,u0,u1,u2,u3 = wl_params    
    p.rp = rp                        #planet radius (in units of stellar radii) (0.1)
    p.u = [u0, u1, u2, u3]           #limb darkening coefficients  (0.5)  (0.1)  (0.1)  (-0.1)	
    flux = m.light_curve(p)          #calculates light curve  
    return flux

def white_noise(level, N):
    """
    """
    return level + level* np.random.rand(N)

def red_noise(a_params, m):	
    """
    """
    return np.sum(a_params*m + 1., axis=0)

def generate_a_params(level, N):
    """
    """
    m = np.zeros(8) + level*np.random.rand(8)
    phase = np.arange(N)*-0.01
    airmass = np.arange(N)*-0.01
    x1 = np.arange(N)*0.01
    x2 = np.arange(N)*0.02
    y1 = np.arange(N)*0.03
    y2 = np.arange(N)*0.02
    fwhm = np.arange(N)*-0.1
    skynoise = np.arange(N)*0.005
    return m, np.array([phase, airmass, x1, x2, y1, y2, fwhm, skynoise])

def generate_data(t_params, a_params, w_level, m, N, exptime):
    """
    """
    t0 = t_params[0]
    t = np.arange(t0 - exptime*N/2., t0 + exptime*N/2., exptime) 
    ferr = white_noise(w_level, N)
    p, model, signal = init_model(t_params, t)
    f = signal*red_noise(a_params, m) + ferr*np.random.randn(N)
    return t, f, ferr

def generate_data_gp(params, N, rng=(-0.025, 0.025)):
    """
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
    """
    print("# time (phase), flux, ferr, fwhm, skynoise")
    for k in range(len(t)):
        print("%f\t%f\t%f\t%f\t%f" % (t[k], f[k], ferr[k], a_params[6][k], 
                                        a_params[7][k]))

def write_aparams(t, a_params):
    """
    """
    print("# time (phase), phase, airmass, x1, x2, y1, y2")
    for k in range(len(t)):
        print("%f\t%f\t%f\t%f\t%f\t%f\t%f" % (t[k],a_params[0][k],a_params[1][k],a_params[2][k],a_params[3][k],a_params[4][k],a_params[6][k]))
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    np.random.seed(1234)
    truth = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1, 0.1, -0.1]
    #t, y, yerr = generate_data_gp(truth, 1000)
    m, a_params = generate_a_params(0.001, 500)
    t, f, ferr = generate_data(truth, a_params, 0.001, 0.001, 500, 0.0001)
    #write_lc(t, f, ferr, a_params, "fname", m, 0.001, 0.001)
    write_aparams(t, a_params)

