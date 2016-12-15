from lc_class import LightCurve

LC = LightCurve('light_curve', 2) # Instantiate the Light Curve class. This class will reads all the light curve files and create light curve objects for each of these files. The first argument is the folder containing the light curve files. The second argument is the wavenumber bin size (2 means that the code lumps every two original wavenumber together)

wave_number = LC.wave_number # Extract the list of original wavenumber
new_wave_number = LC.new_wave_number # Extract the list of the new set of wavenumber following the bin size change

LC_dic = LC.LC_dic # Instantiate the LC dictionnary (this dic contains all the Light Curve objects and each of them is referred by its wavenumber)

wave_number = LC.wave_number # Extract the list of wavenumber
new_wave_number = LC.new_wave_number

print LC_dic
LC_15 = LC_dic['1.5'] # Instantiate Ligt Curve object of wavenumber 1.5 using the LightCurve class dictionary
LC_35 = LC_dic['3.5'] # Instantiate Ligt Curve object of wavenumber 3.5 using the LightCurve class dictionary

LC_15_flux = LC_15.flux # extract the flux from the Light Curve Object of wavenumber 1.5
LC_15_ferr = LC_15.ferr
LC_15_time = LC_15.time

LC_15_param_num = LC_15.param_num # extract the number of parameters for the current set of light cuve files
LC_15_param_name = LC_15.param_name # extract their name
LC_15_param = LC_15.param_list # extract a list of these parameters



print wave_number
print new_wave_number
print LC_15_flux
print LC_15_ferr
print LC_15_time

print LC_15_param_num
print LC_15_param_name
print LC_15_param

LC_15.plot_flux_time(5) # Plot the flux of light curve object of wavenumber 1.5 against time with a new time bin, here new time bin = 5 old time bins

LC_15.plot_flux_param(0) # Plot the flux of light curve object of wavenumber 1.5 against parameters of index 0 (the first parameters in LC_15_param
