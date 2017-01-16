# Deliverables module to parse MCMC data into latex code
#import mcmc
import os
import sys
import inspect
dir_current = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_up = os.path.dirname(dir_current)
sys.path.append(dir_up)

import numpy as np
import unittest
import exospec.deliverables.latex_table as latex_table
from argparse import Namespace

class TestLatex(unittest.TestCase):
    def SetUp():
        obj1 = Namespace()
        obj2 = Namespace()
        LC_dic = {'LC1': obj1, 'LC2': obj2}
        obj1.obj_chain = np.array([[25, 50, 75, 100], [1, 26, 51, 76]])
        obj2.obj_chain = np.array([[125, 150, 175, 200], [101, 126, 151, 176]])
        transit_params = ['trans1','trans2']
        hyper_params = ['hyp1','hyp2']
        return LC_dic, transit_params, hyper_params

    def CleanUp(filename):
        os.system("rm " + filename)

    def testWriteFile():
        SetUp()
        latex_table(LC_dic,transit_params,hyper_params,False,95,"test_latex.txt")
        self.assertTrue(os.path.exists("test_latex.txt"))
        CleanUp("test_latex.txt")

    def testNumPrints():
        SetUp()
        latex_table(LC_dic,transit_params,hyper_params,False,95,"test_latex.txt")
        num_prints = sum(1 for line in open("test_latex.txt"))
        self.assertTrue(num_prints > 8)
        CleanUp("test_latex.txt")

    def testSeparate():
        SetUp()
        latex_table(LC_dic,transit_params,hyper_params,True,95,"test_latex.txt")
        f = open("input.txt")
        num_tabs = 0
        for line in f:
            if line.find("begin") != -1 and line.find("begin") != 0:
                num_tabs = num_tabs + 1
        self.assertEqual(num_tabs,2)
        CleanUp("test_latex.txt")

if __name__ == '__main__':
    unittest.main()
