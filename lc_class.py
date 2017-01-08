import numpy as np
import matplotlib.pyplot as plt
import math as m
from os import listdir
from ast import literal_eval as read

# The following are some definition of user-defined exception class

class EmptyFolder(Exception):
    """Raise when the light curve folder is empty"""
    pass

class IncorrectNameFormat(Exception):
    """Raise when the light curve file name is not under the expected format sample_lc_<wavelength>.txt"""
    pass

class EmptyFile(Exception):
    """Raise when the light curve file is empty"""
    pass

class DifferentFileSizes(Exception):
    """Raise when one the light curve file does not have the same size with light curve file for the lowest wavelength (this file serves as reference)"""
    pass

class DifferentParamNum(Exception):
    """Raise when one the light curve file does not have the same number of parameters with light curve file for the lowest wavelength (this file serves as reference)"""
    pass

class LightCurve:

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
            wave_length[i] = file_name.split('_')[2]
            if wave_length[i].isdigit() == False:
                raise IncorrectNameFormat('Light curve file name %s does not have the correct format' % file_name)
        wave_length.sort()

        # The code is not able yet to handle situation where files_num is not proportional to wave_bin_size
        for i in range(new_obj_num):
            for j in range(wave_bin_size):
                new_wave_length[i] = new_wave_length[i]\
                                     + float(wave_length[i*wave_bin_size + j])/wave_bin_size
        new_wave_length = [str(x) for x in new_wave_length]
        new_wave_length.sort()

        LC_dic = {}

        # Instantiate the new lc objects (with new wave_bin_size)
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

    def LC_dic(self):

        return LC_dic

    def wave_length(self):

        return wave_length

    def new_wave_length(self):

        return new_wave_length


class LightCurveData:

    def __init__(self, Path_to_files):

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

    def len_file(self):

        return self.len_file

    def time(self):

        return self.time

    def flux(self):

        return self.flux

    def ferr(self):

        return self.ferr

    def param_num(self):

        return self.param_num

    def param_name(self):

        return self.param_name

    def param_list(self):

        return self.param_list

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


    def plot_flux_param(self, param_index):

        plt.figure(1)
        param = self.param_list[param_index]
        flux = self.flux
        plt.plot(param, flux)
        plt.show()
