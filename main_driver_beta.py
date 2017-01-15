import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import sys
import os

import george
from george import kernels
import batman
import corner

import mcmc
import lc_class
from read_input import read_input
import TransitModel
import deliverables
import visualize_chains

# routine for fitting one wl: -------------------------------------------------
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
    # create an output folder if it does not exist... (whichever process is fastest will make it)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # always save the chain
    LC_dic[wl_id].obj_mcmc.save_chain(output_dir + "/"+'mcmc_chain_'+ wl_id+'.out')

    # if visualization is True save plots for this wavelength
    if input_param_dic['visualization']:
        print "visualization under developement\n"
        output_dir = input_param_dic['output_dir']
        visualize_chains.plot_single_wavelength(wl_id, LC_dic[wl_id].obj_mcmc, LC_dic[wl_id].transit_model.sample_conditional, extra_burnin_steps=0, theta_true=None,
            plot_transit_params=True, plot_hyper_params=True, saving_dir=output_dir)

        #deliverables.best_fit_plot(x, y, yerr, best_fit, output_dir, wl_id)

    return 0

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Read from user input file -----------------------------------------------
    if len(sys.argv)!=2:
        raise ValueError("Run as python main_driver_beta.py <input_filename>")

    try:
        input_file = read_input(sys.argv[1])
    except IOError:
        print "Input file is not in the same directory as driver program."+\
                " Move to same directory or change path."
        raise

    input_param_dic = input_file.param_dic

    # Read in MPI flag from user input file -----------------------------------
    mpi_flag = input_param_dic['mpi_flag']

    if mpi_flag == 'True':
        try:
            from mpi4py import MPI
        except ImportError:
            print "MPI not installed, but MPI flag set to True. Setting flag to" +\
                    "False and continuing."
            mpi_flag = 'False'
            pass

    # Reading in the data -----------------------------------------------------
    lc_path = input_param_dic['lc_path']  # directory where light curves are stored
    wave_bin_size = input_param_dic['wave_bin_size']  # if user wants to combine wavelength channels
    LC = lc_class.LightCurve(lc_path, wave_bin_size)
    LC_dic = LC.LC_dic # dictionary of light curve for each wavelength

    # MPI sending different wavelength LCs to different nodes -----------------
    if mpi_flag == 'True':
        # initialize MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if comm.Get_size() > len(LC_dic) and rank == 0:
            print "number of processors assigned is more than number of " + \
                    "lightcurves."

        # a parameter counting the rounds for message passing
        j = 0
        # decide the number of rounds for message passing
        if len(LC_dic) % comm.Get_size() == 0:
            jmax = len(LC_dic) / comm.Get_size()
        else:
            jmax = len(LC_dic) / comm.Get_size() + 1

        while j < jmax:
            for i in range(0, comm.Get_size()):
                if i % comm.Get_size() == rank and rank != 0 and i+j*comm.Get_size() < len(LC_dic):

                    print "now rank number: %i of processor: %s is processing channel centered on: %s microns" % (rank, MPI.Get_processor_name(), LC_dic.keys()[i+j*comm.Get_size()])
                    run_mcmc_single_wl(input_param_dic, LC_dic, LC_dic.keys()[i+j*comm.Get_size()])

                    # print "now rank number: %i of processor: %s is sending result to rank 0."% (rank, MPI.Get_processor_name())
                    comm.Send([LC_dic[LC_dic.keys()[i+j*comm.Get_size()]].obj_chain, MPI.FLOAT], dest=0, tag=11)
                    # print "send finished from rank %i"%(rank)

            if rank == 0:
                print "now rank number: %i of processor: %s is processing channel centered on: %s microns" % (rank, MPI.Get_processor_name(), LC_dic.keys()[j*comm.Get_size()])
                run_mcmc_single_wl(input_param_dic, LC_dic, LC_dic.keys()[j*comm.Get_size()])

                for i in range(1, comm.Get_size()):
                    if i+j*comm.Get_size() < len(LC_dic):
                        # print "now rank number: %i is receiving result from rank %i."% (rank, i)
                        chain = np.empty(np.shape(LC_dic[LC_dic.keys()[0]].obj_chain))
                        comm.Recv([chain, MPI.FLOAT], source=i, tag=11)
                        LC_dic[LC_dic.keys()[i+j*comm.Get_size()]].obj_chain = chain
                        # print "receive finished."


            j = j+1

        # master node processing plots
        if rank == 0:
            print "now rank number: %i is proceeding to post processing."%(rank)
            # To-Do: make sure this is working on cluster
            if input_param_dic['visualization']:
                # proceed with post-processing
                # TO-DO: debug deliverables
                output_dir = input_param_dic['output_dir'] + "/"
                confidence = input_param_dic['confidence']  # size of confidence interval to be included in table
                #deliverables.latex_table(LC_dic, True, confidence, output_dir + "/latex_table.out")
                deliverables.simple_table(LC_dic, output_dir + "simple_table.out")
                visualize_chains.plot_all(LC_dic, extra_burnin_steps=0, theta_true=None,
                    plot_transit_params=True, plot_hyper_params=True, saving_dir=output_dir)
    else:
        print "no MPI. Will use single core to process all lightcurves."
        for wl_id in LC_dic.keys():
            print "now processing channel centered on: %s microns" % wl_id
            run_mcmc_single_wl(input_param_dic, LC_dic, wl_id)

        if input_param_dic['visualization']:
            # proceed with post-processing inside this if statement
            # TO-DO: debug deliverables
            output_dir = input_param_dic['output_dir'] + "/"
            confidence = input_param_dic['confidence']  # size of confidence interval to be included in table
            #deliverables.latex_table(LC_dic, True, confidence, output_dir + "/latex_table.out")
            deliverables.simple_table(LC_dic, output_dir + "simple_table.out")

            #visualize_chains.plot_all(LC_dic, extra_burnin_steps=0, theta_true=None,
            #    plot_transit_params=True, plot_hyper_params=True, saving_dir=output_dir)
            visualize_chains.plot_transmission_spec(LC_dic, saving_dir=output_dir)



    # KY comment: it's good not to put code outside the above if-else structure.
    # Otherwise this part will be run multiple times when executing using mpirun.
