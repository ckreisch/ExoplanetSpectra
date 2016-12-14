from lc_class import LightCurve

LC = LightCurve('light_curve', 1) # Instantiate the Light Curve class. This class will reads all the light curve files and create light curve objects for each of these files

LC_dic = LC.LC_obj_dic # Instantiate the LC dictionnary (this dic contains all the Light Curve objects and each of them is referred by its wavenumber)

wave_number = LC.wave_number # Extract the list of wavenumber
new_wave_number = LC.new_wave_number

LC_1 = LC_dic['1'] # Instantiate Ligt Curve object of wavenumber 1 using the LightCurve class dictionary

LC_1_flux = LC_1.flux # extract the flux from the Light Curve Object of wavenumber 1

print wave_number
print new_wave_number
print LC_1.flux

LC_1.plot_flux_time(5) # Plot the flux of light curve object of wavenumber 1 with a new time bin, here new time bin = 5 old time bins
