import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import batman

## Initializes a Batman TransitParams object and Batman TransitModel object with quadratic limb-darkening prescription
# @param t_params A list of transit parameters in order: t0, per, rp, a, inc, ecc, w, u0, u1
# @param times An array of times to sample the flux of the Batman TransitModel at
# @returns TransitParams object, TransitModel object, flux at specified times 
def init_model(t_params, times):
    t0,per,rp,a,inc,ecc,w,u0,u1 = t_params    
    p = batman.TransitParams()  #object to store transit parameters 
    p.t0 = t0                   #time of inferior conjunction 
    p.per = per                 #orbital period 
    p.rp = rp                   #planet radius (in units of stellar radii) 
    p.a = a                     #semi-major axis (in units of stellar radii) 
    p.inc = inc                 #orbital inclination (in degrees) 
    p.ecc = ecc                 #eccentricity 
    p.w = w                     #longitude of periastron (in degrees) 
    p.limb_dark = "quadratic"   #limb darkening model 
    p.u = [u0, u1]              #limb darkening coefficients 
    m = batman.TransitModel(p, times)  #initializes model 
    flux = m.light_curve(p)        #calculates white light curve  

    return p, m, flux

## Update TransitModel object for wavlength channels radius and limb-darkening coefficents, 
# then compute the updated flux measurements
# @param wl_params List of wavelength-specific transit parameters in order radius: rp, limbdarkening-coefficients: u0 and u1
# @param m batman TransitModel object
# @param p batman TransitParameter object
# @returns An array of flux measurements
def wl_channel_flux(wl_params, m, p):
    rp,u0,u1 = wl_params    
    p.rp = rp            #planet radius (in units of stellar radii) 
    p.u = [u0, u1]       #limb darkening coefficients  
    flux = m.light_curve(p)      #calculates light curve 

    return flux

## Generates white (random) noise
# @param level The scaling of white noise that is desired, higher numbers make noisier light curves
# @param N The size of the white noise array needed
# @returns An array of length N which can be added to signal to give it white noise
def white_noise(level, N):

    return level*np.random.rand(N)

## Generates semi-reasonable values of four auxiliary measurements: airmass, position, fwhm, skynoise
# @param level The scale factor for the slopes, relates to the total amount of red noise that will be incorporated 
# @param N number of time steps to generate auxiliary measurments for
# @returns Length 4 array containing a slope to use in linear correlation between signal and each auxiliary measure
# @returns 4 x N array containing the 4 auxiliary measurements for each time step of light curve
def generate_a_params(level, N):
    slopes = np.zeros(4) + level*np.random.randn(4)
    # approximate change in  airmass over course of observation with a quadratic
    airmass = N*10.**(-5.)*np.arange(-0.1*N/4., 0.3*N/4.,0.1)**2. + 1.6  
    # approximate change in position on detector over course of observation
    # with cube root 
    pos = np.concatenate((-1.*np.arange(0., N/2.,1.)[::-1]**(1./3.),  
                         np.arange(1., N/2.+1,1.)**(1./3.)))*0.05 + 10.0      

    # approximate full-width-half-maximum size of psf with sine wave        
    fwhm = np.sin(6.*np.arange(N)/(N*np.pi))*2.25  

    # random skynoise levels but also related to fhwm
    skynoise = fwhm + np.random.randn(N)*0.00001    

    return slopes, np.array([airmass, pos, skynoise, fwhm])

## Generates red (correlated) noise as super position of linear correlations to auxiliary measurements
# @param a_params The 4 x N array of auxiliary measures
# @param slopes The randomly generated slopes to use in linear correlation
# @returns Length N array, the normalized red noise array to be multiplied by the light curve
def red_noise(a_params, slopes):	
    red_superposition = np.sum((a_params.T*slopes).T, axis=0) + 1.
    norm = np.median(red_superposition)

    return red_superposition/norm

## Writes a light curve text file in form needed for exospec
# @param times The times of light curve
# @param flux The flux levels of light curve
# @param ferr The error on flux measure
# @param a_params The four auxiliary measurements for each time
# @param fname The name of the file to save light curve to
# @param slopes The slopes used in correlating the signal to the auxiliary measures 
# @param w_level The level of white noise (a scale factor)
# @param r_level The level of red noise (a scale factor)
# @param wl_params The radius and limb darkening coefficients for this wavelength
# @returnval 0 if successful 
# @returnval other if not successful
def write_lc(fname, times, flux, ferr, a_params, slopes, w_level, r_level, wl_params):
    ofile = open(fname,"w")
    # add header with more info for testing purposes
    ofile.write("# white scalel: %f, red scale: %f, fwhm corr. coeff.: %f, skynoise corr. coeff.: %f, position corr. coeff.: %f, airmass corr. coeff.: %f\n" % (w_level,r_level,slopes[3],slopes[2],slopes[1],slopes[0]))
    ofile.write("# transit parameters: rp = %f, u0 = %f, u1 = %f\n" % (wl_params[0],wl_params[1],wl_params[2]))
    ofile.write("# time (phase), flux, ferr, fwhm, skynoise, position, airmass\n")
    for k in range(len(times)):
        ofile.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (times[k], flux[k], ferr[k], a_params[3][k], a_params[2][k], a_params[1][k], a_params[0][k]))
    ofile.close()

    return 0

## Writes a summary of parameters used to generate the lightcurves to a textfile, useful for benchmark testing
# @param fname The file name to save to
# @param truth List of the base transit parameters, and star/planet spectral information that synthetic measures are based on
# @param slopes Array of the base slopes used to correlate the signal to the auxiliary measures 
# @param w_level Level of white noise
# @param r_level Level of red noise
# @retval 0 if successful
def write_expected_vals(fname, truth, slopes, w_level, r_level):
    t_params, wl, radii, ldark, starspec, w_scale, r_scale = truth
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
        ofile.write("%f\t%f\t%f\t%f\t%f\t%f\n" % (wl[k],radii[k],ldark[k][0],ldark[k][0],w_scale[k],r_scale[k]))

    return 0

