import numpy as np
import matplotlib.pyplot as plt

import george
from george import kernels
import batman
import corner

import mcmc
import lc_class
# import gp_model # waiting for this piece from Polina still

# following definiitions are replacing gp_model for now -----------------------
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
    flux = m.light_curve(p)        #calculates light curve
    return p, m, flux

def model(params, t):
    rp, u0, u1, u2, u3 = params       # the wavelength dependent params
    transit_pars.rp = rp            # planet radius (in units of stellar radii)
    transit_pars.u = [u0, u1, u2, u3] #limb darkening coefficients
    flux = model_object.light_curve(transit_pars)  #calculates light curve
    return flux

def lnlike_base(p, t, y, yerr):
    inv_sigma2 = 1.0/(yerr**2 + model(p,t)**2)
    return -0.5*(np.sum((y-model(p,t))**2*inv_sigma2 - np.log(inv_sigma2)))

def lnprior_base(p):
    rp, u0, u1, u2, u3 = p
    if not 0.0 <= rp <=1.0:
        return -np.inf
    if not -1.0 <= u0 <= 1.0:
        return -np.inf
    if not -1.0 <= u1 <= 1.0:
        return -np.inf
    if not -1.0 <= u2 <= 1.0:
        return -np.inf
    if not -1.0 <= u3 <= 1.0:
        return -np.inf
    return 0.0

def lnprob_base(p,t,y,yerr):
    lp = lnprior_base(p)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike_base(p,t,y,yerr)

def lnlike_gp(p, t, y, yerr):
    a, tau = np.exp(p[:2])
    gp = george.GP(a * kernels.Matern32Kernel(tau))
    gp.compute(t, yerr)
    return gp.lnlikelihood(y - model(p[2:], t))

def lnprior_gp(p):
    lna, lntau = p[:2]
    if not -5 < lna < 5:
        return -np.inf
    if not -5 < lntau < 5:
        return -np.inf
    return lnprior_base(p[2:])

def lnprob_gp(p, t, y, yerr):
    lp = lnprior_gp(p)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike_gp(p, t, y, yerr)

if __name__ == "__main__":
    # replacing user parameter file for now -----------------------------------
    transit_parameters = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1, 0.1,
                         -0.1]
    p0 = [0.1, 0.1, 0.1, 0.5, 0.1, 0.1, -0.1]
    priors = [(0,1),(-0.5,0.5),(-0.5,0.5),(-0.5,0.5),(-0.5,0.5)]
    lc_path = 'light_curve'
    nwalkers = 32
    nburnin = 100
    nsteps =  1000
    ndim = 5
    wave_bin_size = 1
    # -------------------------------------------------------------------------
    LC = lc_class.LightCurve(lc_path, wave_bin_size)
    LC_dic = LC.LC_dic # dictionary of light curve for each wavelength

    #this part should have MPI so different LCs go on different nodes
    for wavelength_id in LC_dic:
        #below print statement needs to be edited. Correct object attribute??? Units??
        print "LC for wavelength "+str(LC_dic[wavelength_id].new_wave_number)+" um running on node MPINUMBER"
        x = LC_dic[wavelength_id].time # extract the times
        y = LC_dic[wavelength_id].flux / 8.0 # extract the flux & semi-normalize it
        yerr = LC_dic[wavelength_id].ferr # extract the flux error

        #initialize batman model
        transit_pars, model_object, flux0 = init_model(transit_parameters, x)

        # run mcmc beginning at users initial guess without GP
        LC_dic[wavelength_id].obj_mcmc = mcmc.MCMC(x, y, yerr, lnprob_base, ["rp","u1","u2","u3","u4"],
                       [], nwalkers, 1)
        pos = [p0[2:] + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]
        LC_dic[wavelength_id].obj_chain = LC_dic[wavelength_id].obj_mcmc.run(pos, nburnin, nsteps)

        # run mcmc beginning at users initial guess with Matern Kernel GP for now
        LC_dic[wavelength_id].obj_mcmcGP = mcmc.MCMC(x, y, yerr, lnprob_gp, ["a","tau","rp","u1","u2","u3","u4"],
                       [], nwalkers, 1)
        pos = np.array([p0 + 1e-4*np.random.randn(ndim+2) for i in range(nwalkers)])
        LC_dic[wavelength_id].obj_chainGP = LC_dic[wavelength_id].obj_mcmcGP.run(pos, nburnin, nsteps)

        # check out results... plotting is not ready for general use yet :(
        plt.figure(1)
        for k in range(ndim):
            plt.subplot(ndim,1,k+1)
            plt.plot(range((nsteps - nburnin)*nwalkers), LC_dic[wavelength_id].obj_chain[:,k])

        plt.figure(2)
        for k in range(ndim+2):
            plt.subplot(ndim+2,1,k+1)
            plt.plot(range((nsteps - nburnin)*nwalkers), LC_dic[wavelength_id].obj_chainGP[:,k])

        corner.corner(LC_dic[wavelength_id].obj_chain, labels=["rp","u1","u2","u3","u4"], truths=p0[2:])
        corner.corner(LC_dic[wavelength_id].obj_chainGP, labels=["a","tau","rp","u1","u2","u3","u4"], truths=p0)
