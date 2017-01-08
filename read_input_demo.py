from read_input import read_input #
#import re
#from ast import literal_eval as read

try:
    input_file = read_input('test_suite_input_file.txt')
except IOError:
    print "Input file is not in the same directory as driver program."+\
            " Move to same directory or change path."
    raise
param_dic = input_file.param_dic
global_dic = input_file.global_dic

lc_path = param_dic['lc_path']
p0 = param_dic['p0']
ndim = param_dic['ndim']
params = param_dic['transit_parameters']



print param_dic
print global_dic
print lc_path
print p0
print ndim
print params
