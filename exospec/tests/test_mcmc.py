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
        self.nwalkers=10
        self.steps=100
        self.pos_init = mcmc_test_case.get_init_pos(self.true_params, self.data, self.nwalkers)

        self.mcmc_hyper=mcmc.MCMC(x, y, yerr, mcmc_test_case.lnprob, ["m", "b"] , ["lnf"], self.nwalkers, 1)
        self.mcmc_nohyper=mcmc.MCMC(x, y, yerr, mcmc_test_case.lnprob, ["m", "b", "lnf"] , [], self.nwalkers, 1)

        c1=self.mcmc_hyper.run(self.pos_init, 0, self.steps)
        c2=self.mcmc_nohyper.run(self.pos_init, 0, self.steps)
        self.flatchain_hyper=c1
        self.flatchain_nohyper=c2

        self.mcmc_hyper_no_run=mcmc.MCMC(x, y, yerr, mcmc_test_case.lnprob, ["m", "b"] , ["lnf"], self.nwalkers, 1)

        #create directory to test if plot is saved correctly.
        #This directory is removed in tearDown
        self.saving_dir="mcmc_test"
        os.mkdir(self.saving_dir)

    def test_mcmc_basic_run(self):
        self.assertTrue(self.flatchain_hyper.shape==(self.steps*self.nwalkers, len(self.true_params)))
        self.assertTrue(self.flatchain_nohyper.shape==(self.steps*self.nwalkers, len(self.true_params)))

    def test_run_with_burnin(self):
        burnin=5
        steps=50
        c1=self.mcmc_hyper.run(self.pos_init, burnin, steps)
        c2=self.mcmc_nohyper.run(self.pos_init, burnin, steps)

        self.assertTrue(c1.shape==(steps*self.nwalkers, len(self.true_params)))
        self.assertTrue(c2.shape==(steps*self.nwalkers, len(self.true_params)))

    def test_plotting_routines(self):
        #Test walker and triangle plots for transit and hyper params are successful
        w1=self.mcmc_hyper.walker_plot(50,self.true_params, save_as_dir=self.saving_dir, save_as_name="w1.png")
        self.assertTrue(w1==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w1.png"))

        t1=self.mcmc_hyper.triangle_plot(50,self.true_params, save_as_dir=self.saving_dir, save_as_name="t1.png")
        self.assertTrue(t1==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t1.png"))

        #Test walker and triangle plots for just transit params are successful
        w2=self.mcmc_hyper.walker_plot(50, self.true_params[0:2], True, False, save_as_dir=self.saving_dir, save_as_name="w2.png")
        self.assertTrue(w2==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w2.png"))

        t2=self.mcmc_hyper.triangle_plot(50, self.true_params[0:2], True, False, save_as_dir=self.saving_dir, save_as_name="t2.png")
        self.assertTrue(t2==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t2.png"))

        #Test walker and triangle plots for just hyper params are successful
        w3=self.mcmc_hyper.walker_plot(50, self.true_params[2:], False, True, save_as_dir=self.saving_dir, save_as_name="w3.png")
        self.assertTrue(w3==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w3.png"))

        t3=self.mcmc_hyper.triangle_plot(50, self.true_params[2:], False, True, save_as_dir=self.saving_dir, save_as_name="t3.png")
        self.assertTrue(t3==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t3.png"))

        #Test walker and triangle plots with an extra burnin phase removed are successful
        w4=self.mcmc_nohyper.walker_plot(50,self.true_params, save_as_dir=self.saving_dir, save_as_name="w4.png")
        self.assertTrue(w4==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w4.png"))

        t4=self.mcmc_nohyper.triangle_plot(50,self.true_params, save_as_dir=self.saving_dir, save_as_name="t4.png")
        self.assertTrue(t4==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t4.png"))

        #Test walker and triangle plots with no true values specified are successful
        w5=self.mcmc_nohyper.walker_plot(50, save_as_dir=self.saving_dir, save_as_name="w5.png")
        self.assertTrue(w5==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w5.png"))

        t5=self.mcmc_nohyper.triangle_plot(50, save_as_dir=self.saving_dir, save_as_name="t5.png")
        self.assertTrue(t5==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t5.png"))

        #Test walker and triangle plots with no true values or burnin specified are successful
        w6=self.mcmc_nohyper.walker_plot(save_as_dir=self.saving_dir, save_as_name="w6.png")
        self.assertTrue(w6==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/w6.png"))

        t6=self.mcmc_nohyper.triangle_plot(save_as_dir=self.saving_dir, save_as_name="t6.png")
        self.assertTrue(t6==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/t6.png"))

        #test light_curve_plot with true values known
        l1=self.mcmc_nohyper.light_curve_plot(mcmc_test_case.model_fn, 0, self.true_params, save_as_dir=self.saving_dir, save_as_name="l1.png")
        self.assertTrue(l1==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/l1.png"))

        #test light_curve_plot without true values known
        l2=self.mcmc_nohyper.light_curve_plot(mcmc_test_case.model_fn, save_as_dir=self.saving_dir, save_as_name="l2.png")
        self.assertTrue(l1==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/l1.png"))
        l2=self.mcmc_nohyper.light_curve_plot(mcmc_test_case.model_fn, save_as_name="l2.png")

        #Calling the plot routines as below should be unsuccessful. wf=walker fail, tf=triangle fail

        #Test that asking for neither transit nor hyper parameter plots is unsuccessful
        wf1=self.mcmc_hyper.walker_plot(50, self.true_params[2:], False, False, save_as_dir=self.saving_dir, save_as_name="wf1.png")
        self.assertTrue(wf1==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/wf1.png"))

        tf1=self.mcmc_hyper.triangle_plot(50, self.true_params[2:], False, False, save_as_dir=self.saving_dir, save_as_name="tf1.png")
        self.assertTrue(tf1==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/tf1.png"))

        #test that trying to have too many extra burnin steps is unsuccessful
        wf2=self.mcmc_nohyper.walker_plot(5000,self.true_params, save_as_dir=self.saving_dir, save_as_name="wf2.png")
        self.assertTrue(wf2==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/wf2.png"))

        tf2=self.mcmc_nohyper.triangle_plot(5000,self.true_params, save_as_dir=self.saving_dir, save_as_name="tf2.png")
        self.assertTrue(tf2==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/tf2.png"))

        #Trying to only plot hyper parameters when none exist is unsuccessful
        wf3=self.mcmc_nohyper.walker_plot(50,[], False, True, save_as_dir=self.saving_dir, save_as_name="wf3.png")
        self.assertTrue(wf3==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/wf3.png"))

        tf3=self.mcmc_nohyper.triangle_plot(50,[], False, True, save_as_dir=self.saving_dir, save_as_name="tf3.png")
        self.assertTrue(tf3==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/tf3.png"))

        #If an MCMC object has not been run yet it's chain is empty so plot should fail
        wf4=self.mcmc_hyper_no_run.walker_plot(0,self.true_params, save_as_dir=self.saving_dir, save_as_name="wf4.png")
        self.assertTrue(wf4==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/wf4.png"))

        tf4=self.mcmc_hyper_no_run.triangle_plot(0,self.true_params, save_as_dir=self.saving_dir, save_as_name="tf4.png")
        self.assertTrue(tf4==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/tf4.png"))


    def test_mean_acceptance(self):
        #ensure that acceptance fraction is a float between 0 and 1
        a1=self.mcmc_hyper.get_mean_acceptance_fraction()
        self.assertTrue(isinstance(a1,float))
        self.assertTrue(a1>0 and a1<1)
        a2=self.mcmc_nohyper.get_mean_acceptance_fraction()
        self.assertTrue(isinstance(a2,float))
        self.assertTrue(a2>0 and a2<1)

    def test_save_chains(self):
        s1=self.mcmc_hyper.save_chain(self.saving_dir+"/chain1.txt")
        self.assertTrue(s1==0)
        self.assertTrue(os.path.isfile(self.saving_dir+"/chain1.txt"))

        #Try save in a directory that does not exist:
        s1=self.mcmc_hyper.save_chain(self.saving_dir+"/nonexistent_chain_directory/chain1.txt")
        self.assertTrue(s1==1)
        self.assertFalse(os.path.isfile(self.saving_dir+"/nonexistent_chain_directory/chain1.txt"))

    def test_median_err(self):
        median1, err_plus1, err_minus1=self.mcmc_hyper.get_median_and_errors()
        self.assertTrue(len(median1)==len(self.true_params))
        self.assertTrue(len(err_plus1)==len(self.true_params))
        self.assertTrue(len(err_minus1)==len(self.true_params))

        median2, err_plus2, err_minus2=self.mcmc_nohyper.get_median_and_errors()
        self.assertTrue(len(median2)==len(self.true_params))
        self.assertTrue(len(err_plus2)==len(self.true_params))
        self.assertTrue(len(err_minus2)==len(self.true_params))



    def tearDown(self):
        #delete directory created in setup
        import shutil
        shutil.rmtree(self.saving_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
