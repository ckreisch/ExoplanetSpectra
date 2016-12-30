import emcee
import corner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time


class MCMC(object):
    def __init__(self, t, val, err, ln_prob_fn, transit_params, noise_params, num_walkers, num_threads):
        """Returns an object to run emcee and visualize results """
        self._t=t
        self._val=val
        self._err=err
        self._ln_prob_fn = ln_prob_fn
        self._transit_params=transit_params #strings for plotting
        self._noise_params=noise_params #strings for plotting
        self._all_params=transit_params+noise_params
        self._dim=len(self._all_params)
        self._nwalkers=num_walkers
        self._nthreads=num_threads
        self._sampler = emcee.EnsembleSampler(num_walkers, self._dim, self._ln_prob_fn, args=(t, val, err), threads=num_threads)



    def run(self, pos, burnin_steps, production_run_steps):
        """should run emcee given a log probability function
        result is the MCMC chains which are saved as an object attribute"""

        if burnin_steps>0:
            time0 = time.time()
            # burnin phase
            pos, prob, state  = self._sampler.run_mcmc(pos, burnin_steps)
            self._sampler.reset()
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


    def save_chains(self):
        #saves the MCMC chains for the user to analyse
        return 0

    def triangle_plot(self, theta_true):
        #makes triangle plot
        m_true, b_true, f_true=theta_true
        burnin = 50
        samples = self._sampler.chain[:, burnin:, :].reshape((-1, self._dim))

        fig = corner.corner(samples, labels=["$m$", "$b$", "$\ln\,f$"],
                              truths=[m_true, b_true, np.log(f_true)])
        fig.savefig("line-triangle.png")
        plt.show()


    def walker_plot(self, theta_true):
        #makes a walker plot
        m_true, b_true, f_true=theta_true

        plt.clf()
        fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 9))
        axes[0].plot(self._sampler.chain[:, :, 0].T, color="k", alpha=0.4)
        axes[0].yaxis.set_major_locator(MaxNLocator(5))
        axes[0].axhline(m_true, color="#888888", lw=2)
        axes[0].set_ylabel("$m$")

        axes[1].plot(self._sampler.chain[:, :, 1].T, color="k", alpha=0.4)
        axes[1].yaxis.set_major_locator(MaxNLocator(5))
        axes[1].axhline(b_true, color="#888888", lw=2)
        axes[1].set_ylabel("$b$")

        axes[2].plot(np.exp(self._sampler.chain[:, :, 2]).T, color="k", alpha=0.4)
        axes[2].yaxis.set_major_locator(MaxNLocator(5))
        axes[2].axhline(f_true, color="#888888", lw=2)
        axes[2].set_ylabel("$f$")
        axes[2].set_xlabel("step number")

        fig.tight_layout(h_pad=0.0)
        fig.savefig("line-time.png")
        plt.show()

    def light_curve_plot(self, t, model, theta_true):
        # Plot some samples onto the data.
        burnin = 50
        samples = self._sampler.chain[:, burnin:, :].reshape((-1, self._dim))

        plt.figure()
        for theta in samples[np.random.randint(len(samples), size=100)]:
            plt.plot(t, model(theta, t), color="k", alpha=0.1)
        plt.plot(t, model(theta_true, t), color="r", lw=2, alpha=0.8)
        plt.errorbar(self._t, self._val, yerr=self._err, fmt=".k")
        plt.ylim(-9, 9)
        plt.xlabel("$t$")
        plt.ylabel("flux")
        plt.tight_layout()
        plt.savefig("line-mcmc.png")
        plt.show()
