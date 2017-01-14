import matplotlib.pyplot as plt
import numpy as np

def plot_single_wavelength(wl_id, mcmc_obj, model, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, saving_dir=""):
    if wl_id=='500.0':
        theta_true_transit=[5.000000000000000278e-02, 4.500000000000000111e-01, 1.000000000000000056e-01]
    if wl_id=='650.0':
        theta_true_transit=[8.000000000000000167e-02, 5.500000000000000444e-01, 1.000000000000000056e-01]
    if wl_id=='800.0':
        theta_true_transit=[1.000000000000000056e-01, 4.500000000000000111e-01, 1.100000000000000006e-01]
    if wl_id=='950.0':
        theta_true_transit=[1.199999999999999956e-01, 3.499999999999999778e-01, 1.600000000000000033e-01]
    if wl_id=='1100.0':
        theta_true_transit=[1.499999999999999944e-01, 5.000000000000000000e-01, 1.000000000000000056e-01]
    print "producing plots for channel centered on: "+wl_id +" microns, acceptance fraction="+str(mcmc_obj.get_mean_acceptance_fraction())
    mcmc_obj.walker_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "walkers_"+str(wl_id)+".png")
    mcmc_obj.triangle_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "triangle_"+str(wl_id)+".png")
    mcmc_obj.light_curve_plot(model, extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "light_curve_"+str(wl_id)+".png")

    max_steps=[50,100, 150, 200]#[50, 100, 250, 500, 750, 1000]
    for m in max_steps:
        mcmc_obj.walker_plot(extra_burnin_steps, theta_true_transit, True, False, saving_dir, "walkers_"+str(wl_id)+"_transit_params_max"+str(m)+".png", m)
        mcmc_obj.triangle_plot(extra_burnin_steps, theta_true_transit, True, False, saving_dir, "triangle_"+str(wl_id)+"_transit_params_max"+str(m)+".png", m)


    mcmc_obj.walker_plot(extra_burnin_steps, theta_true_transit, True, False, saving_dir, "walkers_"+str(wl_id)+"_transit_params.png")
    mcmc_obj.triangle_plot(extra_burnin_steps, theta_true_transit, True, False, saving_dir, "triangle_"+str(wl_id)+"_transit_params.png")

    mcmc_obj.walker_plot(extra_burnin_steps, theta_true, False, True, saving_dir, "walkers_"+str(wl_id)+"_hyper_params.png")
    mcmc_obj.triangle_plot(extra_burnin_steps, theta_true, False, True, saving_dir, "triangle_"+str(wl_id)+"_hyper_params.png")


def plot_transmission_spec(LC_dic, saving_dir=""):
    #triangle plots, walker plots, lightcurve plots, transmission spectrum plots
    wavelengths=np.sort([float(x) for x in LC_dic.keys()])
    median_radius=[]
    err_plus_radius=[]
    err_minus_radius=[]
    for wl in wavelengths:
        flatchain=LC_dic[str(wl)].obj_chain
        #mcmc=LC_dic[str(wl)].obj_mcmc    #MCMC object for wavelength wl_id - not guaranteed to have if using MPI
        median, err_plus, err_minus=get_median_and_errors(flatchain) #mcmc.get_median_and_errors()   #don't use object, use chains
        median_radius.append(median[0])
        err_plus_radius.append(err_plus[0])
        err_minus_radius.append(err_minus[0])

    #print "wavelengths", wavelengths
    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(wavelengths, median_radius, yerr=[err_minus_radius, err_plus_radius], drawstyle = 'steps-mid', linewidth=3)
    ax.set_xlabel("wavelength", fontsize=20)
    ax.set_ylabel("radius", fontsize=20)
    ax.set_title("Transmission Spectrum", fontsize=20)
    #ax.set_xlim(425, 1175)
    plt.savefig(saving_dir+"transmission_spectrum.png")
    plt.close()

def get_median_and_errors(flatchain):
    ps=np.percentile(flatchain, [16, 50, 84],axis=0)
    median=ps[1]
    err_plus=ps[2]-ps[1]
    err_minus=ps[1]-ps[0]
    return median, err_plus, err_minus
