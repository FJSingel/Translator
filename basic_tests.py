#from mock import patch
from mock import patch
from StringIO import StringIO

from testify import *

import translator

class BasisTests(TestCase):
    """
    Tests all conditionals
    """
    @class_setup
    def setUp(self):
        self.input = ["1234567 MCKINLEY NATHAN AWESOME nmc F13 S15"]
        self.output = "1234567,MCKINLEY,NATHAN,AWESOME,nmc,S15\n"

class DataFlow(TestCase):
    """
    Test some dataflow cases
    """

    pass

class BoundaryTests(TestCase):
    """
    Test some boundary data
    """
    pass

class GoodData(TestCase):
    """
    Test some nominal data
    """
    @class_setup
    def setUp(self):
        self.input = ["1234567 MCKINLEY D'NA-THAN AWESOME nmc F13 S15", "2345678 GUTMAN CAMERON camg F13 S14"]
        self.output = "1234567,McKinley,D'Na-than,Awesome,nmc,S15\n2345678,Gutman,Cameron,,camg,S14\n"

    @patch('sys.stdout', new_callable=StringIO)
    def test_multiple_lines(self, output):
        assert_equals(True, translator.main(self.input))
        assert_equals(self.output, output.getvalue())

class BadData(TestCase):
    """
    Test some bad data
    """
    pass

class StressTest(TestCase):
    """
    Some stress testing
    """
    @suite('stress', reason="Time Intensive Stress Test not needed on every test run")
    def test_more_input(self):
        pass

class ErrorGuessing(TestCase):
    """
    Guessing errors here
    """
    pass

'''
TODO
test empty lines
makefile
'''
# class ExhaustiveTests(unittest.TestCase):

#     def setUp(self):
#         pass

#     def test_validate_tokens(self):
#         #translator.sys.stdin = lambda _: '1234567 MCKINLEY NATHAN AWESOME nmc F13 S15'
#         tokens = ["1234567 ",  "LA'LA'MCKINLEY-KUN ", "NATHAN ", "AWESOME ", "nmc ", "F13 ", "S15 "]
#         self.assertRaises(ValueError, translator._validate_tokens, tokens)

#     def test_end_to_end(self):
#         sys.stdin = {"Let's try to break this.\nWoah."}
#         #sys.stdin = open(input.txt)
#         print translator.main()

if __name__ == '__main__':
    run()