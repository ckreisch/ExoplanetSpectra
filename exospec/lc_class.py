import numpy as np
import matplotlib.pyplot as plt
import math as m
from os import listdir
from ast import literal_eval as read


## @class EmptyFolder
# Raise exception when the light curve folder is empty
class EmptyFolder(Exception):
    pass
## @class IncorrectNameFormat
# Raise when the light curve file name is not under the expected format sample_lc_<wavelength>.txt
class IncorrectNameFormat(Exception):
    pass
## @class EmptyFile
# Raise when the light curve file is empty
class EmptyFile(Exception):
    pass
## @class DifferentFileSize
# Raise when one the light curve file does not have the same size with light curve file for the lowest wavelength (this file serves as reference)
class DifferentFileSizes(Exception):
    pass
## @class DifferentParamNum
# Raise when one the light curve file does not have the same number of parameters with light curve file for the lowest wavelength (this file serves as reference)
class DifferentParamNum(Exception):
    pass

## @class LightCurve
# List all the light curve files in the indicated folder
# if the user decided to use another wavelength resolution than the one provided with the files, the code compute the resulting number of new wavelength to be used
# loop over the light curve files to get their file names and original wavelengths
# if the user decided to use a new wavelength resolution, the code computes the new wavelength to be used
# instantiate the new lc objects (with new wave_bin_size)
# Warning: The code is not able yet to handle situation where files_num is not proportional to wave_bin_size
class LightCurve:
    # @param PathToLC The path to the directory which contains the light curve files
    # @param wave_bin_size The user defined new bin size for wavelengths
    def __init__(self, PathToLC, wave_bin_size):

        files_list = listdir(PathToLC)
        files_list.sort()
        files_num = len(files_list)
        if files_num == 0:
            raise EmptyFolder('No light curve files in indicated folder')

        new_obj_num = files_num/wave_bin_size
        wave_length = [None]*files_num
        new_wave_length = [0.0]*new_obj_num

        for i in range(files_num):
            file_name = files_list[i].split('.')[0]
            try:
                wave_length[i] = file_name.split('_')[2]
            except IndexError:
                print 'Light curve file name %s does not have the correct format\n Format should be <string>_<string>_<wavelength>' % file_name
                raise
            if wave_length[i].isdigit() == False:
                raise IncorrectNameFormat('Light curve file name %s does not have the correct format\n Format should be <string>_<string>_<wavelength>' % file_name)
        wave_length.sort()

        for i in range(new_obj_num):
            for j in range(wave_bin_size):
                new_wave_length[i] = new_wave_length[i]\
                                    + float(wave_length[i*wave_bin_size + j])/wave_bin_size
        new_wave_length = [str(x) for x in new_wave_length]
        new_wave_length.sort()

        LC_dic = {}

        Path_to_files = [None]*wave_bin_size
        for i in range(new_obj_num):
            for j in range(wave_bin_size):
                Path_to_files[j] = '{}/{}'.format(PathToLC, files_list[i*wave_bin_size + j])
            LC_dic[new_wave_length[i]] = LightCurveData(Path_to_files)

        self.files_list = files_list
        self.files_num = files_num
        self.wave_length = wave_length
        self.new_wave_length = new_wave_length
        self.LC_dic = LC_dic
        self.obj_mcmc = None
        self.obj_chain = None
        self.obj_mcmcGP = None
        self.obj_chainGP = None
        self.transit_model = None

    ## Return LC_dic
    # @returns LC_dic the dictionary that contains the light curve objects and which are references by their wavelength as keys 
    def LC_dic(self):

        return LC_dic
    ## Return wave_length
    # @returns wave_length a list containing the original wavelength of the ligth curve files
    def wave_length(self):

        return wave_length
    ## Return new_wave_length
    # @returns new_wave_length a list containing the new user defined wavelength of the ligth curve objects
    def new_wave_length(self):

        return new_wave_length
    ## Stores transit_model
    # @param transit_model
    def store_transit_model(self, transit_model):

        self.transit_model = transit_model

