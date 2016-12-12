import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
plt.rcParams['font.size']=20
import corner

import emcee_fn as mc

# Generate synthetic data from a model.
# For simplicity, let us assume a LINEAR model y = m*x + b
# where we want to fit m and b
m_true = -0.9594
b_true = 4.294
N = 50

x = np.sort(10*np.random.rand(N))
yerr = 0.2 + 0.5*np.random.rand(N)
y = m_true*x + b_true
y += yerr * np.random.randn(N)

fig = plt.figure()
fig.set_size_inches(12, 8)
plt.errorbar(x, y, yerr=yerr, fmt='.k')

# Now, let's setup some parameters that define the MCMC
ndim = 2
nwalkers = 500

# Initialize the chain
# Choice 1: chain uniformly distributed in the range of the parameters
pos_min = np.array([-5., 0.])
pos_max = np.array([5., 10.])
psize = pos_max - pos_min
pos = [pos_min + psize*np.random.rand(ndim) for i in range(nwalkers)]

# Define the posterior PDF
# Reminder: post_pdf(theta, data) = likelihood(data, theta) * prior_pdf(theta)
# We take the logarithm since emcee needs it.

# As prior, we assume an 'uniform' prior (i.e. constant prob. density)
def lnprior(theta):
    m, b = theta
    if -5.0 < m < 0.5 and 0.0 < b < 10.0:
        return 0.0
    return -np.inf

# As likelihood, we assume the chi-square. Note: we do not even need to normalize it.
def lnlike(theta, x, y, yerr):
    m, b = theta
    model = m * x + b
    return -0.5*(np.sum( ((y-model)/yerr)**2. ))

def lnprob(theta, x, y, yerr):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, y, yerr)

# call the emcee solver:
samples = mc.run_emcee (nwalkers, ndim, lnprob,(x,y, yerr), pos, 0, 400)


#let's plot the results
plt.close('all')
fig = corner.corner(samples, labels=["$m$", "$b$"], extents=[[-1.1, -0.8], [3.5, 5.]],
                      truths=[m_true, b_true], quantiles=[0.16, 0.5, 0.84], show_titles=True, labels_args={"fontsize": 40})
# fig.set_size_inches(10,10)
fig.show()
