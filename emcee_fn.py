
import emcee
import time

'''maybe good to do some tests on the inputs'''

def run_emcee (nwalkers, ndim, lnprob, args_for_lnprob, pos, burnin_steps, production_run_steps):
    """run the emcee package"""
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=args_for_lnprob)

    if burnin_steps>0:
        time0 = time.time()
        # burnin phase
        pos, prob, state  = sampler.run_mcmc(pos, burnin_steps)
        sampler.reset()
        time1=time.time()
        print "burnin time: %f" %(time1-time0)
    else:
        print "Warning: incorrect input for burnin steps!"

    time0 = time.time()
    # perform MCMC
    pos, prob, state  = sampler.run_mcmc(pos, production_run_steps)
    time1=time.time()
    print "production run time: %f"%(time1-time0)

    samples = sampler.flatchain
    # samples.shape
    return samples
