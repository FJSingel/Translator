"""
Unit tests for translator
Frank Singel

LINE NUMBERS ARE SUBJECT TO CHANGE!!!
Locations for structured basis testing
Main:               3
For     28
If      32
Elif    34

_validate_tokens:   2
For     52
If      53

_format_output:     1
If      69

_tokenize_input:    1
For     62

_format_name:       2
For     79
if      80

_assert_not_empty:  1
If      86

Total:              10
"""

#from mock import patch
from mock import patch
from StringIO import StringIO

from testify import *

import translator

NO_MATCH = "Data is empty or does not match. Exiting.\n"
TOKEN_ERROR = "Error in token: "
EXIT_SUCCESS = True
EXIT_FAILURE = False

@patch('sys.stdout', new_callable=StringIO)
class BasisTests(TestCase):
    """
    Tests all conditionals
    """
    def test_no_lines(self, output):
        #Test for 28, Boundary test
        assert_equals(EXIT_SUCCESS, translator.main([]))
        assert_equals("", output.getvalue())

    def test_six_tokens(self, output):
        #Test if 32, Bpundary test
        assert_equals(EXIT_SUCCESS, translator.main(["1234567 MCKINLEY NATHAN nmc F13 S15"]))
        assert_equals("1234567,McKinley,Nathan,,nmc,S15\n", output.getvalue())

    def test_five_tokens(self, output):
        #Test Elif 34
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY nmc F13 S15"]))
        assert_equals(NO_MATCH, output.getvalue())

    def test_validate_no_tokens(self, output):
        #Test If 49
        with assert_raises(ValueError):
            translator._validate_tokens([])

    def test_mismatch(self, output):
        #Test If 53
        with assert_raises(ValueError):
            translator._validate_tokens(["ERROR"])
        assert_equals(TOKEN_ERROR + "ERROR" +"\n", output.getvalue())

    def test_tokenize_input(self, output):
        #Test for 62
        assert_equals([], translator._tokenize_input(""))

    def test_format_output(self, output):
        #Test if 69
        assert_equal("1234567,McKinley,Nathan,nmc,S15",
            translator._format_output(["1234567 ", "MCKINLEY ", "NATHAN ", "nmc ", "F13 ", "S15 "]))

    def test_format_no_output(self, output):
        with assert_raises(ValueError):
            translator._format_output([])
        assert_equals("", output.getvalue())

    def test_format_no_name(self, output):
        with assert_raises(ValueError):
            translator._format_name("")
        assert_equals("", output.getvalue())

    def test_format_name_prefix(self, output):
        #test if 80
        assert_equals("McKinley", translator._format_name("MCKINLEY"))

    def test_assert_not_empty(self, output):
        with assert_raises(ValueError):
            translator._assert_not_empty("")

@patch('sys.stdout', new_callable=StringIO)
class BoundaryTests(TestCase):
    """
    Test for off-by-one errors: just above/below/on min
    Contains most of BadData tests
    """
    def test_min_input(self, output):
        assert_equals(EXIT_SUCCESS, translator.main(["0000000 M N n F13 S00"]))
        assert_equals("0000000,M,N,,n,S00\n", output.getvalue())

    def test_no_number(self, output):
        assert_equals(EXIT_FAILURE, translator.main([" MCKINLEY NATHAN nmc F13 S15"]))
        assert_equals(NO_MATCH, output.getvalue())

    def test_missing_name(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 N n F13 S00"]))
        assert_equals(NO_MATCH, output.getvalue())

    def test_no_id(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN F13 S15"]))
        assert_equals(NO_MATCH, output.getvalue())

    def test_no_F13(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc S15"]))
        assert_equals(NO_MATCH, output.getvalue())

    def test_no_SXX(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc F13"]))
        assert_equals(NO_MATCH, output.getvalue())

@patch('sys.stdout', new_callable=StringIO)
class DataFlow(TestCase):
    """
    Test as many if's as possible
    """
    @class_setup
    def setUp(self):
        self.input = ["1234567 MCKINLEY D'NA-THAN AWESOME nmc F13 S15", "2345678 GUTMAN CAMERON camg F13 S14"]
        self.output = "1234567,McKinley,D'Na-than,Awesome,nmc,S15\n2345678,Gutman,Cameron,,camg,S14\n"

    def test_multiple_lines(self, output):
        assert_equals(EXIT_SUCCESS, translator.main(self.input))
        assert_equals(self.output, output.getvalue())

class BadData(TestCase):
    """
    Test some bad data
    """
    def test_bad_number(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234 MCKINLEY NATHAN nmc F13 S15"]))
        assert_equals(NO_MATCH, output.getvalue())

    

@patch('sys.stdout', new_callable=StringIO)
class StressTest(TestCase):
    """
    Some stress testing
    """

    @suite('stress', reason="Time Intensive Stress Test not needed on every test run")
    def test_more_input(self, output):
        old = ["0009001 L"]
        new = "0009001,L"
        for x in xrange(1,100000):
            old[0] += "E"
            new += 'e'
        old[0] += "ROY JENKINS lrj F13 S15"
        new += "roy,Jenkins,,lrj,S15\n"
        assert_equals(EXIT_SUCCESS, translator.main(old))
        assert_equals(new, output.getvalue())

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