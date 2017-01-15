import unittest
import os
from os import listdir
from src_copy.lc_class import LightCurve
from src_copy.lc_class import EmptyFolder
from src_copy.lc_class import IncorrectNameFormat
from src_copy.lc_class import EmptyFile
from src_copy.lc_class import DifferentFileSizes

class test_lc_class(unittest.TestCase):

    def testEmptyFolder(self):  

        os.system("mkdir empty_folder")
        with self.assertRaises(EmptyFolder):
            LC = LightCurve('empty_folder', 1)
        os.system("rmdir empty_folder")

    def testIncorrectNameFormat1(self):
        
        os.system("mkdir folder_with_problems")
        os.system("> folder_with_problems/bad_file_name")
        with self.assertRaises(IncorrectNameFormat):
            LC = LightCurve('folder_with_problems', 1)
        os.system("rm -r folder_with_problems")

    def testIncorrectNameFormat2(self):

        os.system("mkdir folder_with_problems")
        os.system("> folder_with_problems/sample_lc_wavelength.txt")
        with self.assertRaises(IncorrectNameFormat):
            LC = LightCurve('folder_with_problems', 1)
        os.system("rm -r folder_with_problems")

    def testEmptyFile(self):

        os.system("mkdir folder_with_problems")
        os.system("> folder_with_problems/sample_lc_432.txt")
        with self.assertRaises(EmptyFile):
            LC = LightCurve('folder_with_problems', 1)
        os.system("rm -r folder_with_problems")

    def testDifferentFileSizes(self):

        os.system("cp -R light_curve folder_with_problems2")
        files_list = listdir('folder_with_problems2')
        files_list.sort()
        path_to_file = 'folder_with_problems2/{}'.format(files_list[1])
        f = open(path_to_file)
        lines = f.readlines()
        f.close()
        g = open(path_to_file, 'w')
        g.writelines([line for line in lines[:-1]])
        g.close()
        with self.assertRaises(DifferentFileSizes):
            LC = LightCurve('folder_with_problems2', 1)
        os.system("rm -r folder_with_problems2")
   

if __name__ == "__main__":

    unittest.main()
