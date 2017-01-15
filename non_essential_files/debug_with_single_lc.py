import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

import george
from george import kernels
import batman
import corner

import mcmc
import lc_class
from read_input import read_input
import TransitModel
import deliverables

# Read in MPI flag from user input file ---------------------------------------
try:
    input_file = read_input('test_suite_input_file.txt')
except IOError:
    print "Input file is not in the same directory as driver program."+\
            " Move to same directory or change path."
    raise
input_param_dic = input_file.param_dic
#remove following for loop once we correct read_input.py
for key in input_param_dic.keys():
    if len(input_param_dic[key]) == 1:
        input_param_dic[key]=input_param_dic[key][0]

mpi_flag = input_param_dic['mpi_flag']

if mpi_flag:
    try:
        from mpi4py import MPI
        #mpi_flag = True
    except ImportError:
        print "MPI not installed, but MPI flag set to True. Setting flag to" +\
                "False and continuing."
        mpi_flag = False
        pass

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # From user input file ----------------------------------------------------
    lc_path = input_param_dic['lc_path']
    wave_bin_size = input_param_dic['wave_bin_size']
    visualization = input_param_dic['visualization']
    confidence = input_param_dic['confidence']

    # Reading in the data -----------------------------------------------------

    LC = lc_class.LightCurve(lc_path, wave_bin_size)
    LC_dic = LC.LC_dic # dictionary of light curve for each wavelength

    wl_id = '650.0'
    nwalkers = input_param_dic['nwalkers']
    nburnin = input_param_dic['nburnin']
    nsteps = input_param_dic['nsteps']
    ndim = input_param_dic['ndim']
    nthreads = input_param_dic['nthreads']

    p0 = input_param_dic['p0']    
    x = LC_dic[wl_id].time # extract the times
    y = LC_dic[wl_id].flux # extract flux  
    yerr = LC_dic[wl_id].ferr # extract the flux error

    # add correct wavelength's t, y, yerr to the parameter dictionary
    input_param_dic['t'] = x 
    input_param_dic['y'] = y
    input_param_dic['yerr1'] = yerr

    # add auxiliary measurments to be used in GP kernel
    # TODO: check n_errors = aparam_num, and that len(aparam_list) == n_errors
    aparam_num = LC_dic[wl_id].param_num # extract the # of auxiliary measures
    aparam_name = LC_dic[wl_id].param_name # extract their names
    aparam_list = LC_dic[wl_id].param_list # extract a list of these parameters
    for i in range(input_param_dic['n_errors']):
        input_param_dic['yerr'+str(i+2)]= aparam_list[i]

    #initialize model
    model = TransitModel.TransitModel(**input_param_dic)
    transit_par_names = ["rp","u1","u2"]
    gp_hyper_par_names = ["a","sig2","g1","g2","g3","g4","g5", "g6"]

    # run mcmc beginning at users initial guess 
    LC_dic[wl_id].obj_mcmcGP = mcmc.MCMC(x, y, yerr, model.lnprob_mcmc, 
                                       transit_par_names, gp_hyper_par_names, 
                                       nwalkers, nthreads)
    pos = np.array([p0 + 1e-4*np.random.randn(ndim) for i in range(nwalkers)])

    for values in pos:
        plt.plot(x, model.sample_conditional(values, x, y, yerr))
    plt.plot(x, y,'ko')
    plt.show()

    LC_dic[wl_id].obj_chainGP = LC_dic[wl_id].obj_mcmcGP.run(pos, nburnin, nsteps)
    values = np.median(LC_dic[wl_id].obj_chainGP, axis=0)
    errors = np.std(LC_dic[wl_id].obj_chainGP, axis=0) 
    plt.plot(x, model.sample_conditional(values, x, y, yerr))
    plt.plot(x, y,'ko')
    plt.show()
    corner.corner(LC_dic[wl_id].obj_chainGP, labels=["rp","u1","u2","a","sig2","g1","g2","g3","g4","g5", "g6"], 
                       truths=input_param_dic["p0"])
    plt.show()
    
