import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import sys

import george
from george import kernels
import batman
import corner

import mcmc
import lc_class
from read_input import read_input
import TransitModel
#import deliverables

# routine for fitting one wl: -------------------------------------------------
def run_mcmc_single_wl(input_param_dic, LC_dic, wl_id):

    nwalkers = input_param_dic['nwalkers']
    nburnin = input_param_dic['nburnin']
    nsteps = input_param_dic['nsteps']
    ndim = input_param_dic['ndim']
    nthreads = input_param_dic['nthreads']
    transit_par_names = input_param_dic['transit_par_names']
    gp_hyper_par_names = input_param_dic['gp_hyper_par_names']

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
    for i in range(input_param_dic['n_errors']):  # add auxiliary parameter measures
        input_param_dic['yerr'+str(i+2)]= aparam_list[i]

    #initialize model
    model = TransitModel.TransitModel(**input_param_dic)

    # run mcmc beginning at users initial guess
    LC_dic[wl_id].obj_mcmcGP = mcmc.MCMC(x, y, yerr, model.lnprob_mcmc,
                                       transit_par_names, gp_hyper_par_names,
                                       nwalkers, nthreads)
    pos = np.array([p0 + 1e-4*np.random.randn(ndim) for i in range(nwalkers)])
    LC_dic[wl_id].obj_chainGP = LC_dic[wl_id].obj_mcmcGP.run(pos, nburnin, nsteps)

    values = np.median(LC_dic[wl_id].obj_chainGP, axis=0)
    errors = np.std(LC_dic[wl_id].obj_chainGP, axis=0)

    # print values, errors  # TO_DO: print this out more nicely


# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Read from user input file ----------------------------------------------------
    if len(sys.argv)!=2:
        raise ValueError("Run as python main_driver_beta.py <input_filename>")

    try:
        input_file = read_input(sys.argv[1])   # TO-DO: this should be command line argument
    except IOError:
        print "Input file is not in the same directory as driver program."+\
                " Move to same directory or change path."
        raise
    input_param_dic = input_file.param_dic
    # TO_DO: remove following for loop once we correct read_input.py ??
    for key in input_param_dic.keys():
        if len(input_param_dic[key]) == 1:
            input_param_dic[key]=input_param_dic[key][0]

    lc_path = input_param_dic['lc_path']
    wave_bin_size = input_param_dic['wave_bin_size']
    visualization = input_param_dic['visualization']
    confidence = input_param_dic['confidence']

    # Read in MPI flag from user input file ---------------------------------------
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
    LC = lc_class.LightCurve(lc_path, wave_bin_size)
    LC_dic = LC.LC_dic # dictionary of light curve for each wavelength

    # MPI sending different wavelength LCs to different nodes -----------------
    if mpi_flag == 'True':
        # initialize MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if comm.Get_size() > len(LC_dic) and rank == 0:
            print "number of processors assigned is more than number of " + \
                    "wavelengths."

        for i in range(0, len(LC_dic.keys())):
            if i % comm.Get_size() == rank and rank != 0:
                #below print statement needs to be edited. Units??
                print "now rank number: %i of processor: %s is processing channel centered on: %s microns" % (rank, MPI.Get_processor_name(), LC_dic.keys()[i])
                run_mcmc_single_wl(input_param_dic, LC_dic, LC_dic.keys()[i])

                # print LC_dic[LC_dic.keys()[i]].obj_chainGP
                print "now rank number: %i of processor: %s is sending result to rank 0."% (rank, MPI.Get_processor_name())
                comm.Send([LC_dic[LC_dic.keys()[i]].obj_chainGP, MPI.FLOAT], dest=0, tag=11)
                print "send finished from rank %i"%(rank)

        if rank == 0:
            for i in range(0, len(LC_dic.keys())):
                if i % comm.Get_size() == rank:
                    print "now rank number: %i of processor: %s is processing channel centered on: %s microns" % (rank, MPI.Get_processor_name(), LC_dic.keys()[i])
                    run_mcmc_single_wl(input_param_dic, LC_dic, LC_dic.keys()[i])

            for i in range(1, comm.Get_size()):
                print "now rank number: %i is receiving result from rank %i."% (rank, i)
                data = np.empty(np.shape(LC_dic[LC_dic.keys()[0]].obj_chainGP))
                comm.Recv([data, MPI.FLOAT], source=i, tag=11)
                print "receive finished."
                LC_dic[LC_dic.keys()[i]].obj_chainGP = data
                # print LC_dic[LC_dic.keys()[i]].obj_chainGP
                # print "len of LC_dic:",len(LC_dic[LC_dic.keys()[i]].obj_chainGP)
            print "now rank number: %i is reaching corner."%(rank)
            for wl_id in LC_dic.keys():
                print "wl_id:", wl_id
                print "LC_dic[wl_id].obj_chainGP: ", LC_dic[wl_id].obj_chainGP
                # corner.corner(LC_dic[wl_id].obj_chainGP,
                #     labels=input_param_dic['transit_par_names']+input_param_dic['gp_hyper_par_names'],
                #     truths=input_param_dic["p0"])
    else:
        print "no MPI. Will use single core to process all lightcurves."
        for wl_id in LC_dic.keys():

            #below print statement needs to be edited. Correct object attribute??? Units are microns
            print "now processing channel centered on: %s microns" % wl_id
            run_mcmc_single_wl(input_param_dic, LC_dic, wl_id)

    # TO-DO: debug deliverables
    #deliverables.latex_table("test_data", LC_dic, visualization, confidence)
    # TO-DO: add summary comparing expected values to the fit found by our routine
    # TO_DO: add heather's nice visualization and remove the loop below
    # KY comment: currently this part is not working when MPI is used.
        for wl_id in LC_dic.keys():
            corner.corner(LC_dic[wl_id].obj_chainGP,
                labels=input_param_dic['transit_par_names']+input_param_dic['gp_hyper_par_names'],
                truths=input_param_dic["p0"])
