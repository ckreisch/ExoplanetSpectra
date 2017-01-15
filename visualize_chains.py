import matplotlib.pyplot as plt
import numpy as np

## Produces triangle, walker and lightcurve plots for the MCMC results for a single wavelength
# @param wl_id The wavelength being processed
# @param mcmc_obj An object of the MCMC class that has been run for the wavelength wl_id
# @param model A function that takes a set of parameters and produces plots of the transit's lightcurve
# @param extra_burnin_steps Number of steps (in addition to burnin_steps from run) at the start of each chain to neglect
# @param theta_true Numpy array of true parameter values if known (used for test data)
# @param plot_transit_params Boolean value specifying whether or not to plot the transit parameters
# @param plot_hyper_params Boolean value specifying whether or not to plot the hyper parameters
# @param save_as_dir Directory where plot should be saved. Default is current working Directory
def plot_single_wavelength(wl_id, mcmc_obj, model, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, saving_dir=""):
    print "producing plots for channel centered on: "+wl_id +" microns, acceptance fraction="+str(mcmc_obj.get_mean_acceptance_fraction())
    w=mcmc_obj.walker_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "walkers_"+str(wl_id)+".png")
    t=mcmc_obj.triangle_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "triangle_"+str(wl_id)+".png")
    l=mcmc_obj.light_curve_plot(model, extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "light_curve_"+str(wl_id)+".png")

## Produces a plot of the best-fit radius as a function of wavelengths
# @param LC_dic A lightcurve dictionary with a lightcurve object for each wavelengths
# @param save_as_dir Directory where plot should be saved. Default is current working Directory
def plot_transmission_spec(LC_dic, save_as_dir=""):
    #transmission spectrum plots from mcmc flatchain
    wavelengths=np.sort([float(x) for x in LC_dic.keys()])
    median_radius=[]
    err_plus_radius=[]
    err_minus_radius=[]
    for wl in wavelengths:
        flatchain=LC_dic[str(wl)].obj_chain
        median, err_plus, err_minus=get_median_and_errors(flatchain)
        median_radius.append(median[0])
        err_plus_radius.append(err_plus[0])
        err_minus_radius.append(err_minus[0])

    half_bin_1=(wavelengths[1]-wavelengths[0])/2
    half_bin_2=(wavelengths[-1]-wavelengths[-2])/2

    plt.close()
    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(wavelengths, median_radius, yerr=[err_minus_radius, err_plus_radius], drawstyle = 'steps-mid', color='blue', linewidth=2)
    ax.plot([wavelengths[0]-half_bin_1, wavelengths[0]],[median_radius[0], median_radius[0]], color='blue', linewidth=2)
    ax.plot([wavelengths[-1], wavelengths[-1]+half_bin_2], [median_radius[-1],median_radius[-1]], color='blue', linewidth=2)
    ax.set_xlabel("wavelength", fontsize=15)
    ax.set_ylabel("radius", fontsize=15)
    ax.set_title("Transmission Spectrum", fontsize=15)
    plt.savefig(save_as_dir+"transmission_spectrum.png")
    plt.close()

## Obtains the median parameter values and 1 sigma errors from the MCMC flatchain
# @param flatchain A 2D numpy array with all the samples for each of the transit and hyper parameters
def get_median_and_errors(flatchain):
    ps=np.percentile(flatchain, [16, 50, 84],axis=0)
    median=ps[1]
    err_plus=ps[2]-ps[1]
    err_minus=ps[1]-ps[0]
    return median, err_plus, err_minus
