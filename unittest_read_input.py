import unittest
import os
from read_input import read_input
from read_input import EmptyFile
from read_input import NoInput
from read_input import WrongInput

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

    def testNoInput(self):

        os.system("> incorrect_file1")
        os.system("echo '#'This is a comment > incorrect_file1")
        os.system("echo lc_path = >> incorrect_file1")
        with self.assertRaises(NoInput):
            input_file = read_input("incorrect_file1")
        os.system("rm incorrect_file1")

    def testWrongInput(self):

        os.system("> incorrect_file2")
        os.system("echo '#'This is a comment > incorrect_file2")
        os.system("echo t0 = pikachu >> incorrect_file2")
        with self.assertRaises(WrongInput):
            input_file = read_input("incorrect_file2")
      #  os.system("rm incorrect_file2")


if __name__ == "__main__":

    unittest.main()    
   


