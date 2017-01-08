import emcee
import corner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time


class MCMC(object):
    def __init__(self, t, val, err, ln_prob_fn, transit_params, hyper_params, num_walkers, num_threads):#, burnin_steps=0):
        """Returns an object to run emcee and visualize results """
        self._t=t
        self._val=val
        self._err=err
        self._ln_prob_fn = ln_prob_fn
        self._transit_params=transit_params #strings for plotting
        self._hyper_params=hyper_params #strings for plotting
        self._all_params=transit_params+hyper_params
        self._dim=len(self._all_params)
        self._nwalkers=num_walkers
        self._nthreads=num_threads
        #self._burnin_steps=burnin_steps
        self._sampler = emcee.EnsembleSampler(self._nwalkers, self._dim, self._ln_prob_fn, args=(self._t, self._val, self._err), threads=self._nthreads)


    def run(self, pos, burnin_steps, production_run_steps):
        """should run emcee given a log probability function
        result is the MCMC chains which are saved as an object attribute"""
        #burnin_steps=max(self._burnin_steps, burnin_steps)  #when you run you can choose to use a longer burnin than you may have set when initialising the object

        if burnin_steps>0:
            time0 = time.time()
            # burnin phase
            pos, prob, state  = sampler.run_mcmc(pos, burnin_steps)
            sampler.reset()
            time1=time.time()
            print "burnin time: %f" %(time1-time0)
        elif burnin_steps==0:
            print "no burnin requested"
        else:
            print "Warning: incorrect input for burnin steps!"

        time0 = time.time()
        # perform MCMC
        pos, prob, state  = self._sampler.run_mcmc(pos, production_run_steps)
        time1=time.time()
        print "production run time: %f"%(time1-time0)

        samples = self._sampler.flatchain
        # samples.shape
        return samples

    def update_ln_prob_fn(self, ln_prob_fn):
        "user may want to try to fit the same dater using a different likelihood funtion"
        self._ln_prob_fn = ln_prob_fn

    def update_num_walkers(self, num_walkers):
        self._nwalkers=num_walkers

    def update_num_threads(self, num_threads):
        self._nthreads=num_threads

    def save_chains(self):
        #saves the MCMC chains for the user to analyse
        return 0

    def get_acceptance_fraction(self):
        return 0

    def get_median_and_errors(self):
        return 0

    def triangle_plot(self, burnin_steps, theta_true=None):
        #makes triangle plot
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run
        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n \
            object_name.run(starting_positions, burnin_steps, production_run_steps) \n \
            to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n \
            Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1


        m_true, b_true, f_true=theta_true
        samples = self._sampler.chain[:, burnin_steps:, :].reshape((-1, self._dim))

        print "Checking flatchain:", self._sampler.chain.reshape((-1, self._dim))-self._sampler.flatchain


        fig = corner.corner(samples, labels=self._all_params,
                              truths=theta_true)
        fig.savefig("triangle.png")
        plt.show()


    def walker_plot(self, burnin_steps=50, theta_true=None):
        #makes a walker plot and histogram
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run

        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n \
            object_name.run(starting_positions, burnin_steps, production_run_steps) \n \
            to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n \
            Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1

        nplots=len(self._transit_params)
        #use gridspec??
        fig, axes = plt.subplots(nplots, 2, figsize=(8, 9))
        fig.subplots_adjust(wspace=0)

        for i, p in enumerate(self._transit_params):
            axes[i][0].hist(self._sampler.flatchain[burnin_steps:,i].T, bins=50, orientation='horizontal', alpha=.5)
            axes[i][0].yaxis.set_major_locator(MaxNLocator(5))
            axes[i][0].minorticks_off()
            axes[i][0].invert_xaxis()
            if theta_true:
                axes[i][0].axhline(theta_true[i], color="#888888", lw=2)
            axes[i][0].set_ylabel(p)
            if i+1==nplots:
                axes[i][0].set_xlabel("counts")

            axes[i][0].get_shared_y_axes().join(axes[i][0], axes[i][1])
            plt.setp(axes[i][1].get_yticklabels(), visible=False)
            # .T transposes the chains to plot each walker's position as a function of time
            axes[i][1].plot(self._sampler.chain[:, burnin_steps:, i].T, color="k", alpha=0.4)   #should it be .T??
            if theta_true:
                axes[i][1].axhline(theta_true[i], color="#888888", lw=2)
            if i+1==nplots:
                axes[i][1].set_xlabel("time")
            #axes[i][1].set_ylabel(p)

        fig.tight_layout(h_pad=0.0)
        fig.savefig("walkers.png")
        plt.show()


    def light_curve_plot(self, t, model, burnin_steps, theta_true):
        # Plot some samples onto the data.
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run

        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n \
            object_name.run(starting_positions, burnin_steps, production_run_steps) \n \
            to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n \
            Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1
            
        samples = self._sampler.chain[:, burnin_steps:, :].reshape((-1, self._dim))

        plt.figure()
        for theta in samples[np.random.randint(len(samples), size=100)]:
            plt.plot(t, model(theta, t), color="k", alpha=0.1)
        plt.plot(t, model(theta_true, t), color="r", lw=2, alpha=0.8)
        plt.errorbar(self._t, self._val, yerr=self._err, fmt=".k")
        plt.ylim(-9, 9)
        plt.xlabel("$t$")
        plt.ylabel("flux")
        plt.tight_layout()
        plt.savefig("light_curve.png")
        plt.show()
