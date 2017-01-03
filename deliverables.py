# Deliverables module to parse MCMC data into latex code
#import mcmc

#table of both trans and noise params for now
def latex_table(self,LC_dic,visualization):
        try:
            f = open("latex_tables_"+str(wavelength_id)+".txt", "a")
        except IOError:
            print "Cannot open file to write tables to."
            raise
        col_string = "c|"
        colhead_string = r"\colhead{Light Curve}"
        for i in np.arange(LC_dic[LC_dic.keys()[0]].obj_mcmc._all_params): #assumes each LC has the same params
            col_string = col_string + "c"
            colhead_string = colhead_string + r" & \colhead{"+i+"}"
        f.write(r"\begin{deluxetable*}{"+col_string+"}\n"\
                +r"\tablewidth{0pc}"+"\n")
        f.write(r"\tablecaption{Light Curve Constraints \label{tab:LC}}"+"\n")
        f.write(r"\tablehead{ "+colhead_string+" } \n")
        f.write(r"\startdata"+"\n")
        f.write(r"\hline \\[-1.5ex]"+"\n")
        for wavelength_id in LC_dic:
            LC_dic[wavelength_id].obj_chain
          Planck+BKP & $1.0$ & & $-0.65$ & $-1$ &  & $0.48$ & $0.96$ \\
               & $0.1$ & & $-0.50$ & $-0.98$ & & $0.33$ & $0.74$ \\
          +mpk+RSD & $1.0$ & & $-0.66$ &  $-1$ & & $0.41$ & $0.80$ \\
               & $0.1$ & & $-0.50$ & $-0.94$ & & $0.02$ & $0.46$
          \enddata
         \tablecomments{Parameter constraints. To do: compute best-fit with action=2 in cosmomc. Likestats best-fit not accurate.}
        \end{deluxetable*}


        try:
            f.close()
        except IOError:
            print "Could not close file for some reason."
            raise

if __name__ == "__main__":
    import sys
    if len(sys.argv)!=3:
        raise ValueError("Did not enter sufficient number of arguments to test"\
                        +" code. Only entered "+str(len(sys.argv)-1)+".\n"\
                        +"Run as python deliverables.py <arg1> <arg2>")
    latex_table(int(sys.argv[1]),int(sys.argv[2]))
