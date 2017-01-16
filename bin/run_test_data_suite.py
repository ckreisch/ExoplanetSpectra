import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import os

import george
from george import kernels
import batman
import corner

import exospec
#import mcmc
#import lc_class
#from read_input import read_input
#import TransitModel
#import deliverables

# usage: python run_test_data_suite.py <list of test data input files> <list of output files> <file with table of expected values>

# import the table of expected values
print "reading expected value file: " + sys.argv[3]
wl, rp, u0, u1, w_scale, r_scale, = np.loadtxt(sys.argv[3], unpack=True)

# import the list of input files
print "importing list of input files to run from file: " + sys.argv[1]
input_file_list = open(sys.argv[1]).readlines()


# run main driver on them all
for filename in input_file_list:
	print "runnning main_driver_beta.py on :" + filename
    os.system("python main_driver_beta.py " + filename)

output_file_list = open(sys.argv[2]).readlines()
best_fits = []
for filename in output_file_list:
	best_fit = np.loadtxt(filename,unpack=True)
	best_fits.append(best_fits)  # columns are: wl[0] rp[1] u0[2] u1[3] rp_e1[4] u1_e1[5] u0_e1[6] rp_e2[7] u0_e2[8] u1_e2[9]
	# compare expected to fit:
	print "plotting transmission spectra"
	# over plot the transmission spectra (include error bars)
	plt.title("transmission spectra for " + filename)
	plt.plot(wl, rp, "ko", label="true")
	plt.plot(best_fits[0], best_fits[1], "bo", label="fit")
	plt.plot(best_fits[0], best_fits[1]+best_fits[4], 'bx', label="confidence interval")
	plt.plot(best_fits[0], best_fits[1]-best_fits[7], 'bx')
	plt.ylabel("radius of planet (units of stellar radii)")
	plt.xlabel("wavelength (microns)")


	print "plotting residuals"
	# residuals for rp u1 u2 as x y and color
	np.sort
	res_rp =
    res_u1 =
    res_u2 =
    plt.


best_fits = np.array(best_fits)
print "writing master table"
# table of residuals for all
