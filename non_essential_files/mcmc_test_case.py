import numpy as np
import scipy.optimize as op
#Using a noisy straight line model as in #http://dan.iel.fm/emcee/current/user/line/ to test our MCMC class

def get_data():
    # Choose the "true" parameters.
    m_true = -1.
    b_true = 4.
    f_true = 0.5

    # Generate some synthetic data from the model.
    N = 50
    x = np.sort(10*np.random.rand(N))
    yerr = 0.1+0.5*np.random.rand(N)
    y = m_true*x+b_true
    y += np.abs(f_true*y) * np.random.randn(N)
    y += yerr * np.random.randn(N)

    theta_true=(m_true, b_true, np.log(f_true))
    return x, y, yerr, theta_true

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

def get_init_pos(theta_true, data, nwalkers):
    m_true, b_true, lnf_true=theta_true
    ndim=3

    chi2 = lambda *args: -2 * lnlike(*args)
    result = op.minimize(chi2, [m_true, b_true, lnf_true], args=data)

    pos = [result["x"] + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]
    return pos
