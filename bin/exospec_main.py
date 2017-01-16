import sys
import numpy as np

import exospec
from exospec.read_input import read_input
import exospec.fitting_single_lc as fsl
#import lc_class
#from read_input import read_input
#import deliverables
#import fitting_single_lc as fsl

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Read from user input file -----------------------------------------------
    if len(sys.argv) != 2:
        raise ValueError("Run as python exospec_main.py <input_filename>")

    try:
        input_file = read_input(sys.argv[1])
    except IOError:
        print "Input file is not in the same directory as driver program." + \
                " Move to same directory or change path."
        raise

    input_param_dic = input_file.param_dic

    # Read in MPI flag from user input file -----------------------------------
    mpi_flag = input_param_dic['mpi_flag']

    if mpi_flag == 'True':
        try:
            from mpi4py import MPI
        except ImportError:
            print "MPI not installed, but MPI flag set to True. Setting" +\
                    "flag to False and continuing."
            mpi_flag = 'False'
            pass

    # Reading in the data -----------------------------------------------------
    # directory where light curves are stored
    lc_path = input_param_dic['lc_path']

    # if user wants to combine wavelength channels
    wave_bin_size = input_param_dic['wave_bin_size']
    LC = exospec.lc_class.LightCurve(lc_path, wave_bin_size)

    # dictionary of light curve for each wavelength
    LC_dic = LC.LC_dic

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
                if (i % comm.Get_size() == rank and
                        rank != 0 and i+j*comm.Get_size() < len(LC_dic)):
                    print "now rank number: %i of processor: %s" % (
                        rank, MPI.Get_processor_name()) + \
                     "is processing channel centered on: %s microns" % (
                        LC_dic.keys()[j*comm.Get_size()])
                    fsl.run_mcmc_single_wl(
                        input_param_dic, LC_dic,
                        LC_dic.keys()[i+j*comm.Get_size()])
                    comm.Send(
                        [LC_dic[LC_dic.keys()[i+j*comm.Get_size()]].obj_chain,
                            MPI.FLOAT], dest=0, tag=11)

                    # print "send finished from rank %i"%(rank)

            if rank == 0:
                print "now rank number: %i of processor: %s" % (
                    rank, MPI.Get_processor_name()) + \
                 "is processing channel centered on: %s microns" % (
                    LC_dic.keys()[j*comm.Get_size()])
                fsl.run_mcmc_single_wl(
                    input_param_dic, LC_dic, LC_dic.keys()[j*comm.Get_size()])

                for i in range(1, comm.Get_size()):
                    if i+j*comm.Get_size() < len(LC_dic):
                        chain = np.empty(
                            np.shape(LC_dic[LC_dic.keys()[0]].obj_chain))
                        comm.Recv(
                            [chain, MPI.FLOAT], source=i, tag=11)
                        LC_dic[LC_dic.keys()[i+j*comm.Get_size()]].obj_chain =\
                        chain
                        # print "receive finished."
            j = j+1

        # master node processing plots
        if rank == 0:
            print "now rank number: %i is proceeding to post processing." % (
                rank)
            if input_param_dic['visualization']:
                # proceed with post-processing inside this if statement
                exospec.deliverables.post_processing_all_wl(input_param_dic, LC_dic)

    else:
        print "no MPI. Will use single core to process all lightcurves."
        for wl_id in LC_dic.keys():
            print "now processing channel centered on: %s microns" % wl_id
            fsl.run_mcmc_single_wl(input_param_dic, LC_dic, wl_id)

        if input_param_dic['visualization']:
            # proceed with post-processing inside this if statement
            exospec.deliverables.post_processing_all_wl(input_param_dic, LC_dic)

    # KY comment: it's good not to put code outside the above if-else
    # structure.
    # Otherwise this part will be run multiple times when executing using
    # mpirun.
