#http://dan.iel.fm/emcee/current/user/line/
import mcmc
import numpy as np
import matplotlib.pyplot as pl
import scipy.optimize as op

def get_data():
    # Choose the "true" parameters.
    m_true = -0.9594
    b_true = 4.294
    f_true = 0.534

    # Generate some synthetic data from the model.
    N = 50
    x = np.sort(10*np.random.rand(N))
    yerr = 0.1+0.5*np.random.rand(N)
    y = m_true*x+b_true
    y += np.abs(f_true*y) * np.random.randn(N)
    y += yerr * np.random.randn(N)

    # Plot the dataset and the true model.
    xl = np.array([0, 10])
    pl.errorbar(x, y, yerr=yerr, fmt=".k")
    pl.plot(xl, m_true*xl+b_true, "k", lw=3, alpha=0.6)
    pl.ylim(-9, 9)
    pl.xlabel("$x$")
    pl.ylabel("$y$")
    pl.tight_layout()
    pl.savefig("line-data.png")
    pl.close()

    theta_true=(m_true, b_true, f_true)
    return x, y, yerr, theta_true

# Define the probability function as likelihood * prior.
def lnprior(theta):
    m, b, lnf = theta
    if -5.0 < m < 0.5 and 0.0 < b < 10.0 and -10.0 < lnf < 1.0:
        return 0.0
    return -np.inf

def lnlike(theta, x, y, yerr):
    m, b, lnf = theta
    model = m * x + b
    inv_sigma2 = 1.0/(yerr**2 + model**2*np.exp(2*lnf))
    return -0.5*(np.sum((y-model)**2*inv_sigma2 - np.log(inv_sigma2)))

def lnprob(theta, x, y, yerr):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, y, yerr)

def model_fn(theta, x):
    m, b, lnf = theta
    model = m * x + b
    return model

if __name__=="__main__":
    x, y, yerr, theta_true=get_data()
    m_true, b_true, f_true=theta_true
    nwalkers=100
    ndim=3

    mcmc1=mcmc.MCMC(x, y, yerr, lnprob, ["m", "b"] , ["lnf"], nwalkers, 1)

    # Find the maximum likelihood value.
    chi2 = lambda *args: -2 * lnlike(*args)
    result = op.minimize(chi2, [m_true, b_true, np.log(f_true)], args=(x, y, yerr))

    pos = [result["x"] + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]

    #I will incorporate the cases below into a unittest soon
    mcmc1.run(pos, 0, 500)

    xl = np.array([0, 10])
    mcmc1.walker_plot(50,theta_true)
    mcmc1.triangle_plot(50, theta_true)
    #mcmc1.triangle_plot(50)
    #mcmc1.triangle_plot()
    mcmc1.light_curve_plot(model_fn, 50, theta_true)
    med, err1, err2=mcmc1.get_median_and_errors()
    print "Acceptance fraction: ", mcmc1.get_mean_acceptance_fraction()

    mcmc2=mcmc.MCMC(x, y, yerr, lnprob, ["m", "b", "lnf"] , [], nwalkers, 1)
    #mcmc2.walker_plot(50,theta_true)
    mcmc2.run(pos, 0, 500)
    mcmc2.walker_plot(5000,theta_true)
    #mcmc2.walker_plot(50,theta_true)
    #mcmc2.walker_plot(50)
    #mcmc2.walker_plot()
    #mcmc2.triangle_plot()
    #mcmc2.light_curve_plot(xl, model_fn, theta_true)
    #mcmc2.light_curve_plot(model_fn)
    med, err1, err2=mcmc2.get_median_and_errors()
    print "Acceptance fraction: ", mcmc2.get_mean_acceptance_fraction()
