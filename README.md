Jenkins current build status: [![Build Status](https://jenkins.princeton.edu/buildStatus/icon?job=ckreisch/ExoplanetSpectra)](https://jenkins.princeton.edu/buildStatus/icon?job=ckreisch/ExoplanetSpectra)

# ExoplanetSpectra
Design project to extract exoplanet transmission spectra from multi-wavelength light curves.

#Classes we plan to use:
 - Noise (with derived classes WhiteNoise, RedNoise)
 - LightCurve (reading in and using/plotting light curve datafile)
 - Model (use batman to get model curves for transit model parameters)
 - Decorrelator (remove correlated noise) - maybe derived classes for atmosphere and instrument
 - MCFitter (do fit using batman and emcee)

#Main steps for our project:

1. Generate simulated data:
    - light curves for a transit at different frequencies from batman (existing code)
    - noise (white noise, red correlated noise derived classes)
    * inputs: noise amplitude, correlated noise parameters
    * outputs: datafile with noisy intensity vs time for a variety of different wavelengths
    * use classes Noise and Model (to generate theoretical light curve and add noise)

2. Decorrelate:
    - try to fit and remove correlations with observed parameters
    - possibly deal with atmosphere and telescope in separate ways
    * inputs: noisy light curves datafile from step 1 (or real data), observed parameters file (things that might be causing correlated noise, eg psf shape and width, detector temperature, pointing etc)
    * outputs: produce light curve that ideally only has white noise and very small red noise residuals left
    * uses classes Decorrelator and LightCurve

3. Fit:
    - use emcee and batman to fit transit parameters (depth, limb darkening parameters, central time)
    * inputs: decorrelated light curves
    * outputs: best fit transit parameters and uncertainties for each wavelength
    * uses classes MCFitter, Model and LightCurve

4. Visualize output
    - effective size vs wavelength (due to atmospheric effects being wavelength dependent)

#Functionality to add later once everything is working:
Binning:
    - allow user to specify binning in wavelength and time to reduce error bars on fitted parameters
    - do once we have everything else working
    - this would probably just produce different datafiles with binned lightcurves and use the same code as above

Additional methods for treating noise eg Gaussian processes

User friendliness:
    - make parts 2 and 3 easy to use for people wanting to fit their light curves

#Background
A little background on transmission spectroscopy of exoplanets:

A transit occurs when a planet passes in front of its host star. This leaves a tell-tale dip in the light curve of the star as the planet blocks out part of the star's surface/light. The depth of that dip is proportional to the ratio of the area of planet to the area of the star. (see attached image showing cartoon light curve as planet transits star)

If you consider a planet with a significant atmosphere, then the planet's apparent radius will actually vary with wavelength of light. At wavelengths where the atmosphere is highly absorptive you have a larger radius and at wavelengths where the atmosphere is not absorbing you have a smaller radius. A transmission spectrum is simply a measure of the planet's apparent radius as a function of wavelength. This can allow you to back out what molecules are present in the planets atmosphere.  A nice video showing change of planet radius with wavelength can be found at: http://www.exoclimes.com/topics/transmission-spectroscopy/

These people have some pretty videos as well: https://svs.gsfc.nasa.gov/11428

I have some multi-wavelength data from a ground-based transit of an exoplanet which I have been wrestling with to get nice light curves. Our package would be a tool for the next step of actually fitting light curves to the data. The motivation to do it in python is really just because that is a popular language among the astronomical community. We could potentially publish the tool for others to apply to their own projects.

There are already some very nice python packages available that will do most of the hard work:
generates transit light curves given parameters of your system: http://astro.uchicago.edu/~kreidberg/batman/
run MCMC chains: http://dan.iel.fm/emcee/current/
implement gaussian processes to model correlated noise: http://dan.iel.fm/george/current/

We could take these tools and piece them together with a nice interface for the user.

I'm imagining the project will entail a few parts:

1) generate some synthetic "data"  (this can be done with the batman python package, the creative part will be adding in noise that mimics annoyances of atmosphere/ground-based observing)

2) come up with convenient way for user to bin their data both temporally and by wavelength

3) allow user to fit different parameters as they desire (e.g. all parameters for white light curve, or just planet radius and limb-darkening coefficients for different wavelength bins)

4) give user different options for modeling noise (this will be most work perhaps, there are 2 or 3 different ways I have seen people treat noise that seem worth including)

5) make nice plots: characterize the MCMC runs, light curve data overlaid with best fit light curve, transmission spectrum with errors
