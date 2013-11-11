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

EXIT_FAILURE = False
EXIT_SUCCESS = True

def main(lines):
	'''
	Takes a list of lines as input.
	'''

	for line in lines:
		tokens = _format_line(line)

		try:
			#Ensures entry has 7 values
			if len(tokens) == 6:
				tokens.insert(3, " ")
			elif len(tokens) != 7:
				raise ValueError
			_validate_tokens(tokens)
		except ValueError:
			print "Data does not match. Exiting."
			return EXIT_FAILURE

	    #Form a line for printing without F13
		tokens.remove("F13 ")
		line = "".join([token[:-1] + ',' for token in tokens])
		print line[:-1]
	return EXIT_SUCCESS

def _validate_tokens(tokens):
	token_pairs = zip(regexes, tokens)
	for regex, token in token_pairs:
		if re.match(regex, token) == None:
			print "Error in token: |" + token + "|"
			raise ValueError

def _format_line(line):
	tokens = re.split("\s", line)
	#remove empty tokens
	tokens = filter(None, tokens)
	return [token + ' ' for token in tokens] #end each token with whitespace

if __name__ == '__main__':
	lines = stdin.readlines()
	main(lines)