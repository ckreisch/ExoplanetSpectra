import matplotlib.pyplot as plt


def plot_all(LC_dic, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, saving_dir=""):
    #triangle plots, walker plots, lightcurve plots, transmission spectrum plots
    wavelengths=[float(x) for x in LC_dic.keys()]
    median_radius=[]
    err_plus_radius=[]
    err_minus_radius=[]
    for wl_id in LC_dic.keys():
        print "producing plots for channel centered on: %s microns" % wl_id
        mcmc=LC_dic[wl_id].obj_mcmc    #MCMC object for wavelength wl_id
        mcmc.walker_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "walkers_"+str(wl_id)+".png")
        mcmc.triangle_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "triangle_"+str(wl_id)+".png")
        #mcmc.light_curve_plot(LC_dic[wl_id].transit_model, extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, saving_dir, "light_curve_"+str(wl_id)+".png")

        median, err_plus, err_minus= mcmc.get_median_and_errors()

        median_radius.append(median[0])
        err_plus_radius.append(err_plus[0])
        err_minus_radius.append(err_minus[0])

    print "wavelengths", wavelengths
    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.errorbar(wavelengths, median_radius, yerr=[err_minus_radius, err_plus_radius], linestyle="none", marker="o")
    ax.set_xlabel("wavelength")
    ax.set_ylabel("radius")
    plt.savefig(saving_dir+"transmission_spectrum.png")
    plt.show()
    plt.close()
