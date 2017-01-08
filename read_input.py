from ast import literal_eval as read
import re
import numpy as np
from lc_class import LightCurve

class NoInput(Exception):
    """Raise when no input is found for a parameter"""
    pass

class WrongInput(Exception):
    """Raise when the input for a parameters is not set correctly (mainly when the type is not as expected"""
    pass

class read_input:


  def __init__(self, input_file):


    input_file = open(input_file)
    line = input_file.readlines()
    len_input_file = len(line)

    #Remove any comments
    for i in range(len_input_file-1, -1, -1):
        line[i] = line[i].partition('#')[0].rstrip()
        if line[i] == '':
            del line[i]

    len_input_file = len(line)

    params_name = np.array([])
    #['transit_parameters', 'p0', 'priors', 'lc_path', 'mwalkers', 'nburnin', 'nsteps', 'nsteps', 'ndim', 'wave_bin_size']
    param_dic = {}

    for i in range(len_input_file):

        params_name = np.append(params_name,re.split('= |#', line[i])[0].rstrip())
        param_input = re.split('= |#', line[i])[1]
        param_input = param_input.split()
        len_param_input = len(param_input)
        if len_param_input==0:
            raise NoInput('Failure to set value for '+params_name[i])
        param_elt = [None]*len_param_input
        if params_name[i] == 'lc_path' or params_name[i] == 'mpi_flag' or params_name[i] == 'visualization' or params_name[i] == 'confidence' or params_name[i] == 'limb_dark':
             param_elt = param_input
        else:
             for j in range(len_param_input):
                 #put in try except block for if they messed up input type like this
                 #try:
                 #     test = int(param_input[j])
                 #except TypeError:
                #     print "Did not input value for "+params_name[i]+" correctly. Input is "+str(param_input[j])
                 try:
                     param_elt[j] = read(param_input[j])
                 except WrongInput:
                     print "Did not input value for "+params_name[i]+" correctly. Input is "+str(param_input[j])
                     raise


        param_dic[params_name[i]] = param_elt

    transit_param_names = ['t0', 'per', 'rp', 'a', 'inc', 'ecc', 'w', 'u0', 'u1', 'u2', 'u3'] # This list all the possible transit parameters that the users might have written as input and that should be referenced by the transit_parameters key
    actual_transit_param = []
    for i in params_name:
        if i in transit_param_names:
            actual_transit_param.append(param_dic[i][0])
            
    #param_dic['transit_parameters'] = [param_dic['t0'][0],param_dic['per'][0],\
    #                                    param_dic['rp'][0],param_dic['a'][0],\
    #                                    param_dic['inc'][0],param_dic['ecc'][0]\
    #                                   ,param_dic['w'][0],param_dic['u0'][0],\
    #                                   param_dic['u1'][0],param_dic['u2'][0],\
    #                                    param_dic['u3'][0]]

    param_dic['transit_parameters'] = actual_transit_param

    light_curve = param_dic['lc_path'][0]
    wave_bin_size = param_dic['wave_bin_size'][0]
    LC_dic = LightCurve(light_curve, wave_bin_size).LC_dic

    global_dic = LC_dic
    global_dic.update(param_dic)


    self.param_dic = param_dic
    self.global_dic = global_dic

  def param_dic(self):

      return param_dic
