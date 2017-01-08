from lc_class import LightCurve

LC = LightCurve('lc_white_none_red_none', 1) # Instantiate the Light Curve class. This class will reads all the light curve files and create light curve objects for each of these files. The first argument is the folder containing the light curve files. The second argument is the wavelength bin size (2 means that the code lumps every two original wavelength together)

wave_length = LC.wave_length # Extract the list of original wavelength
new_wave_length = LC.new_wave_length # Extract the list of the new set of wavelength following the bin size change

LC_dic = LC.LC_dic # Instantiate the LC dictionnary (this dic contains all the Light Curve objects and each of them is referred by its wavelength)

wave_length = LC.wave_length # Extract the list of wavelength
new_wave_length = LC.new_wave_length

print LC_dic
LC_15 = LC_dic['950.0'] # Instantiate Ligt Curve object of wavelength 1.5 using the LightCurve class dictionary
LC_35 = LC_dic['1100.0'] # Instantiate Ligt Curve object of wavelength 3.5 using the LightCurve class dictionary

LC_15_flux = LC_15.flux # extract the flux from the Light Curve Object of wavelength 1.5
LC_15_ferr = LC_15.ferr
LC_15_time = LC_15.time

LC_15_param_num = LC_15.param_num # extract the length of parameters for the current set of light cuve files
LC_15_param_name = LC_15.param_name # extract their name
LC_15_param = LC_15.param_list # extract a list of these parameters


transit_model = [1, 2, 3]
LC.store_transit_model(transit_model)
print LC.transit_model

print wave_length
print new_wave_length
print LC_15_flux
print LC_15_ferr
print LC_15_time

print LC_15_param_num
print LC_15_param_name
print LC_15_param

LC_15.plot_flux_time(5) # Plot the flux of light curve object of wavelength 1.5 against time with a new time bin, here new time bin = 5 old time bins

LC_15.plot_flux_param(0) # Plot the flux of light curve object of wavelength 1.5 against parameters of index 0 (the first parameters in LC_15_param
