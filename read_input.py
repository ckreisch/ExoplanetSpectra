from ast import literal_eval as read
import re

class read_input:


  def __init__(self, input_file):

    
    input_file = open(input_file)
    line = input_file.readlines()
    len_input_file = len(line)

    #Remove full line comments
    for i in range(len_input_file-1, -1, -1):
        if line[i].split()[0] == '#':
           del line[i]

    len_input_file = len(line)   

    params_name = ['transit_parameters', 'p0', 'priors', 'lc_path', 'mwalkers', 'nburnin', 'nsteps', 'nsteps', 'ndim', 'wave_bin_size']

    param_dic = {}

    for i in range(len_input_file):

        param_input = re.split('= |#', line[i])[1]
        param_input = param_input.split()
        len_param_input = len(param_input)
        param_elt = [None]*len_param_input
        if params_name[i] == 'lc_path':
             param_elt = param_input
        else:
             for j in range(len_param_input):
                 param_elt[j] = read(param_input[j])            
             
             
        param_dic[params_name[i]] = param_elt

    self.param_dic = param_dic

  def param_dic(self):

      return param_dic
    
    
    
  
