# Find the different unit test scripts and run them

from unit_test.test_gen_syn_dat import TestSynthData
from unit_test.test_mcmc import TestMCMC
from unit_test.testTransitModel import TestFunctions
from unit_test.test_lc_class import test_lc_class
from unit_test.test_read_input import test_read_input
import unittest

unittest.main()
