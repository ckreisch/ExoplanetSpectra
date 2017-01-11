import emcee
import corner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time


class MCMC(object):
    def __init__(self, t, val, err, ln_prob_fn, transit_params, hyper_params, num_walkers, num_threads):
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
        self._sampler = emcee.EnsembleSampler(self._nwalkers, self._dim, self._ln_prob_fn, args=(self._t, self._val, self._err), threads=self._nthreads)


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
            print "Warning: incorrect input for burnin steps, setting burnin to 0"

        time0 = time.time()
        # perform MCMC
        pos, prob, state  = self._sampler.run_mcmc(pos, production_run_steps)
        time1=time.time()
        print "production run time: %f"%(time1-time0)

        samples = self._sampler.flatchain
        # samples.shape
        return samples

    """
    consider adding as options once everything else is working:

    def update_ln_prob_fn(self, ln_prob_fn):
        "user may want to try to fit the same dater using a different likelihood funtion"
        self._ln_prob_fn = ln_prob_fn
        self._sampler = emcee.EnsembleSampler(self._nwalkers, self._dim, self._ln_prob_fn, args=(self._t, self._val, self._err), threads=self._nthreads)

    def update_num_walkers(self, num_walkers):
        self._nwalkers=num_walkers
        self._sampler = emcee.EnsembleSampler(self._nwalkers, self._dim, self._ln_prob_fn, args=(self._t, self._val, self._err), threads=self._nthreads)

    def update_num_threads(self, num_threads):
        self._nthreads=num_threads
        self._sampler = emcee.EnsembleSampler(self._nwalkers, self._dim, self._ln_prob_fn, args=(self._t, self._val, self._err), threads=self._nthreads)
    """

    def save_chain(self, filename):
        #saves the MCMC chains for the user to analyse
        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n" \
            "object_name.run(starting_positions, burnin_steps, production_run_steps) \n" \
            "to sample the posterior distribution before saving"
            return 1

        try:
            np.savetxt(filename, self._sampler.flatchain)
        except IOError:
            print "Invalid filename, unable to save chains"
            return 1
        return 0

    def get_mean_acceptance_fraction(self):
        return np.mean(self._sampler.acceptance_fraction)

    def get_median_and_errors(self):
        "return median and errors"
        "I plan to use ths to plot 1 sigma or 3 sigma confidence levels on the posterior probability distribution"
        ps=np.percentile(self._sampler.flatchain, [16, 50, 84],axis=0)
        median=ps[1]
        err_plus=ps[2]-ps[1]
        err_minus=ps[1]-ps[0]

        for i, p in enumerate(self._all_params):
            print p,"=",median[i],"+",err_plus[i],"-",err_minus[i]

        return median, err_plus, err_minus


    def triangle_plot(self, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, save_as_dir="", save_as_name="triangle.png"):
        #makes triangle plot
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run
        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n" \
            "object_name.run(starting_positions, burnin_steps, production_run_steps) \n" \
            "to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n" \
            "Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1

        if plot_transit_params and plot_hyper_params:
            samples = self._sampler.flatchain[burnin_steps:,:]
            fig = corner.corner(samples, labels=self._all_params, truths=theta_true)
        elif plot_transit_params:
            samples = self._sampler.flatchain[burnin_steps:, 0:len(self._transit_params)]
            fig = corner.corner(samples, labels=self._transit_params, truths=theta_true)    #check theta true shape!
        elif plot_hyper_params:
            if len(self._hyper_params)==0:
                print "You do not have any hyper parameters to plot. "\
                "Try plotting your transit parameters by setting plot_transit_params=True"
                return 1
            samples = self._sampler.flatchain[burnin_steps:, len(self._transit_params):]
            fig = corner.corner(samples, labels=self._hyper_params, truths=theta_true)    #check theta true shape!
        else:
            print "Either plot_transit_params or plot_hyper_params must be true"
            return 1
        fig.savefig(save_as_dir+save_as_name)   #check if it works, otherwise save in current directory and print message
        plt.close()


    def walker_plot(self, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, save_as_dir="", save_as_name="walkers.png"):
        #makes a walker plot and histogram
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run
        #check theta_true!!

        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n" \
            "object_name.run(starting_positions, burnin_steps, production_run_steps) \n" \
            "to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n" \
            "Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1

        if plot_transit_params and plot_hyper_params:
            params=self._all_params
            samples_flat=self._sampler.flatchain[burnin_steps:,:]
            samples=self._sampler.chain[:, burnin_steps:, :]
        elif plot_transit_params:
            params=self._transit_params
            samples_flat=self._sampler.flatchain[burnin_steps:,0:len(self._transit_params)]
            samples=self._sampler.chain[:, burnin_steps:, 0:len(self._transit_params)]
        elif plot_hyper_params:
            if len(self._hyper_params)==0:
                print "You do not have any hyper parameters to plot. "\
                "Try plotting your transit parameters by setting plot_transit_params=True"
                return 1
            params=self._hyper_params
            samples_flat=self._sampler.flatchain[burnin_steps:,len(self._transit_params):]
            samples=self._sampler.chain[:, burnin_steps:, len(self._transit_params):]
        else:
            print "Either plot_transit_params or plot_hyper_params must be true"
            return 1

        nplots=len(params)
        #use gridspec??
        fig, axes = plt.subplots(nplots, 2, figsize=(10, 2.5*nplots))
        fig.subplots_adjust(wspace=0)
        if nplots==1:
            axes=[axes] #want 2D array to index below

        for i, p in enumerate(params):
            axes[i][0].hist(samples_flat[:,i].T, bins=30, orientation='horizontal', alpha=.5)
            axes[i][0].yaxis.set_major_locator(MaxNLocator(5))
            axes[i][0].minorticks_off()
            axes[i][0].invert_xaxis()
            if theta_true:
                axes[i][0].axhline(theta_true[i], color="#888888", lw=2)
            axes[i][0].set_ylabel(p)
            if i+1==nplots:
                axes[i][0].set_xlabel("counts")

            axes[i][0].get_shared_y_axes().join(axes[i][0], axes[i][1])
            axes[i][1].minorticks_off()
            plt.setp(axes[i][1].get_yticklabels(), visible=False)
            # .T transposes the chains to plot each walker's position as a function of time
            axes[i][1].plot(samples[:, :, i].T, color="k", alpha=0.4)   #should it be .T??
            if theta_true:
                axes[i][1].axhline(theta_true[i], color="#888888", lw=2)
            if i+1==nplots:
                axes[i][1].set_xlabel("time")
            #axes[i][1].set_ylabel(p)

        fig.tight_layout(h_pad=0.0)
        fig.savefig(save_as_dir+save_as_name)
        plt.close()


    def light_curve_plot(self, model, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, save_as_dir="", save_as_name="light_curve"):
        # Plot some samples onto the data.
        #burnin_steps here means how many steps we discard when showing our plots. It doesn't have to match the burnin_steps argument to run
        #model is a function that takes an array of parameters and an array of times and evaluates the model
        if self._sampler.chain.shape[1]==0:
            print "The Markov chain is empty. Run MCMC using \n" \
            "object_name.run(starting_positions, burnin_steps, production_run_steps) \n" \
            "to sample the posterior distribution before plotting"
            return 1

        if self._sampler.chain.shape[1]<burnin_steps:
            print "The chain is shorter than the requested burnin. \n" \
            "Please run the chain for more iterations or reduce the burnin steps requested for the plot"
            return 1

        samples = self._sampler.flatchain # self._sampler.chain[:, burnin_steps:, :].reshape((-1, self._dim))

        t=self._t #can make it finer resolution
        plt.figure()
        for theta in samples[np.random.randint(len(samples), size=100)]:
            plt.plot(t, model(theta, t), color="k", alpha=0.1)
        if theta_true:
            plt.plot(t, model(theta_true, t), color="r", lw=2, alpha=0.8)
        plt.errorbar(self._t, self._val, yerr=self._err, fmt=".k")
        plt.xlabel("$t$")
        plt.ylabel("flux")
        plt.tight_layout()
        plt.savefig(save_as_dir+save_as_name)
        plt.close()
