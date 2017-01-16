import os
import sys
import inspect
dir_current = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir_up = os.path.dirname(dir_current)
sys.path.append(dir_up)

import numpy as np
import unittest
from exospec.deliverables import latex_table
from argparse import Namespace

## @class TestLatex
# Class to test the creation of the latex tables.
class TestLatex(unittest.TestCase):
    ## Sets up a fake dictionary and object attributes for use with the
    # deliverables latex_table definition.
    # @returns LC_dic A fake light curve dictionary with fake chains stored.
    # @returns transit_params A list of fake transit parameter names.
    # @returns hyper_params A list of fake hyper parameter names.
    def SetUp(self):
        obj1 = Namespace()
        obj2 = Namespace()
        LC_dic = {'LC1': obj1, 'LC2': obj2}
        obj1.obj_chain = np.array([[25, 50, 75, 100], [1, 26, 51, 76]])
        obj2.obj_chain = np.array([[125, 150, 175, 200], [101, 126, 151, 176]])
        transit_params = ['trans1','trans2']
        hyper_params = ['hyp1','hyp2']
        return LC_dic, transit_params, hyper_params

    ## Tests that a file is created.
    def testWriteFile(self):
        LC_dic, transit_params, hyper_params = self.SetUp()
        latex_table(LC_dic,transit_params,hyper_params,False,95,"test_latex.txt")
        self.assertTrue(os.path.exists("test_latex.txt"))
        os.system("rm test_latex.txt")

    ## Tests that, in addition to the scaffolding of the latex table,
    # data are written to the file.
    def testNumPrints(self):
        LC_dic, transit_params, hyper_params = self.SetUp()
        latex_table(LC_dic,transit_params,hyper_params,False,95,"test_latex.txt")
        num_prints = sum(1 for line in open("test_latex.txt"))
        self.assertTrue(num_prints > 8)
        os.system("rm test_latex.txt")

    ## Tests that two tables are written to file if the user specifies that the
    # transit and hyper parameters should be in separate tables.
    def testSeparate(self):
        LC_dic, transit_params, hyper_params = self.SetUp()
        latex_table(LC_dic,transit_params,hyper_params,True,95,"test_latex.txt")
        f = open("test_latex.txt")
        num_tabs = 0
        for line in f:
            if line.find("begin") != -1 and line.find("begin") != 0:
                num_tabs = num_tabs + 1
        self.assertEqual(num_tabs,2)
        os.system("rm test_latex.txt")

if __name__ == '__main__':
    unittest.main()
