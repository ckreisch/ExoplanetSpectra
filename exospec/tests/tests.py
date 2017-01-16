# Program created to do systematic tests with Jenkins
# ! /usr/bin/env python
import unittest
import glob
import fnmatch
import os
import pep8
import numpy as np

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.output_dir = "jenkins_test_data/jenkins_test_out"
        self.input_file_path = "jenkins_test_data/jenkins_test.ini"
        self.output_to_test_dir = "../../"
        self.expected_files = ["light_curve_500.0.png", "transmission_spectrum.png",
                          "light_curve_650.0.png" , "triangle_500.0.png",
                           "mcmc_chain_500.0.out", "triangle_650.0.png",
                          "mcmc_chain_650.0.out",  "walkers_500.0.png",
                          "simple_table.out",    "walkers_650.0.png",
                          "latex_table.txt"]
        os.chdir(self.output_dir)
        # remove any previous test outputs
        for filename in self.expected_files:
            os.system("rm "+filename)
        os.chdir(self.output_to_test_dir)
        os.system("python ../../bin/exospec_main.py " + self.input_file_path) # run main_driver

    def testOutput_names(self):
        """
        this test needs to be run from the same directory as jenkins_test_data/.
        it assumes that the test script is in exospec/tests while the main driver is
        in bin/ and bin/ and exospec/ are in same level
        so long as jenkins_test.ini jenkins_test_out and jenkins_test_lc are kept
        as they are, this test will show that main_driver is producing the expected
        outputs. as main driver is editted to contain different visualization output, checks
        can be added.
        """

        os.chdir(self.output_dir) 

        file_list = np.array([])      # get list of output files
        for file in glob.glob("*"):
            file_list = np.append(file_list, file)

        flag = True
        k = 0
        if len(file_list) > 0:   # compare output file names to expected file names
            while flag and k < len(self.expected_files) :
                if self.expected_files[k] in file_list:
                    flag = True
                    os.system("rm "+ self.expected_files[k])
                else:
                    flag = False
                k = k+1

        else: flag = False

        os.chdir(self.output_to_test_dir)

        if flag:
            pass

    def check_chain_shapes(self):
        """

        """

if __name__ == '__main__':
    unittest.main()