## @class LightCurveData
# this class is used by the class LightCurve to extract, store and process the data from the light curve files
# @param Path_to_files A list that contains the path(s) to the file(s) that will be used to create a light curve object (multiple files can be lumped together to create a ligh curve object)
class LightCurveData:

    def __init__(self, Path_to_files):

        # this counts the number of files specified per LC object. Typically, if the user decided to lump several light curve files together to change the wavelength resolution, file_num will be higher than one
        file_num = len(Path_to_files)

        #just sample the first file just to have info that are in common for all files
        f = open(Path_to_files[0])
        line = f.readlines()
        len_file = len(line)

        if len_file == 0:
            raise EmptyFile('Light curve file %s is empty' % Path_to_files[0])

        # Remove all the comments
        for i in range(len_file-1, -1, -1):
            if ('#' in line[i]) == True:
                del line[i]

        len_file = len(line)

        if len_file == 0:
            raise EmptyFile('Light curve file %s only contains comments' % Path_to_files[0])

       
        param_num = len(line[1].split())-3
        param_name = line[0].split()[4:]
        param_list = np.zeros((param_num, len_file-1))
        time = np.zeros(len_file-1)
        param_num = len(line[1].split())-3
        param_name = line[0].split()[5:]
        for i in range(1,len_file):
            time[i-1] = line[i].split()[0]

        flux = np.zeros((file_num, len_file-1))
        ferr = np.zeros((file_num, len_file-1))
        param_list = np.zeros((file_num, param_num, len_file))

        # loop over the number of light curve files to be lumped together to first extract their data
        for i in range(file_num):
            lc_file = open(Path_to_files[i])
            line_i = lc_file.readlines()
            len_i = len(line_i)

            if len_i == 0:
                raise EmptyFile('Light curve file %s is empty' % Path_to_files[i])

            # Remove all the comments
            for i in range(len_i-1, -1, -1):
                if ('#' in line_i[i]) == True:
                    del line_i[i]

            len_i = len(line_i)
            if len_i == 0:
                raise EmptyFile('Light curve file %s only contains comments' % Path_to_files[i])

            param_num_i = len(line_i[1].split())-3
            if len_i != len_file:
                raise DifferentFileSizes('File %s does not have the same size as file %s' % (Path_to_files[i], Path_to_files[0]))
            if param_num_i != param_num:
                raise DifferentParamNum('File %s does not have the same number of parameter as file %s' % (Path_to_files[i], Path_to_files[0]))
            for j in range(1, len_file):
                flux[i][j-1] = line_i[j].split()[1]
                ferr[i][j-1] = line_i[j].split()[2]
                for k in range(param_num):
                    param_list[i][k][j-1] = line_i[j].split()[3 + k]

        tot_flux = np.zeros(len_file-1)
        tot_ferr = np.zeros(len_file-1)

        # finally merge the data of the different light curve files to lump them together
        for i in range(len_file-1):
            for j in range(file_num):
                tot_flux[i] = tot_flux[i] + flux[j][i]
                tot_ferr[i] = tot_ferr[i] + ferr[j][i]
        av_param_list = np.zeros((param_num, len_file-1))
        for i in range(len_file-1):
            for j in range(param_num):
                for k in range(file_num):
                   av_param_list[j][i] = av_param_list[j][i] + param_list[k][j][i]/file_num

        self.len_file = len_file
        self.time = time
        self.flux = tot_flux
        self.ferr = tot_ferr
        self.param_num = param_num
        self.param_name = param_name
        self.param_list = av_param_list
    ## Returns len_file
    # @returns len_file the length of the light curve file
    def len_file(self):

        return self.len_file
    ## Return time
    # @returns time the time vector
    def time(self):

        return self.time
    ## Returns flux
    # @returns flux the flux vector
    def flux(self):

        return self.flux
    ## Returns ferr
    # @returns ferr the error on the flux
    def ferr(self):

        return self.ferr
    ## Returns param_num
    # @returns param_num the number of parameters defined in the light curve file
    def param_num(self):

        return self.param_num
    ## Returns param_name
    # @returns param_name a list containing the names of the parameters
    def param_name(self):

        return self.param_name
    ## Returns param_list
    # @returns param_list a list containing the parameters
    def param_list(self):

        return self.param_list

    ## Change the time resolution of a light curve object
    # enables the user to use a new time resolution
    # @param bin_size number of time points to lump together
    def new_time_bin(self, bin_size):

        time = self.time
        flux = self.flux
        new_size = int(m.ceil((self.len_file - 1)/bin_size))
        new_time = np.zeros(new_size)
        new_flux = np.zeros(new_size)
        for i in range(new_size):
            for j in range(bin_size):
                new_time[i] = new_time[i] + time[i*bin_size + j]/bin_size
                new_flux[i] = new_flux[i] + flux[i*bin_size + j]/bin_size

        return new_time, new_flux

    ## Plot the flux against the time
    # plot the flux with a new time resolution using function new_time_bin
    # @param bin_size number of time points to lump together
    def plot_flux_time(self, bin_size):

        if (bin_size == 1):
          plt.figure(0)
          time = self.time
          flux = self.flux
          plt.plot(time, flux)
          plt.show()
        else:
          plt.figure(0)
          new_time = self.new_time_bin(bin_size)[0]
          new_flux = self.new_time_bin(bin_size)[1]
          plt.plot(new_time, new_flux)
          plt.show()

    ## Plot the flux against a parameter
    # plot the flux againt the parameter indicated by the user
    # @param param_index the index of the param selected by the user in param_list
    def plot_flux_param(self, param_index):

        plt.figure(1)
        param = self.param_list[param_index]
        flux = self.flux
        plt.plot(param, flux)
        plt.show()