# Deliverables module to parse MCMC data into latex code and plots
import numpy as np
import mcmc
import matplotlib.pyplot as plt

#table of both trans and gp/noise params for now. Code visualization later.
def latex_table(LC_dic,visualization,confidence,filename):
        if visualization:
            print "Visualization of table has not been implemented yet. "\
                    +"This will be available in a future release."
        quantile = (100.-confidence)/2.
        try:
            f = open(filename, "w")
        except IOError:
            print "Cannot open file to write tables to."
            raise
        f.write("\n\n")
        col_string = "c|"
        colhead_string = r"\colhead{Light Curve}"
        for i in LC_dic[LC_dic.keys()[0]].obj_mcmc._all_params: #assumes each LC has the same params
            col_string = col_string + "c"
            colhead_string = colhead_string + r" & \colhead{"+i+"}"
        f.write(r"\begin{deluxetable*}{"+col_string+"}\n"\
                +r"\tablewidth{0pc}"+"\n")
        f.write(r"\tablecaption{Light Curve Constraints $\left("+str(confidence)+r"\%\,\mathrm{CL}\right)$\label{tab:LC}}"+"\n")
        f.write(r"\tablehead{ "+colhead_string+" } \n")
        f.write(r"\startdata"+"\n")

        for wavelength_id in LC_dic.keys():
            # Compute the quantiles.
            median_array = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
                             zip(*np.percentile(LC_dic[wavelength_id].obj_chain, [quantile, 50, 100.-quantile],
                                                axis=0)))
            up_array = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
                             zip(*np.percentile(LC_dic[wavelength_id].obj_chain, [quantile, 50, 100.-quantile],
                                                axis=1)))
            down_array = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
                             zip(*np.percentile(LC_dic[wavelength_id].obj_chain, [quantile, 50, 100.-quantile],
                                                axis=2)))
            #dic_median = {x: median_array[i] for (x,i) in zip(LC_dic[wavelength_id].obj_mcmc._all_params,np.arange(len(median_array)))}
            vals_string = str(LC_dic[wavelength_id].wave_length) + ""
            for i in np.arange(len(LC_dic[LC_dic.keys()[0]].obj_mcmc._all_params)):
                vals_string = vals_string + " & $"+str(median_array[i])+"^{+"+str(up_array[i])+"}_{-"+str(down_array[i])+"}$"
            if wavelength_id!=LC_dic.keys()[-1]:
                vals_string = vals_string + r" \\"
            f.write(vals_string+"\n")
        f.write(r"\enddata"+"\n")
        f.write(r"\tablecomments{Light curve parameter constraints.}"+"\n")
        f.write(r"\end{deluxetable*}")

        try:
            f.close()
        except IOError:
            print "Could not close file for some reason."
            raise

## Writes the best fit transit parameters from MCMC fit to an output file.
# Output file columns are: wavelength, radius of planet, first limb darkening
# parameter, second limb darkening parameter, followed by lower bound of 
# corresponding confidence intervals then upper bound of corresponding
# confidence intervals. Note that this currently only works for the quadratic 
# limb darkening model.
# @param LC_dic A light curve dictionary with finished chains stored.
# @param filename The name of the file to write the table in.
def simple_table(LC_dic, filename):

    try:
        ofile = open(filename, "w")
    except IOError:
        print "Cannot open file to write tables to."
        raise

    ofile.write("# wl rp u0 u1 rp_e1 u1_e1 u0_e1 rp_e2 u0_e2 u1_e2 \n")
    for wavelength_id in LC_dic.keys():
        ps=np.percentile(LC_dic[wavelength_id].obj_chain, [16, 50, 84], axis=0)
        medians=ps[1]
        err_plus=ps[2]-ps[1]
        err_minus=ps[1]-ps[0]
        ofile.write("%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (wavelength_id, medians[0],
            medians[1],medians[2], err_minus[0], err_minus[1], err_minus[2], err_plus[0],
            err_plus[1], err_plus[2]))
    try:
        ofile.close()
    except IOError:
        print "Could not close file for some reason."
        raise

## Produces triangle, walker and lightcurve plots for the MCMC results for a single wavelength
# @param wl_id The wavelength being processed
# @param mcmc_obj An object of the MCMC class that has been run for the wavelength wl_id
# @param model A function that takes a set of parameters and produces plots of the transit's lightcurve
# @param extra_burnin_steps Number of steps (in addition to burnin_steps from run) at the start of each chain to neglect
# @param theta_true Numpy array of true parameter values if known (used for test data)
# @param plot_transit_params Boolean value specifying whether or not to plot the transit parameters
# @param plot_hyper_params Boolean value specifying whether or not to plot the hyper parameters
# @param save_as_dir Directory where plot should be saved. Default is current working Directory
def plot_single_wavelength(wl_id, mcmc_obj, model, extra_burnin_steps=0, theta_true=None, plot_transit_params=True, plot_hyper_params=True, save_as_dir=""):
    print "producing plots for channel centered on: "+wl_id +" microns, acceptance fraction="+str(mcmc_obj.get_mean_acceptance_fraction())
    w=mcmc_obj.walker_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, save_as_dir, "walkers_"+str(wl_id)+".png")
    t=mcmc_obj.triangle_plot(extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, save_as_dir, "triangle_"+str(wl_id)+".png")
    l=mcmc_obj.light_curve_plot(model, extra_burnin_steps, theta_true, plot_transit_params, plot_hyper_params, save_as_dir, "light_curve_"+str(wl_id)+".png")

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
    ax.set_xlim(wavelengths[0]-half_bin_1, wavelengths[-1]+half_bin_2)
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


if __name__ == "__main__":
    import sys
    if len(sys.argv)!=5:
        raise ValueError("Did not enter correct number of arguments to test"\
                        +" code. You entered "+str(len(sys.argv)-1)+".\n"\
                        +"Run as python deliverables.py <LC dic> <vis> <conf> <name>")
    latex_table(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])
