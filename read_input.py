from ast import literal_eval as read
import re
import numpy as np
from lc_class import LightCurve

class EmptyFile(Exception):
    """Raise when the input file is empty or only has comments"""
    pass

class NoInput(Exception):
    """Raise when no input is found for a parameter"""
    pass

class WrongInput(Exception):
    """Raise when the input for a parameters is not set correctly (mainly when the type is not as expected"""
    pass

class read_input:


  def __init__(self, input_file):

    # check the size of the iput file
    input_file = open(input_file)
    line = input_file.readlines()
    len_input_file = len(line)

    if len_input_file == 0:
        raise EmptyFile('The input file %s is empty!' % input_file)

    #Remove any comments
    for i in range(len_input_file-1, -1, -1):
        line[i] = line[i].partition('#')[0].rstrip()
        if line[i] == '':
            del line[i]

    len_input_file = len(line)

    if len_input_file == 0:
        raise EmptyFile('The input file %s only contains comments' % input_file)

    params_name = np.array([])
    param_dic = {}

    # extract the name and the input of the parameters from the input file
    for i in range(len_input_file):

        params_name = np.append(params_name,re.split('= |#', line[i])[0].rstrip())
        try:
            param_input = re.split('= |#', line[i])[1]
        except NoInput:
            print "Failure to set value for "+params_name[i]
            raise
        param_input = param_input.split()
        len_param_input = len(param_input)
#        if len_param_input==0:
 #           raise NoInput('Failure to set value for '+params_name[i])
        param_elt = [None]*len_param_input
        
        # the following parameters have string input and are treated differently than numbers inputs
        if params_name[i] == 'lc_path' or params_name[i] == 'mpi_flag' or params_name[i] == 'visualization' or params_name[i] == 'confidence' or params_name[i] == 'limb_dark':
             param_elt = param_input
        # the follwing parameters have numbers input
        else:
             for j in range(len_param_input):
                 try:
                     param_elt[j] = read(param_input[j])
                 except WrongInput:
                     print "Did not input value for "+params_name[i]+" correctly. Input is "+str(param_input[j])
                     raise

        # set the input element associated with the name of the parameter as the dictionary key
        param_dic[params_name[i]] = param_elt
    # This list all the possible transit parameters that the users might have written as input and that should be referenced by the transit_parameters key
    transit_param_names = ['t0', 'per', 'rp', 'a', 'inc', 'ecc', 'w', 'u0', 'u1', 'u2', 'u3']
    actual_transit_param = []
    for i in params_name:
        if i in transit_param_names:
            actual_transit_param.append(param_dic[i][0])

    # lump the transit parameters together in the dictionnary
    param_dic['transit_parameters'] = actual_transit_param

    # create a global dictionnary made of the light curve dictionnary and the parameters dictionnary
    light_curve = param_dic['lc_path'][0]
    wave_bin_size = param_dic['wave_bin_size'][0]
    LC_dic = LightCurve(light_curve, wave_bin_size).LC_dic
    global_dic = LC_dic
    global_dic.update(param_dic)


    self.param_dic = param_dic
    self.global_dic = global_dic

  def param_dic(self):

      return param_dic
