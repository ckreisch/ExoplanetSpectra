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

if __name__ == '__main__':
    unittest.main()
