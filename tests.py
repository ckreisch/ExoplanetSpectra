# Program created to do systematic tests with Jenkins
# ! /usr/bin/env python
import unittest
import glob
import os
import pep8
import numpy as np


class TestStyle(unittest.TestCase):
    def fetch_pyfiles(self):
        """
        Fetch names of all python files in directory.
        """
        file_list = np.array([])
        for file in glob.glob("*.py"):
            file_list = np.append(file_list, file)
            # print file
        return file_list

    def test_pep8(self):
        """
        Test for pep8 style in .py files.
        """
        file_list = self.fetch_pyfiles()
        pep8style = pep8.StyleGuide(report=pep8.StandardReport)
        file_error = pep8style.check_files(file_list)

        self.assertEqual(file_error.total_errors, 0, "pep8 style violation.")

class TestIntegration(unittest.TestCase):
    def run_main_and_check_output(self):
        """
        so long as jenkins_test.ini jenkins_test_out and jenkins_test_lc are kept
        as they are, this test will show that main_driver is producing the expected
        outputs.
        """
        os.chdir("jenkins_test_out")
        os.system("rm *.png")
        os.chdir("../")
        os.system("python main_driver_beta.py jenkins_test.ini")
        os.chdir("jenkins_test_out")
        file_list = np.array([])
        for file in glob.glob("*"):
            file_list = np.append(file_list, file)

        expected_files = ["best_fit_500.0.png", "transmission_spectrum.png",
                          "best_fit_650.0.png" , "triangle_500.0.png",
                           "mcmc_chain_500.0.out", "triangle_650.0.png",
                          "mcmc_chain_650.0.out",  "walkers_500.0.png",
                          "simple_table.out",    "walkers_650.0.png"]

        flag = True
        k = 0
        if len(file_list) > 0:
            while flag and k < len(expected_files) :
                if expected_files[k] in file_list:
                    flag = True
                else:
                    flag = False
                k = k+1

        else: flag = False

        if flag:
            pass

if __name__ == '__main__':
    unittest.main()
