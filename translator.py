"""
Created on Nov 8, 2013
@author: Frank Singel
FJS52@case.edu
This module translates a series of spaces strings into CSVs
"""

import re
# import sys
from sys import stdin

#Regex Strings
regexes = ["\d{7} ", 
			"([A-Z]+')?[A-Z]+(-[A-Z]+)? ", #Allows [Letters]'[Letters]-[Letters] Like LA'FAWN-DAH
			"([A-Z]+')?[A-Z]+(-[A-Z]+)? ",
			"[A-Z]* ",
			"[a-z]+ ",
			"F13 ",
			"S[0-9]{2} "]

ERROR_FAILURE = -1


def main():

	for line in stdin.readlines():
		print line

		if line == None:
			raise ValueError

		tokens = re.split("\s", line)
		#remove empty tokens
		tokens = filter(None, tokens)
		tokens = [token + ' ' for token in tokens] #end each token with whitespace

		try:
			#Ensures entry has 7 values
			if len(tokens) == 6:
				tokens.insert(3, " ")
			elif len(tokens) != 7:
				raise ValueError
			_validate_tokens(tokens)
		except ValueError:
			print "Data does not match."
			return "Failure!"

	    #Form a line for printing without F13
		print tokens
		tokens.remove("F13 ")
		line = "".join([token[:-1] + ',' for token in tokens])
		print line[:-1]

		return tokens


def _validate_tokens(tokens):
	token_pairs = zip(regexes, tokens)
	for regex, token in token_pairs:
		if re.match(regex, token) == None:
			print "Error in token: |" + token + "|"
			raise ValueError

if __name__ == '__main__':
	main()