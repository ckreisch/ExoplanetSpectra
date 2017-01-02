import read_input #from read_input 
#import re
#from ast import literal_eval as read

input_file = read_input('input_file')
param_dic = input_file.param_dic

lc_path = param_dic['lc_path']
p0 = param_dic['p0']
priors = param_dic['priors']
ndim = param_dic['ndim']
params = param_dic['transit_parameters']

print lc_path
print p0
print priors
print ndim
print params
