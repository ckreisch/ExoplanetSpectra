
import numpy as np
import george
import batman
from george import kernels
from itertools import chain


class TransitModel(object):

    def __init__(self, **kwargs):

        # Default values

        # u - pack into list in init

        self.batman_default_params = {"rp": -1000., "u": [-1., -1., -1., -1.], "per": 1., "a": 15.,
                                      "inc": 87., "ecc": 0., "w": 90., "limb_dark": 'nonlinear'}

        self.transit_default_priors = {"rp_prior_d": -1., "rp_prior_u": 1.,
                                       "u_prior_d": -1., "u_prior_u": 1.}

        self.kernel_default_params = {"kernel_a": 1., "kernel_tau": 5., "kernel_sig2": 1.}

        self.kernel_default_priors = {"a_prior_d": -5., "a_prior_u": 5.,
                                      "tau_prior_d": -10., "tau_prior_u": 10.,
                                      "sig2_prior_d": 0., "sig2_prior_u": 5., }

        self.data_defaults = {"t": np.linspace(0,0,1), "y": None, "yerr": None}

        self.params = batman.TransitParams()

        self.readLimbDarkParams(**kwargs)

        self.readPriors(**kwargs)

        #for (param, default) in batman_default_params.iteritems():
        for (param, default) in self.batman_default_params.items():
            setattr(self.params, param, kwargs.get(param, default))

        self.setValues(self.transit_default_priors, **kwargs)
        self.setValues(self.kernel_default_params, **kwargs)
        self.setValues(self.kernel_default_priors, **kwargs)
        self.setValues(self.data_defaults, **kwargs)

    def setValues(self, dict_of_values, **kwargs):
        #for (param, default) in dict_of_values.iteritems():
        for (param, default) in dict_of_values.items():
            setattr(self, param, kwargs.get(param, default))

    def readPriors(self, **kwargs):
        if 'priors' in kwargs:
            vals = kwargs.get('priors')
            print(vals)

    def readLimbDarkParams(self, **kwargs):

        u_names = []
        for keyword in kwargs:
            if keyword.startswith("u"):
                u_names.append(keyword)

        if len(u_names) == 0:
            return self.batman_default_params["u"]

        u_names.sort()

        u = []
        for ux in u_names:
            u.append(kwargs.get(ux))

        u = list(chain(*u))

        return u



    def update_data(self, time=None, obs=None, errors=None):

        """
        Update the data for the given parameters

        :param time:
        :param obs:
        :param errors:
        :return:

        """

        if time is not None:
            self.t = time

        if obs is not None:
            self.y = obs

        if errors is not None:
            self.yerr = errors

        self.updateTransitMode()

    def update_transit_params(self, rp_new, u_new):
        '''Update the parameters of the model'''

        #TODO: check the length of the parameters
        self.params.rp = rp_new
        self.params.u = u_new
        self.updateTransitMode()

    def update_kernel_params(self, a_new, tau_new):
        '''Update the parameters of the model'''
        self.kernel_a = a_new
        self.kernel_tau = tau_new

    def updateTransitMode(self):
        self.batman_model = batman.TransitModel(self.params, self.t)
        self.model_initialized = True

    def model(self):
        '''Returns the flux values array'''
        return self.batman_model.light_curve(self.params)

    def meanfnc(self, t):
        return self.model()

    def lnlike_gp(self):

        a = 1.      # Hyperparam 1
        gamma = 5.  # Hyperparam 2
        sigma = 1.  # variance

        t, yerr, y = self.t, self.yerr, self.y
        kernel = a * kernels.ExpSquaredKernel(2*gamma) + kernels.WhiteKernel(sigma)  # 2*gamma since in the expsqrkernel
        # it is divided
        gp = george.GP(kernel, mean=self.meanfnc)

        gp.compute(t, yerr)

        return gp.lnlikelihood(y - self.model())

    #def lnprior_base(self, rp0, u0, sig20 = 0):
    def lnprior_base(self ):

        """ Checks if the the points are within the predefined prior ranges """

        #TODO: what is sig2 in Batman
        #rp, u, sig2 = rp0, u0, sig20

        if not self.rp_prior_d < self.rp0 < self.rp_prior_u:
            return -np.inf

        # TODO: for EACH u

        for el in self.u0:

            if not self.u_prior_d < el < self.u_prior_u:
                return -np.inf

        #if not 0 < sig2 < 3.0:
        #    return -np.inf

        return 0.0

    def lnprior_gp(self, p0=[0, 0]):

        """A list of the initial positions of the walkers in the
        parameter space. It should have the shape ``(nwalkers, dim)``
        Checks if the the points are within the predefined prior ranges"""

        p = np.array(p0)

        lna, lntau = p

        # TODO: tuning of the kernel parameters??
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


