
import numpy as np
import george
import batman
from george import kernels

class TransitModel(object):

    def __init__(self, **kwargs):

        self.batman_default_params = {"t0": 0, "rp": -1000., "u": [-100., -100., -100., -100.],
                                      "per": 1., "a": 15., "inc": 87., "ecc": 0.,
                                      "w": 90., "limb_dark": 'nonlinear'}

        self.transit_default_priors = {"rp_prior_lower": -1., "rp_prior_upper": 1.,
                                       "u_prior_lower": -1.,   "u_prior_upper": 1.}

        self.kernel_default_params = {"kernel_a": 1.,
                                      "kernel_gamma": 5.,
                                      "kernel_variance": 1.}

        self.kernel_default_priors = {"kernel_a_prior_lower": -5.,       "kernel_a_prior_upper": 5.,
                                      "kernel_gamma_prior_lower": 0.,    "kernel_gamma_prior_upper": 10.,
                                      "kernel_variance_prior_lower": 0., "kernel_variance_prior_upper": 5., }

        self.data_defaults = {"t": np.linspace(0,0,1),
                              "y": None,
                              "yerr": None}

        self.params = batman.TransitParams()

        # uncomment for the Python 2 and comment the line after next
        #for (param, default) in batman_default_params.iteritems():
        for (param, default) in self.batman_default_params.items():
            setattr(self.params, param, kwargs.get(param, default))

        # update the limb darkening parameters
        self.read_limb_dark_params(**kwargs)

        # setting the attributes of the class other then light curve parameters
        self.set_values(self.transit_default_priors, **kwargs)
        self.set_values(self.kernel_default_params, **kwargs)
        self.set_values(self.kernel_default_priors, **kwargs)
        self.set_values(self.data_defaults, **kwargs)

        if self.params.rp == self.batman_default_params["rp"]:
            raise ValueError(" The value for the rp parameter of the transit model was not passed.")

        if self.params.u == self.batman_default_params["u"]:
            raise ValueError(" The value for the u parameters of the transit model was not passed.")

        if self.kernel_variance_prior_lower < 0.:
            raise ValueError(" The prior for kernel variance cannot be negative.")

        self.batman_model = batman.TransitModel(self.params, self.t)

    def set_values(self, dict_of_values, **kwargs):
        """Sets the attributes. If value is not provided the default value is set"""

        # uncomment for the Python 2 and comment the line after next
        # for (param, default) in dict_of_values.iteritems():
        for (param, default) in dict_of_values.items():
            setattr(self, param, kwargs.get(param, default))

    def read_limb_dark_params(self, **kwargs):
        """Forms a list of the limb darkening parameters from the user input"""
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

    def update_data(self, time=None, obs=None, errors=None):
        """ Updates the data for the given parameters """

        if time is not None:
            setattr(self, 't', time)

        if obs is not None:
            setattr(self, 'y', obs)

        if errors is not None:
            setattr(self, 'yerr', errors)

        self.updateTransitMode()

    def update_transit_params(self, rp_new, u_new):
        """
        Update the parameters of the model
        :param rp_new: new value of the rp parameter
        :param u_new: new list of values for the limb darkening
        """
        u_prev = self.params.u

        if len(u_new) != len(u_prev):
            raise ValueError("The length of new limb darkening parameter is wrong. Should be ",
                             len(u_prev), " instead got ", len(u_new),". The current mode is ", self.params.limb_dark)
        elif rp_new is None:
            raise ValueError("The None was passed as rp parameter.")

        elif u_new is None:
            raise ValueError("The None was passed as u parameter.")

        else:
            self.params.rp = rp_new
            self.params.u = u_new
            self.updateTransitMode()

    def update_kernel_params(self, a_new, gamma_new, variance_new):
        """
        Updates the hyperparameters of the kernel function
        :param a_new: new value of the kernel_a
        :param gamma_new: new value of the kernel_gamma
        """

        if a_new is not None:
            raise ValueError("The None was passed as kernel_a parameter.")
        elif gamma_new is None:
            raise ValueError("The None was passed as kernel_gamma parameter.")
        elif variance_new is None:
             raise ValueError("The None was passed as kernel_variance parameter.")
        else:
            self.kernel_a = a_new
            self.kernel_gamma = gamma_new
            self.kernel_variance = variance_new

    def updateTransitMode(self):
        """ Updates the transit model parameters """
        self.batman_model = batman.TransitModel(self.params, self.t)
        self.model_initialized = True

    def model(self):
        """ Returns the flux values array """
        return self.batman_model.light_curve(self.params)

    def meanfnc(self, t):
        """ Mean function for the kernel estimation"""
        return self.model()

    def lnlike_gp(self):
        """ Computes the log likelihood from gaussian process """

        if (self.t is None) | (self.y is None) | (self.yerr is None):
            raise ValueError("Data is not ptoperly initialized.")
            return
        else:
            t, yerr, y = self.t, self.yerr, self.y

            gamma = self.kernel_gamma * 2
            kernel = self.kernel_a * kernels.ExpSquaredKernel(gamma) + kernels.WhiteKernel(self.kernel_variance)

            gp = george.GP(kernel, mean=self.meanfnc)

            gp.compute(t, yerr)

            return gp.lnlikelihood(y - self.model())

    def lnprior_base(self):
        """ Checks if the batman params are within the predefined prior ranges """

        if not self.rp_prior_lower < self.params.rp < self.rp_prior_upper:
            return -np.inf

        for el in self.params.u:

            if not self.u_prior_lower < el < self.u_prior_upper:
                return -np.inf

        return 0.0

    def lnprior_gp(self):
        """Checks if the kernel params are within the predefined prior ranges"""

        if not self.kernel_a_prior_lower < self.kernel_a < self.kernel_a_prior_upper:
            return -np.inf

        if not self.kernel_gamma_prior_lower < self.kernel_gamma < self.kernel_gamma_prior_upper:
            return -np.inf

        if not self.kernel_variance_prior_lower < self.kernel_variance < self.kernel_variance_prior_upper:
            return -np.inf

        return self.lnprior_base()

    def lnprob_gp(self):
        """ Computes the log prob of the parameters for the given data """

        lp = self.lnprior_gp()

        if not np.isfinite(lp):
            return -np.inf

        self.lnprob = lp + self.lnlike_gp()

        return self.lnprob


