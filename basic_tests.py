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

_not_empty_or_valueerror:  1
If      86

Total:              10
"""

from mock import patch
from StringIO import StringIO

from testify import *

import translator

#Constants for checking error handling
NO_MATCH = "Data is empty or does not match. Exiting.\n"
TOKEN_ERROR = "Error in token: "
NONSEVEN_LIST_ERROR = "List not of appropriate length\n"
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
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_validate_no_tokens(self, output):
        #Test If 49
        with assert_raises(AssertionError):
            translator._validate_tokens([])

    def test_mismatch(self, output):
        #Test If 53
        with assert_raises(AssertionError):
            translator._validate_tokens(["ERROR"])
        assert_equals("", output.getvalue())

    def test_tokenize_input(self, output):
        #Test for 62 with empty string
        assert_equals([], translator._tokenize_input(""))

    def test_format_output(self, output):
        #Test if 69
        assert_equal("1234567,McKinley,Nathan,nmc,S15",
            translator._format_output(["1234567 ", "MCKINLEY ", "NATHAN ", "nmc ", "F13 ", "S15 "]))

    def test_format_no_output(self, output):
        with assert_raises(AssertionError):
            translator._format_output([])
        assert_equals("", output.getvalue())

    def test_format_no_name(self, output):
        with assert_raises(AssertionError):
            translator._format_name("")
        assert_equals("", output.getvalue())

    def test_format_name_prefix(self, output):
        #test if 80
        assert_equals("McKinley", translator._format_name("MCKINLEY"))

    def test_len_seven_or_valueerror(self, output):
        with assert_raises(ValueError):
            translator._len_seven_or_valueerror(["","","","","",""])
        translator._len_seven_or_valueerror(["","","","","","",""])

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
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_missing_name(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 N n F13 S00"]))
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_no_id(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN F13 S15"]))
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_no_F13(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc S15"]))
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_no_SXX(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc F13"]))
        assert_equals(NONSEVEN_LIST_ERROR + NO_MATCH, output.getvalue())

    def test_prefixes(self, output):
        '''Tests legal prefixes of Mc, Mac, De, D', and L' '''
        raw =       ["MCKINLEY", "O'REILLEY", "MACDONALD", "DESHAUN", "D'MARQUIS", "L'HOPITAL"]
        processed = ["McKinley", "O'Reilley", "MacDonald", "DeShaun", "D'Marquis", "L'Hopital"]
        for pre, post in zip(raw, processed):
            assert_equals(post, translator._format_name(pre))

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

@patch('sys.stdout', new_callable=StringIO)
class BadData(TestCase):
    """
    Test some bad data
    """
    def test_bad_number(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234 MCKINLEY NATHAN nmc F13 S15"]))
        assert_equals(TOKEN_ERROR + "1234 \n" + NO_MATCH, output.getvalue())

    def test_bad_first(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY Nathan nmc F13 S15"]))
        assert_equals(TOKEN_ERROR + "Nathan \n" + NO_MATCH, output.getvalue())

    def test_bad_last(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 McKINLEY NATHAN nmc F13 S15"]))
        assert_equals(TOKEN_ERROR + "McKINLEY \n" + NO_MATCH, output.getvalue())

    def test_bad_nick(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN Awesome nmc F13 S15"]))
        assert_equals(TOKEN_ERROR + "Awesome \n" + NO_MATCH, output.getvalue())

    def test_bad_id(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nMc F13 S15"]))
        assert_equals(TOKEN_ERROR + "nMc \n" + NO_MATCH, output.getvalue())

    def test_bad_F13(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc f13 S15"]))
        assert_equals(TOKEN_ERROR + "f13 \n" + NO_MATCH, output.getvalue())

    def test_bad_SXX(self, output):
        assert_equals(EXIT_FAILURE, translator.main(["1234567 MCKINLEY NATHAN nmc F13 s15"]))
        assert_equals(TOKEN_ERROR + "s15 \n" + NO_MATCH, output.getvalue())

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

if __name__ == '__main__':
    run()