## Generates light curves for a set of wavelengths and the corresponding radii/limb-darkening coefficients. 
# Also saves textfile with expected values and a plot of the generated lightcurves.
# @param dname Name of the directory where files ought to be stored
# @param truth List of the base transit parameters, and star/planet spectral information that synthetic measures are based on
# @param w_level Level of white noise
# @param r_level Level of red noise
# @param N number of time steps to generate auxiliary measurments for
# @param phase_range A tuple of the lower and upper phase range light curve will span. Note transit occurs at t=0
# @param fileroot A short prefix that will be appended to each file
# @retval 0 if successful 
def gen_obs_set(dname, truth, w_level, r_level, N=300, 
                phase_range=(-0.025,0.025), fileroot="synth"):

    t_params, wl, radii, ldark, starspec, w_scale, r_scale = truth

    # initialize model
    t0 = t_params[0]
    exptime = (phase_range[1]-phase_range[0])/N
    t = np.arange(t0 - exptime*N/2., t0 + exptime*N/2., exptime) 
    p, model, signal_0 = init_model(t_params, t)

    # generate auxiliary parameters
    slopes, a_params = generate_a_params(r_level, N)

    plt.figure(1)
    colors = ['m','c','b','r','g','k']

    if not os.path.exists(dname+"/light_curves"):
        os.makedirs(dname+"/light_curves")

    # for each radii: 
    for k in range(len(radii)):   
        # pure transit signal
        wl_params = [radii[k], ldark[k][0], ldark[k][1]]
        signal = wl_channel_flux(wl_params, model, p)
        # white noise to be added
        ferr =  np.zeros(N) + np.std(white_noise(w_level, N)*w_scale[k])  
        if np.mean(ferr)==0:
            ferr = ferr + 0.0000001 
        # scale the fwhm and sky noise correlated rednoise for that wl
        fwhm, skynoise = r_scale[k]*a_params[3], r_scale[k]*a_params[2]
        wl_a_params = np.concatenate((a_params[:2],np.array([fwhm,skynoise])))
        # put  it all together
        f = signal*red_noise(wl_a_params, slopes) + white_noise(w_level, N)*w_scale[k]*np.random.randn(N)
        # write to a file
        fname = dname+"/light_curves/"+fileroot+"_lc_"+str(wl[k])+".txt"
        write_lc(fname, t, f, ferr, wl_a_params,
                 slopes*r_scale[k], w_level, r_level, wl_params)
        # plot
        plt.errorbar(t,f,yerr=ferr)
        plt.plot(t,f,label=str(wl[k]),color=colors[k])
        plt.plot(t,signal,linestyle="--",color=colors[k])        

    plt.legend(loc="best")
    plt.xlabel("phase")
    plt.ylabel("normalized flux")

    #save things
    plt.savefig(dname+"/"+"visual.png")
    fname = dname+"/"+fileroot+"_expected_values.txt"   
    write_expected_vals(fname, truth, slopes, w_level, r_level)

    return 0

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # All data generated will take on the following
    # "true" parameters, with noise added on top
    # Currently hard-coded in, could be read from file instead
    # transit parameters in order: t0, per, rp, a, inc, ecc, w, u0, u1
    # see def init_model() for physical meanings
    t_params = [0.0, 1.0, 0.1, 15.0, 87.0, 0.0, 90.0, 0.5, 0.1]
    # central wavelengths in microns for each channel
    wl = [500, 650, 800, 950, 1100, 1350]  
    # fractional radius of planet       
    radii = [0.05, 0.08, 0.1, 0.12, 0.15, 0.09]   
    # limb darkening coefficients for the star
    ldark = [[0.45, 0.1],[0.55, 0.1],[0.45, 0.11],[0.35,0.16],[0.5,0.1],[0.3,0.2]]    
    # flux level coming from star normalized to channel with maximum flux (to scale white noise)
    starspec = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # note by all being 1.0 this is currently not affecting anything 
    # fwhm of psf for that wavelength normalized to channel with maximum psf size (to scale red noise)
    fwhm = [np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), 
            np.sqrt(1./2.)]      # note by all being sqrt(1./2.) this is currently not affecting anything
    # sky flux level normalized to maximum sky flux level (to scale red noise)
    skyspec = [np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), np.sqrt(1./2.), 
               np.sqrt(1./2.)] 
    # convert starspec, fwhm, skyspec  to w_scale, r_scale
    w_scale = [1./starspec[k] for k in range(len(starspec))] # brighter channels will have lower white noise levels
    r_scale = [np.sqrt(fwhm[k]**2.+skyspec[k]**2.) for k in range(len(fwhm))]
    # put all together into a list for easy passing to functions
    truth = [t_params, wl, radii, ldark, starspec, w_scale, r_scale]

    # -------------------------------------------------------------------------
    # interpret command line
    if len(sys.argv)!=5:

        raise ValueError("Run as python gen_syn_data.py <output_directory> " + \
                "<N data in lightcurve> <white noise level> <red noise level>")

    output_dir, N, w_level, r_level = sys.argv[1:]

    try:

        N = int(N)
        w_level = float(w_level)
        r_level = float(r_level)

    except ValueError:

        print "command line arguments need to be convertable to string" + \
              " integer float float"
        raise

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # generate one set of data and look at it:
    gen_obs_set(output_dir, truth, w_level, r_level, N=N)
    plt.show()


