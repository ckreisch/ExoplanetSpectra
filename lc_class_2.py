import numpy as np
import matplotlib.pyplot as plt
import math as m
from os import listdir

class LightCurve:

      def __init__(self, PathToLC, wave_bin_size):

               files_list = listdir(PathToLC)
               files_num = len(files_list)
               new_obj_num = files_num/wave_bin_size
               wave_number = [None]*files_num

               for i in range(files_num):
                   file_name = files_list[i].split('.')[0]
                   wave_number[i] = file_name.split('_')[2]

               LC_obj_dic = {}
               
               for i in range(files_num):
                   Path_to_file = '{}/{}'.format(PathToLC, files_list[i])
                   LC_obj_dic[wave_number[i]] = LightCurveData(Path_to_file)

               self.files_list = files_list
               self.files_num = files_num
               self.wave_number = wave_number
               self.LC_obj_dic = LC_obj_dic

      def LC_obj_dic(self):

               return LC_obj_dic

      def wave_number(self):

               return wave_number



class LightCurveData:

      def __init__(self, Path_to_file):
               lc_file = open(Path_to_file)
               line = lc_file.readlines()
               len_file = len(line)
                  
               time = np.zeros(len_file-1)
               flux = np.zeros(len_file-1)
               ferr = np.zeros(len_file-1)

               param_num = len(line[1].split())-3
               param_name = line[0].split()[5:]
               param_list = np.zeros((param_num, len_file-1))

               for i in range(1,len_file):
                   time[i-1] = line[i].split()[0]
                   flux[i-1] = line[i].split()[1]
                   ferr[i-1] = line[i].split()[2]
                   for j in range(param_num):
                       param_list[j][i-1] = line[i].split()[3 + j]

               self.len_file = len_file
               self.time = time
               self.flux = flux
               self.ferr = ferr
               self.param_num = param_num
               self.param_name = param_name
               self.param_list = param_list

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
