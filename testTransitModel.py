import unittest
import numpy as np
import george
from george import kernels
from TransitModel import TransitModel


class TestFunctions(unittest.TestCase):

    def setUp(self):
        # create testing params into the dictionary

        self.params = {'t0': 1, 'a': 15.0, 'ndim': 5, 'p0': [0.1, 0.1, 0.1, 0.5, 0.1, 0.1, -0.1], 'u3': -0.1,
                       'ecc': 0.0, 'mpi_flag': ['True'], 'nburnin': 100, 'nthreads': 4,
                       'priors': [(0, 1), (-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5)],
                       'u1': 0.1, 'u0': 0.5, 'per': 1.0, 'u2': 0.1, 'lc_path': ['light_curve'],
                       't0': 0.0, 'w': 90.0, 'rp': 0.1, 'nwalkers': 32, 'nsteps': 1000,
                       'wave_bin_size': 1, 'inc': 87.0,
                       "kernel_a": 2., "kernel_gamma": 2., "kernel_variance": 2.,
                       "rp_prior_lower": -1., "rp_prior_upper": 1., "u_prior_lower": -1.,   "u_prior_upper": 1.,
                       "kernel_a_prior_lower": -5., "kernel_a_prior_upper": 5.,
                       "kernel_gamma_prior_lower": 0., "kernel_gamma_prior_upper": 10.,
                       "kernel_variance_prior_lower": 0., "kernel_variance_prior_upper": 5.}

        self.params['t'], self.params['y'], self.params['yerr'] = self.generateDataHelper(N=20)

        self.test_transit = TransitModel(**self.params)

        #print( self.test_transit.lnprob_gp() )

    def modelHelper(self,params, t):
        amp, loc, sig2 = params
        return amp * np.exp(-0.5 * (t - loc) ** 2 / sig2)

    def generateDataHelper(self, N, rng=(-5, 5)):
        """
        Generates an artificial dataset with predefined parameters

        :param N: number of the datapoints
        :param rng: over what timerange to generate the data
        :return: t, y, yerr - time, observations and the errors in the observations
         """
        true_params = [-1.0, 0.1, 0.4]
        gp = george.GP(0.1 * kernels.ExpSquaredKernel(3.3))
        t = rng[0] + np.diff(rng) * np.sort(np.random.rand(N))
        y = gp.sample(t)
        y += self.modelHelper(true_params, t)
        yerr = 0.05 + 0.05 * np.random.rand(N)
        y += yerr * np.random.randn(N)

        return t, y, yerr
    #
    # def testCustomInit(self):
    #     """ Testing the customized init of the model"""
    #     rp0 = 0.8
    #     u0 = [0.5, 0.1, 0.1, -0.1]
    #
    #     # setts default parameters
    #     self.test_transit = TransitModel(rp0 = rp0, u0 = u0 )
    #
    #     self.assertTrue(self.test_transit.params.a == 15.)
    #     self.assertTrue(self.test_transit.u_prior_u == 1.)
    #     self.assertTrue(self.test_transit.rp_prior_d == 0.)
    #     self.assertTrue(self.test_transit.params.ecc == 0.)
    #
    #     # reinitialize some of the parameters and checks if they have the correct values
    #     new_params = self.params
    #     new_params['a'] = 1.; new_params['ecc'] = 3.; new_params['rp_prior_d'] = -2.
    #     new_params['u_prior_u'] = 3;
    #     self.test_transit = TransitModel(rp0, u0, **new_params)
    #
    #     self.assertTrue(self.test_transit.params.a == 1.)
    #     self.assertTrue(self.test_transit.u_prior_u == 3.)
    #     self.assertTrue(self.test_transit.rp_prior_d == -2.)
    #     self.assertTrue(self.test_transit.params.ecc == 3.)
    #
    #     pass

    # def test_data_update(self):
    #     """Testing partial and full data update for the model"""
    #     # should be empty at init
    #     self.assertTrue(self.test_transit.y is None)
    #     self.assertTrue(self.test_transit.yerr is None)
    #
    #     t_prev = self.test_transit.t
    #     t, y, yerr = self.generateDataHelper(N=20)
    #
    #     # updates the observations only and checks if other have not changed
    #     self.test_transit.update_data(obs=y)
    #
    #     self.assertTrue(np.array_equal(self.test_transit.t, t_prev))
    #     self.assertTrue(self.test_transit.y is not None)
    #     self.assertTrue(self.test_transit.yerr is None)
    #
    #     # updates the rest and checks if other have the correct values
    #     self.test_transit.update_data(time=t, errors=yerr)
    #
    #     self.assertTrue(np.array_equal(self.test_transit.t, t))
    #     self.assertTrue(np.array_equal(self.test_transit.y, y))
    #     self.assertTrue(np.array_equal(self.test_transit.yerr, yerr))
    #
    #     pass

    # def test_transit_params_update(self):
    #
    #
    #     pass
    #
    # def test_kernel_params_update(self):
    #     pass
    #
    # def test_lnprior_base(self):
    #     pass
    #
    # def test_lnprior_gp(self):
    #     pass
    #
    def test_lnprob_gp(self):
         pass


if __name__ == '__main__':
    unittest.main()