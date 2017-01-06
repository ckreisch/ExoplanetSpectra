
# coding: utf-8

# In[11]:

#%matplotlib inline
import numpy as np
from matplotlib import pyplot as plt
import emcee
import george
from george import kernels


# In[2]:

def model(params, t):
    amp, loc, sig2 = params
    return amp * np.exp(-0.5 * (t - loc) ** 2 / sig2)

def generate_data(params, N, rng=(-5, 5)):
    gp = george.GP(0.1 * kernels.ExpSquaredKernel(3.3))
    t = rng[0] + np.diff(rng) * np.sort(np.random.rand(N))
    y = gp.sample(t)
    y += model(params, t)
    yerr = 0.05 + 0.05 * np.random.rand(N)
    y += yerr * np.random.randn(N)
    return t, y, yerr

def lnlike_gp(p, t, y, yerr):
    a, tau = np.exp(p[:2])
    gp = george.GP(a * kernels.Matern32Kernel(tau))
    gp.compute(t, yerr)
    return gp.lnlikelihood(y - model(p[2:], t))

def lnprior_base(p):
    amp, loc, sig2 = p
    if not -10 < amp < 10:
        return -np.inf
    if not -5 < loc < 5:
        return -np.inf
    if not 0 < sig2 < 3.0:
        return -np.inf
    return 0.0

def lnprior_gp(p):
    lna, lntau = p[:2]
    if not -5 < lna < 5:
        return -np.inf
    if not -5 < lntau < 5:
        return -np.inf
    return lnprior_base(p[2:])

def lnprob_gp(p, t, y, yerr):
    lp = lnprior_gp(p)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike_gp(p, t, y, yerr)

def fit_gp(initial, data, nwalkers=32):
    ndim = len(initial)
    p0 = [np.array(initial) + 1e-8 * np.random.randn(ndim)
          for i in range(nwalkers)]
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob_gp, args=data)

    print("Running burn-in")
    p0, lnp, _ = sampler.run_mcmc(p0, 500)
    sampler.reset()

    print("Running second burn-in")
    p = p0[np.argmax(lnp)]
    p0 = [p + 1e-8 * np.random.randn(ndim) for i in range(nwalkers)]
    p0, _, _ = sampler.run_mcmc(p0, 500)
    sampler.reset()

    print("Running production")
    p0, _, _ = sampler.run_mcmc(p0, 1000)

    return sampler


# In[9]:

def run(true_params, t = None, y = None, yerr = None, seed = 1):
    ''' params - alpha, loc and sigma^2 of the true model'''
    
    if ( (t==None) | (y==None) | (yerr==None) ):
        print("Not enough inputs. Simulating data ...")
        np.random.seed(seed)
        t, y, yerr = generate_data(true_params, 50)
        plt.errorbar(t, y, yerr=yerr, fmt=".k", capsize=0)
        plt.ylabel(r"$y$")
        plt.xlabel(r"$t$")
        plt.xlim(-5, 5)
        plt.title("simulated data")
    
    data = (t, y, yerr)   
    truth_gp = [0.0, 0.0] + true_params
    print("Fitting GP ...")
    sampler = fit_gp(truth_gp, data)
    
    # plot 5 fitted curves
    samples = sampler.flatchain
    x = np.linspace(-5, 5, 500)
    plt.figure()
    plt.errorbar(t, y, yerr=yerr, fmt=".k", capsize=0)
    for s in samples[np.random.randint(len(samples), size=5)]:
        gp = george.GP(np.exp(s[0]) * kernels.Matern32Kernel(np.exp(s[1])))
        gp.compute(t, yerr)
        m = gp.sample_conditional(y - model(s[2:], t), x) + model(s[2:], x)
        plt.plot(x, m, color="#4682b4", alpha=0.3)
    plt.ylabel(r"$y$")
    plt.xlabel(r"$t$")
    plt.xlim(-5, 5)
    plt.title("results with Gaussian process noise model")
    


# In[12]:

if __name__ == "__main__":
    true = [-1.0, 0.1, 0.4]
    run(true)


# In[ ]:



