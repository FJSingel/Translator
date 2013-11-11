#from mock import patch
import unittest
import sys

import translator

class ExhaustiveTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_validate_tokens(self):
        #translator.sys.stdin = lambda _: '1234567 MCKINLEY NATHAN AWESOME nmc F13 S15'
        tokens = ["1234567 ",  "LA'LA'MCKINLEY-KUN ", "NATHAN ", "AWESOME ", "nmc ", "F13 ", "S15 "]
        self.assertRaises(ValueError, translator._validate_tokens, tokens)

    def test_end_to_end(self):
        sys.stdin = {"Let's try to break this.\nWoah."}
        #sys.stdin = open(input.txt)
        print translator.main()

if __name__ == '__main__':
    unittest.main()