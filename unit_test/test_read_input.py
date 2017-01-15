import unittest
import os
from src_copy.read_input import read_input
from src_copy.read_input import EmptyFile
from src_copy.read_input import NoInput

class test_read_input(unittest.TestCase):

    def testEmptyFile1(self):

        os.system("> empty_file")
        with self.assertRaises(EmptyFile):
            input_file = read_input("empty_file")
        os.system("rm empty_file")

    def testEmptyFile2(self):

        os.system("> empty_file")
        os.system("echo '#'That is a comment > empty_file")
        with self.assertRaises(EmptyFile):
            input_file = read_input("empty_file")
        os.system("rm empty_file")

    def testIncorrectFormat(self):

        os.system("> incorrect_file1")
        os.system("echo '#'This is a comment > incorrect_file1")
        os.system("echo lc_path : 'lc_path' >> incorrect_file1")
        with self.assertRaises(IndexError):
            input_file = read_input("incorrect_file1")
        os.system("rm incorrect_file1")

    def testNoInput(self):

        os.system("> incorrect_file2")
        os.system("echo '#'This is a comment > incorrect_file2")
        os.system("echo lc_path = >> incorrect_file2")
        with self.assertRaises(NoInput):
            input_file = read_input("incorrect_file2")
        os.system("rm incorrect_file2")


if __name__ == "__main__":

    unittest.main()    
   


