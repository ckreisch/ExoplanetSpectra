#import mcmc
import os
import sys
import inspect
dir_current = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_up = os.path.dirname(dir_current)
sys.path.append(dir_up)

from exospec import mcmc
import unittest
import mcmc_test_case

class TestMCMC(unittest.TestCase):
    def setUp(self):
        x, y, yerr, theta_true=mcmc_test_case.get_data()
        self.data=(x,y,yerr)
        self.true_params=theta_true
        self.nwalkers=100

        self.pos_init = mcmc_test_case.get_init_pos(self.true_params, self.data, self.nwalkers)

        self.mcmc_hyper=mcmc.MCMC(x, y, yerr, mcmc_test_case.lnprob, ["m", "b"] , ["lnf"], self.nwalkers, 1)
        self.mcmc_nohyper=mcmc.MCMC(x, y, yerr, mcmc_test_case.lnprob, ["m", "b", "lnf"] , [], self.nwalkers, 1)

        #create directory to test if plot is saved correctly

    def test_mcmc_basic_run(self):
        steps=500
        c1=self.mcmc_hyper.run(self.pos_init, 0, steps)
        c2=self.mcmc_nohyper.run(self.pos_init, 0, steps)

        self.assertTrue(c1.shape==(steps*self.nwalkers, len(self.true_params)))
        self.assertTrue(c2.shape==(steps*self.nwalkers, len(self.true_params)))

    def test_run_with_burnin(self):
        burnin=50
        steps=500
        c1=self.mcmc_hyper.run(self.pos_init, burnin, steps)
        c2=self.mcmc_nohyper.run(self.pos_init, burnin, steps)

        self.assertTrue(c1.shape==(steps*self.nwalkers, len(self.true_params)))
        self.assertTrue(c2.shape==(steps*self.nwalkers, len(self.true_params)))

    def test_plots_before_run(self):
        pass

    def test_walker_plots(self):
        #mcmc1.walker_plot(50,theta_true)
        #mcmc1.walker_plot(50, theta_true[0:2], True, False)
        #mcmc1.walker_plot(50, theta_true[2:], False, True)
        #mcmc1.walker_plot(50, theta_true[2:], False, False)

        #mcmc2.walker_plot(5000,theta_true)
        #mcmc2.walker_plot(50,theta_true)
        #mcmc2.walker_plot(50,theta_true, False, True)
        #mcmc2.walker_plot(50)
        #mcmc2.walker_plot()
        pass

    def test_triangle_plots(self):
        #mcmc1.triangle_plot(50, theta_true)
        #mcmc1.triangle_plot(50)
        #mcmc1.triangle_plot()
        #mcmc1.light_curve_plot(model_fn, 50, theta_true)
        #mcmc2.triangle_plot()
        pass

    def test_light_curve_plots(self):
        pass

    def test_mean_acceptance(self):
        pass

    def test_save_chains(self):
        pass

    def test_median_err(self):
        pass

    def tearDown(self):
        #delete directory created in setup
        pass





if __name__ == "__main__":
    unittest.main()
