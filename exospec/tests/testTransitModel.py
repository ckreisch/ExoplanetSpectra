#!/Users/Paulina/anaconda/lib/python3.5

import unittest
import numpy as np
import george
from george import kernels
import os
import sys
import inspect
dir_current = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_up = os.path.dirname(dir_current)
sys.path.append(dir_up)

from exospec.TransitModel import TransitModel
import time

class TestFunctions(unittest.TestCase):

    # TODO: Handling the empty error array

    def setUp(self):
        """ Initializing the testing environment """

        self.params = {'t0': 1, 'a': 15.0, 'ndim': 5, 'p0': [0.1, 0.1, 0.1, 0.5, 0.1, 0.1, -0.1], 'u3': -0.1,
                       'ecc': 0.0, 'mpi_flag': ['True'], 'nburnin': 100, 'nthreads': 4,
                       'priors': [(0, 1), (-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5)],
                       'u1': 0.1, 'u0': 0.5, 'per': 1.0, 'u2': 0.1, 'lc_path': ['light_curve'],
                       't0': 0.0, 'w': 90.0, 'rp': 0.1, 'nwalkers': 32, 'nsteps': 1000,
                       'wave_bin_size': 1, 'inc': 87.0,
                       "kernel_a": 2., "kernel_variance": 2.,
                       "rp_prior_lower": -1., "rp_prior_upper": 1., "u_prior_lower": -1.,   "u_prior_upper": 1.,
                       "kernel_a_prior_lower": -5., "kernel_a_prior_upper": 5.,
                       "kernel_gamma_prior_lower": 0., "kernel_gamma_prior_upper": 10.,
                       "kernel_variance_prior_lower": 0., "kernel_variance_prior_upper": 5.,
                       "kernel_gamma": [2.]}


        self.test_transit = TransitModel(**self.params)
        #
        # t, y, yerr1, yerr2, yerr3 = self.generateDataHelper(N=20)
        # errors = {'yerr1': yerr1, 'yerr2': yerr2, 'yerr3': yerr3}


        #t, y, yerr1, yerr2, _= self.generateDataHelper(N=50)
        #errors = {'yerr1': yerr1 , 'yerr2': yerr2 }
        #self.test_transit.update_data(time=t, obs = y, **errors)
        #self.test_transit.update_kernel_params(gamma_new=[2.,2., 2.])


        #s = time.time()
        #x = self.test_transit.lnprob_gp()
        #print("Took ", time.time() - s)

    def modelHelper(self, params, t):
        """ The model to sample the observations """
        amp, loc, sig2 = params
        return amp * np.exp(-0.5 * (t - loc) ** 2 / sig2)

    def generateDataHelper(self, N, rng=(-5, 5)):
        """
        Generates an artificial dataset for testing

        :param N: number of the datapoints
        :param rng: over what timerange to generate the data
        :return: t, y, yerr - time, observations and the errors in the observations
         """
        true_params = [-1.0, 0.1, 0.4]
        gp = george.GP(0.1 * kernels.ExpSquaredKernel(3.3))
        t = rng[0] + np.diff(rng) * np.sort(np.random.rand(N))
        y = gp.sample(t)
        y += self.modelHelper(true_params, t)
        yerr1 = 0.05 + 0.05 * np.random.rand(N)
        yerr2 = -0.05 + 0.05 * np.random.rand(N)
        yerr3 = 0.1 + 0.05 * np.random.rand(N)
        y += yerr1 * np.random.randn(N)


        return t, y, yerr1, yerr2, yerr3

    def testCustomInit(self):
        """ Testing the customized init of the model """

        # assert the parameters has not been changed before are taken

        self.assertTrue(self.test_transit.params.a == 15.)
        self.assertTrue(self.test_transit.u_prior_upper == 1.)
        self.assertTrue(self.test_transit.rp_prior_lower == -1.)
        self.assertTrue(self.test_transit.params.ecc == 0.)

        # reinitialize some of the parameters and checks if they have the correct values

        new_params = self.params
        new_params["u0"] = 1.; new_params["u1"] = -1.; new_params["u2"] = 1.; new_params["u3"] = -1.;
        new_params['a'] = 1.; new_params['ecc'] = 3.; new_params['rp_prior_lower'] = -2.
        new_params['u_prior_upper'] = 3
        self.test_transit = TransitModel(**new_params)

        self.assertTrue(self.test_transit.params.a == 1.)
        self.assertTrue(self.test_transit.u_prior_upper == 3.)
        self.assertTrue(self.test_transit.rp_prior_lower == -2.)
        self.assertTrue(self.test_transit.params.ecc == 3.)
        self.assertTrue(self.test_transit.params.u == [1., -1., 1., -1.])

        pass

    def testDataUpdate(self):
        """ Tests partial and full data update  """

        # assert that the model was initialized with an empty data - as expected (default)
        self.assertTrue(self.test_transit.y is None)
        self.assertTrue(self.test_transit.yerr1 is None)

        t_prev = self.test_transit.t

        t, y, yerr1, yerr2, yerr3 = self.generateDataHelper(N=20)

        # update the observations only and check if other have not changed
        self.test_transit.update_data(obs=y)

        self.assertTrue(np.array_equal(self.test_transit.t, t_prev))
        self.assertTrue(self.test_transit.y is not None)
        self.assertTrue(self.test_transit.yerr1 is None)

        # update the rest and check if other have the correct values
        errors = {'yerr1': yerr1, 'yerr2': yerr2, 'yerr3': yerr3}
        self.test_transit.update_data(time=t, **errors)

        self.assertTrue(np.array_equal(self.test_transit.t, t))
        self.assertTrue(np.array_equal(self.test_transit.y, y))
        self.assertTrue(np.array_equal(self.test_transit.yerr1, yerr1))
        self.assertTrue(np.array_equal(self.test_transit.yerr2, yerr2))
        self.assertTrue(np.array_equal(self.test_transit.yerr3, yerr3))

        pass

    def testTransitParamsUpdate(self):
        rp_new1 = None; rp_new2 = 10;
        u_new1 = None; u_new2 = [1.]; u_new3 = [1., 2., 3., 4.]

        with self.assertRaises(ValueError):
            self.test_transit.update_transit_params(rp_new1, u_new1)
        with self.assertRaises(ValueError):
            self.test_transit.update_transit_params(rp_new2, u_new1)
        with self.assertRaises(ValueError):
            self.test_transit.update_transit_params(rp_new2, u_new2)

        self.test_transit.update_transit_params(rp_new2, u_new3)

        self.assertTrue(self.test_transit.params.rp == rp_new2)
        self.assertTrue(self.test_transit.params.u == u_new3)

        pass

    def testKernelParamsUpdate(self):
        a_new1 = None; a_new2 = 10.

        gamma_new1 = None; gamma_new2 = 10.
        gamma_new3 = [i for i in range(self.test_transit.n_errors)]
        gamma_new4 = [i for i in range(self.test_transit.n_errors+1)]

        variance_new1 = None; variance_new2 = 10.

        a_prev = self.test_transit.kernel_a
        gamm_prev = self.test_transit.kernel_gamma

        self.test_transit.update_kernel_params(a_new=a_new1, gamma_new=gamma_new1)
        self.assertTrue(self.test_transit.kernel_a == a_prev)
        self.assertTrue(self.test_transit.kernel_gamma == gamm_prev)

        with self.assertRaises(TypeError):
            self.test_transit.update_kernel_params(a_new2, gamma_new2, variance_new2)

        with self.assertRaises(ValueError):
            self.test_transit.update_kernel_params(a_new2, gamma_new3, variance_new2)

        self.test_transit.update_kernel_params(a_new2, gamma_new4, variance_new2)

        self.assertTrue(self.test_transit.kernel_a == a_new2)
        self.assertTrue(self.test_transit.kernel_gamma == gamma_new4)
        self.assertTrue(self.test_transit.kernel_variance == variance_new2)

        pass

    def testModelInitializedProperly(self):
        """ Tests if the program stops in case some data is missing """

        with self.assertRaises(ValueError):
            self.test_transit.lnlike_gp()

        pass

    def testLnpriorBase(self):
        """ Testing if the lnPrior_base() function behaves as expected """

        rp1_too_high = self.test_transit.rp_prior_upper+0.1
        u1_too_low = [0.5, self.test_transit.u_prior_lower-0.1, 0.1, -0.2 ]

        rp_current = self.test_transit.params.rp
        u_current = self.test_transit.params.u

        self.test_transit.update_transit_params(rp1_too_high, u_current)
        self.assertTrue(self.test_transit.lnprior_base() == -np.inf)

        self.test_transit.update_transit_params(rp_current, u1_too_low)
        self.assertTrue(self.test_transit.lnprior_base() == -np.inf)

        self.test_transit.update_transit_params(rp_current, u_current)
        self.assertTrue(self.test_transit.lnprior_base() == 0.)

        pass

    def test_lnprior_gp(self):
        """ Testing if the lnPrior_gp() function behaves as expected """

        kernel_a1 = self.test_transit.kernel_a_prior_lower - 0.1
        kernel_a2 = self.test_transit.kernel_a_prior_lower + 0.1

        t = np.linspace(-1,1,20); y = np.linspace(-1,1,20)
        errors = {'yerr1': np.linspace(-1,1,20), 'yerr2': np.linspace(-1,1,20), 'yerr3': np.linspace(-1,1,20)}
        self.test_transit.update_data(time=t, obs=y, **errors)

        kernel_gamma1 = [self.test_transit.kernel_gamma_prior_upper + 0.1, 1., 1., 1.]
        kernel_gamma2 = [self.test_transit.kernel_gamma_prior_upper - 0.1, 1., 1., 1.]

        kernel_variance1 = 0.
        kernel_variance2 = 4.

        self.test_transit.update_kernel_params(kernel_a1, kernel_gamma1, kernel_variance1)
        self.assertTrue(self.test_transit.lnprior_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a1, kernel_gamma2, kernel_variance2)
        self.assertTrue(self.test_transit.lnprior_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a2, kernel_gamma2, kernel_variance1)
        self.assertTrue(self.test_transit.lnprior_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a2, kernel_gamma1, kernel_variance2)
        self.assertTrue(self.test_transit.lnprior_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a2, kernel_gamma2, kernel_variance2)
        self.assertTrue(self.test_transit.lnprior_gp() != -np.inf)
        pass


    def test_lnprob_gp(self):

        t = np.linspace(1,10,20); y = np.linspace(-21,20,20)
        errors = {'yerr1': np.linspace(-1,1,20), 'yerr2': np.linspace(-5,5,20), 'yerr3': np.linspace(-3,3,20)}
        self.test_transit.update_data(time=t, obs=y, **errors)
        self.test_transit.update_data(time=t, obs=y, **errors)

        kernel_a = 1.
        kernel_gamma = [self.test_transit.kernel_gamma_prior_upper - 0.1, 1., 1., 1.]
        kernel_variance1 = 0.
        kernel_variance2 = 1.

        rp_current1 = self.test_transit.rp_prior_upper+0.1
        rp_current2 = self.test_transit.params.rp
        u = self.test_transit.params.u

        self.test_transit.update_kernel_params(kernel_a, kernel_gamma, kernel_variance1)
        self.test_transit.update_transit_params(rp_current2, u)
        self.assertTrue(self.test_transit.lnprob_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a, kernel_gamma, kernel_variance2)
        self.test_transit.update_transit_params(rp_current1, u)
        self.assertTrue(self.test_transit.lnprob_gp() == -np.inf)

        self.test_transit.update_kernel_params(kernel_a, kernel_gamma, kernel_variance2)
        self.test_transit.update_transit_params(rp_current2, u)
        self.assertTrue(self.test_transit.lnprob_gp() != -np.inf)

        pass

if __name__ == '__main__':
    unittest.main()
