## @file
#Fits a transit lightcurve for a single wavelength
import numpy as np
import os

import deliverables
import TransitModel
import mcmc


## Definition which carries out the procedure for fitting a single wavelength.
# This follows the steps of: initializing a TransitModel object with correct
# data for that wavelength, initializing an mcmc object and running it,
# saving the results of mcmc run, and making walker and triangle plots
# for that mcmc run.
# @params input_param_dic A dictionary of input parameter values
# @params LC_dic A light curve dictionary containing the wavelength data
# @params wl_id The key for the wavelength to be fit
# @retval 0 if successful
def run_mcmc_single_wl(input_param_dic, LC_dic, wl_id):

    # add wavelength specific info to the parameter dictionary
    x = LC_dic[wl_id].time # times
    y = LC_dic[wl_id].flux # flux
    yerr = LC_dic[wl_id].ferr # flux error
    aparam_num = LC_dic[wl_id].param_num # number of auxiliary measures
    aparam_list = LC_dic[wl_id].param_list # auxiliary measures
    input_param_dic['t'] = x
    input_param_dic['y'] = y
    input_param_dic['yerr1'] = yerr
    for i in range(input_param_dic['n_errors']):
        input_param_dic['yerr'+str(i+2)]= aparam_list[i]

    #initialize model object
    model = TransitModel.TransitModel(**input_param_dic)

    # get user specified instructions for MCMC from input file
    nwalkers = input_param_dic['nwalkers']
    nburnin = input_param_dic['nburnin']
    nsteps = input_param_dic['nsteps']
    ndim = input_param_dic['ndim']
    nthreads = input_param_dic['nthreads']
    transit_par_names = input_param_dic['transit_par_names']
    gp_hyper_par_names = input_param_dic['gp_hyper_par_names']
    p0 = input_param_dic['p0']  # the initial guess for model parameters

    # initialize MCMC object
    LC_dic[wl_id].obj_mcmc = mcmc.MCMC(x, y, yerr, model.lnprob_mcmc,
                                       transit_par_names, gp_hyper_par_names,
                                       nwalkers, nthreads)
    # starting positions for walkers
    pos = np.array([p0 + 1e-4*np.random.randn(ndim) for i in range(nwalkers)])

    # run MCMC and store chain in LC_dic[wl_id]
    LC_dic[wl_id].obj_chain = LC_dic[wl_id].obj_mcmc.run(pos, nburnin, nsteps)

    # store model object in LC_dic[wl_id] with parameters set to best values
    median, err1, err2 = LC_dic[wl_id].obj_mcmc.get_median_and_errors()
    accept_frac = LC_dic[wl_id].obj_mcmc.get_mean_acceptance_fraction()
    best_fit = model.sample_conditional(median, x, y, yerr)
    LC_dic[wl_id].transit_model = model
    output_dir = input_param_dic['output_dir']

    # create an output folder if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # always save the chain
    LC_dic[wl_id].obj_mcmc.save_chain(output_dir+"/"+'mcmc_chain_'+wl_id+'.out')

    # if visualization is True save plots for this wavelength
    if input_param_dic['visualization']:
        output_dir = input_param_dic['output_dir']
        deliverables.plot_single_wavelength(wl_id, LC_dic[wl_id].obj_mcmc,
                     LC_dic[wl_id].transit_model.sample_conditional,
                     extra_burnin_steps=0, theta_true=None,
                     plot_transit_params=True, plot_hyper_params=True,
                     save_as_dir=output_dir)



    return 0
