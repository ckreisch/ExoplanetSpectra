import numpy as np
import george
import batman
from george import kernels
import pandas as pd
from time import time
import cProfile

import copy_reg
import types

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)    

## @class TransitModel
# Class to estimate the Transit Model with the customized kernel
#
# More details.
class TransitModel(object):
    ## The constructor. Takes the disctionary of the parameters and data to customize the
    # object. In case some values are missed, the default one are used.
    # @param self The object pointer
    # @param **kwargs Accepts the dictionary of data, transit and kernel parameters
    def __init__(self, **kwargs):

        self.batman_default_params = {"t0": 0, "rp": -10., "u": [-1., -1., -1., -1.],
                                      "per": 1., "a": 15., "inc": 87., "ecc": 0.,
                                      "w": 90., "limb_dark": 'nonlinear'}

        self.transit_default_priors = {"rp_prior_lower": -1., "rp_prior_upper": 1.,
                                       "u_prior_lower": -1.,   "u_prior_upper": 1.}

        self.kernel_default_params = {"kernel_a": 1.,
                                      "kernel_gamma": [1., 1., 1., 1.],
                                      "kernel_variance": 1.,
                                      "kernel_type": "Custom"}

        self.kernel_default_priors = {"kernel_a_prior_lower": -5.,       "kernel_a_prior_upper": 5.,
                                      "kernel_gamma_prior_lower": 0.,    "kernel_gamma_prior_upper": 10.,
                                      "kernel_variance_prior_lower": 0., "kernel_variance_prior_upper": 5., }

        self.data_defaults = {"t": np.linspace(0, 0, 1),
                              "y": None,
                              "yerr1": None}
        self.n_errors = 0
        self.err_names = ["yerr1"]
        self.errors_list = []
        self.params = batman.TransitParams()
        self._model = None

        # uncomment for the Python 2 and comment the line after next
        for (param, default) in self.batman_default_params.iteritems():
        #for (param, default) in self.batman_default_params.items():
            setattr(self.params, param, kwargs.get(param, default))

        # setting the attributes of the class other then light curve parameters
        self.set_values(self.transit_default_priors, **kwargs)
        self.set_values(self.kernel_default_params, **kwargs)
        self.set_values(self.kernel_default_priors, **kwargs)
        self.set_values(self.data_defaults, **kwargs)

        # update the limb darkening parameters
        self.read_limb_dark_params(**kwargs)

        # collecting the data about errors that was passed
        self.read_errors_data(**kwargs)

        if len(self.kernel_gamma) != (self.n_errors + 1):
            raise ValueError('For the kernel gamma hyper parameters expected ', self.n_errors + 1,
                             ' values. Instead got ', len(self.kernel_gamma), ' .')

        if self.params.rp == self.batman_default_params["rp"]:
            raise ValueError(" The value for the rp parameter of the transit model was not passed.")

        if self.params.u == self.batman_default_params["u"]:
            raise ValueError(" The value for the u parameters of the transit model was not passed.")

        if self.kernel_variance_prior_lower < 0.:
            raise ValueError(" The prior for kernel variance cannot be negative.")

        self.batman_model = batman.TransitModel(self.params, self.t)
        self.model = self.params

        self.data_dict = dict(zip(self.t, zip(*self.errors_list)))

    ## Set the parameters of the model based on the values provided.
    # In case some values are missed, the default ones will be taken.
    # @param self The object pointer
    # @param dict_of_values Dictionary of the parameters to pass
    def set_values(self, dict_of_values, **kwargs):
        for (param, default) in dict_of_values.iteritems():
            setattr(self, param, kwargs.get(param, default))

    ## Forms a list of the limb darkening parameters from the user input
    # In case some values are missed, the default ones will be taken.
    # @param self The object pointer
    # @param **kwargs Dictionary of the parameters to pass
    def read_limb_dark_params(self, **kwargs):
        u_names = []
        for keyword in kwargs:
            if keyword.startswith("u") and not keyword.startswith("u_"):
                u_names.append(keyword)

        if len(u_names) == 0:

            set_u = self.batman_default_params["u"]
        else:
            u_names.sort()

            set_u = []
            for ux in u_names:
                set_u.append(kwargs.get(ux))

        setattr(self.params, 'u', set_u)

    ## Collects the data about errors that was passed
    # In case some values are missed, the default ones will be taken.
    # @param self The object pointer
    # @param **kwargs Dictionary of the parameters to pass
    def read_errors_data(self, **kwargs):
        err_names = []
        for keyword in kwargs:
            if keyword.startswith("yerr"):
                err_names.append(keyword)

        if len(err_names) == 0:
            # nothing to initialize/update
            return

        else:
            for er_name in err_names:
                setattr(self, er_name, kwargs.get(er_name, None))

                if er_name not in self.err_names:
                    self.err_names.append(er_name)

        self.n_errors = 0
        for name in self.err_names:
            if getattr(self, name) is not None:
                self.n_errors+=1
                self.errors_list.append(getattr(self, name))

        self.data_dict = dict(zip(self.t, zip(*self.errors_list)))

    ## Updates the data for the given parameters
    # @param self The object pointer
    # @param time(=None) Time data
    # @param obs(=None) Observations data
    # @param **kwargs Handles arbitrary number of the errors that was passed
    def update_data(self, time=None, obs=None, **kwargs):

        if time is not None:
            setattr(self, 't', time)

        if obs is not None:
            setattr(self, 'y', obs)

        self.read_errors_data(**kwargs)

        self.updateTransitMode()

    ## Updates the parameters of the model
    # @param self The object pointer
    # @param rp_new New value of the rp parameter
    # @param u_new New list of values for the limb darkening
    def update_transit_params(self, rp_new, u_new):

        u_prev = self.params.u

        if rp_new is None:
            raise ValueError("The None was passed as rp parameter.")

        elif u_new is None:
            raise ValueError("The None was passed as u parameter.")

        elif len(u_new) != len(u_prev):
            raise ValueError('The length of new limb darkening parameter is wrong. Should be ',
                             len(u_prev), ' instead got ', len(u_new),'. The current mode is ', self.params.limb_dark)

        else:
            self.params.rp = rp_new
            self.params.u = u_new
            self.updateTransitMode()

    ## Updates the hyperparameters of the kernel function
    # @param self The object pointer
    # @param a_new New value of the kernel_a
    # @param gamma_new New value of the kernel_gamma
    def update_kernel_params(self, a_new=None, gamma_new=None, variance_new=None):

        if a_new is None:
            setattr(self, "kernel_a", self.kernel_a)
        else:
            setattr(self, "kernel_a", a_new)

        if gamma_new is None:
            setattr(self, "kernel_gamma", self.kernel_gamma)
        elif type(gamma_new) != list:
            raise TypeError("For the gamma parameters list is expected. Instead got ", type(gamma_new))
        elif len(gamma_new) != (self.n_errors + 1):
            raise ValueError("The length of eta is wrong. List of size", (self.n_errors + 1),
                             "is expected.")
        else:
            setattr(self, "kernel_gamma", gamma_new)

        if variance_new is None:
            setattr(self, "kernel_variance", self.kernel_variance)

        else:
            setattr(self, "kernel_variance", variance_new)

    ## Updates the transit model parameters
    # @param self The object pointer
    def updateTransitMode(self):
        self.batman_model = batman.TransitModel(self.params, self.t)
        self.model = self.params
        self.model_initialized = True

    ## Returns the flux values array
    # @param self The object pointer
    # @return Model-generated observation for the given transit parameters
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, params):
        self._model = self.batman_model.light_curve(params)

    ## Mean function for the kernel meaan estimation
    # @param self The object pointer
    # @param t The time data
    def meanfnc(self, t):
        return self.model

    ## Computes the kernel function for the arbitrary sources of errors in the observations
    # @param self The object pointer
    # @param x1 First time coordinate
    # @param x2 Second time coordinate
    # @param p(=None) Kernel auxiliary parameters
    # @return Covariance between two points in time
    def kernelfnc(self, x1, x2, p=None):
        ksi, sig, eta = self.kernel_a, self.kernel_variance, self.kernel_gamma
        s = eta[0]*((x1[0]-x2[0])**2)

        for i in range(self.n_errors):
            s += eta[(i+1)]*((self.data_dict[x1[0]][i]-self.data_dict[x2[0]][i])**2)

        val = ksi * np.exp(-s) + (x1 == x2) * sig

        return val

    ## Computes the log likelihood from gaussian process
    # @param self The object pointer
    # @return Log likelihood of a set of observations under the Gaussian process model.
    def lnlike_gp(self):

        if (self.t is None) | (self.y is None):
            raise ValueError("Data is not properly initialized. Reveived Nones.")

        elif len(self.t) == 1:
            raise ValueError("Time data is not properly initialized. Expected array of size greater then 1.")

        else:

            t, y = self.t, self.y

            if self.kernel_type == "Standard":
                kernel = 1.*kernels.ExpSquaredKernel(5.) + kernels.WhiteKernel(2.)
                gp = george.GP(kernel, mean=self.meanfnc)
                gp.compute(t, self.yerr1)
                return gp.lnlikelihood(y - self.model)

            else:
                kernel = kernels.PythonKernel(self.kernelfnc)
                gp = george.GP(kernel, mean=self.meanfnc)
                gp.compute(t)
                return gp.lnlikelihood(y - self.model)

    ## Checks if the batman parameters are within the predefined prior ranges
    # @param self The object pointer
    # @return Returns 0 in case transit parameters whithin the prior range and -inf otherwise
    def lnprior_base(self):

        if not self.rp_prior_lower < self.params.rp < self.rp_prior_upper:
            return -np.inf

        for el in self.params.u:
            if not self.u_prior_lower < el < self.u_prior_upper:
                return -np.inf

        return 0.0

    ## Checks if the kernel parameters are within the predefined prior ranges
    # @param self The object pointer
    # @return Returns -inf in case parameters out of the range and 0.0 if within the prior range
    def lnprior_gp(self):

        if not self.kernel_a_prior_lower < self.kernel_a < self.kernel_a_prior_upper:
            return -np.inf

        for el in self.kernel_gamma:
            if not self.kernel_gamma_prior_lower < el < self.kernel_gamma_prior_upper:
                return -np.inf

        if not self.kernel_variance_prior_lower <= self.kernel_variance < self.kernel_variance_prior_upper:
            return -np.inf

        return self.lnprior_base()

    ## Computes the log probability of the parameters for the given data
    # @param self The object pointer
    # @return Log probability of the parameters
    def lnprob_gp(self):

        lp = self.lnprior_gp()

        if not np.isfinite(lp):
            return -np.inf

        self.lnprob = lp + self.lnlike_gp()

        return self.lnprob

    ## For a given set of parameters get predicted y values at t, and
    # separate this into the transit signal component and the noise component
    # @param self The object pointer
    # @param p Parameters of the transit
    # @param t Time data
    # @param y Observations data
    # @param yerr Errors data
    # @return Predicted observations
    def sample_conditional(self, p, t, y, yerr):
        if self.params.limb_dark == 'quadratic':
            rp_new, u0, u1, kernel_a, kernel_sig2 = p[:5]
            u_new = [u0, u1]
            kernel_gamma = p[5:].tolist()

        if self.params.limb_dark == 'nonlinear':
            rp_new, u0, u1, u2, u3, kernel_a, kernel_sig2 = p[:7]
            u_new = [u0, u1, u2, u3]
            kernel_gamma = p[7:].tolist()

        self.update_transit_params(rp_new=rp_new, u_new=u_new)
        self.update_kernel_params(a_new=kernel_a, gamma_new=kernel_gamma, variance_new=kernel_sig2)

        kernel = kernels.PythonKernel(self.kernelfnc)
        gp = george.GP(kernel, mean=self.meanfnc)
        gp.compute(t, yerr)

        sample = gp.sample_conditional(y - self.model,t)  +  self.model

        return sample


    ## MCMC API for the Transit Model object
    # @param self The object pointer
    # @param p Parameters of the transit
    # @param t Time data
    # @param y Observations data
    # @param yerr Errors data
    # @return Log probability of the chosen parameters
    def lnprob_mcmc(self, p, t, y, yerr):
        if self.params.limb_dark == 'quadratic':
            rp_new, u0, u1, kernel_a, kernel_sig2 = p[:5]
            u_new = [u0, u1]
            kernel_gamma = p[5:].tolist()

        if self.params.limb_dark == 'nonlinear':
            rp_new, u0, u1, u2, u3, kernel_a, kernel_sig2 = p[:7]
            u_new = [u0, u1, u2, u3]
            kernel_gamma = p[7:].tolist()

        self.update_transit_params(rp_new=rp_new, u_new=u_new)
        self.update_kernel_params(a_new=kernel_a, gamma_new=kernel_gamma, variance_new=kernel_sig2)

        return self.lnprob_gp()
