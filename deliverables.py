# Deliverables module to parse MCMC data into latex code
import numpy as np

#table of both trans and gp/noise params for now. Code visualization later.
def latex_table(LC_dic,visualization,confidence,filename):
        if visualization:
            print "Visualization of table has not been implemented yet. "\
                    +"This will be available in a future release."
        quantile = (100.-confidence)/2.
        try:
            f = open("latex_tables_"+filename+".txt", "a")
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

if __name__ == "__main__":
    import sys
    if len(sys.argv)!=5:
        raise ValueError("Did not enter correct number of arguments to test"\
                        +" code. You entered "+str(len(sys.argv)-1)+".\n"\
                        +"Run as python deliverables.py <LC dic> <vis> <conf> <name>")
    latex_table(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])