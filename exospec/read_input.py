from ast import literal_eval as read
import re
import numpy as np
from lc_class import LightCurve

## @class EmptyFile
# Raise exception when the input file is empty or only has comments
class EmptyFile(Exception):
    pass
## @class NoInput
# Raise exception when the input entry is not properly set
class NoInput(Exception):
    pass

## @class read_input
# reads the input file and stores the input entries
class read_input:

  # @param input_file path to the input file
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

        params_name = np.append(params_name,re.split('=|#', line[i])[0].rstrip())
        try:
            param_input = re.split('=|#', line[i])[1]
        # This exception handling does not work and I have no ideas why
        except IndexError:
            print "The input for %s is not correctly set" % params_name[i]
            raise

        param_input = param_input.split()
        len_param_input = len(param_input)
        if len_param_input == 0:
            raise NoInput('Looks like you forgot to write an input for %s' %params_name[i])

        # if the input is a single entry
        if len_param_input == 1:
            if param_input[0].isdigit() or self.is_float(param_input[0]) == True:
                param_elt = read(param_input[0])
            else:
                param_elt = param_input[0]

        # if the input is multiple entries
        else:
            param_elt = [None]*len_param_input
            for j in range(len_param_input):
                if param_input[j].isdigit() or self.is_float(param_input[0]) == True:
                    param_elt[j] = read(param_input[j])
                else:
                    param_elt[j] = param_input[j]

        param_dic[params_name[i]] = param_elt

    self.param_dic = param_dic
  ## Returns the parameters dictionary
  # @returns param_dic the parameters dictionary
  def param_dic(self):

        return param_dic
  ## Check if the string contains a float
  def is_float(self, string):

        try:
            float(string)
            return True
        except ValueError:
            return False