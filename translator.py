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
			"[A-Z]* ", #Middle name does not get fancy punctuation
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
		try:
			tokens = _tokenize_input(line)
			#Ensures entry has 7 values
			if len(tokens) == 6:
				tokens.insert(3, " ")
			elif len(tokens) != 7:
				raise ValueError
			_validate_tokens(tokens)
		except ValueError:
			print "Data is empty or does not match. Exiting."
			return EXIT_FAILURE
		line = _format_output(tokens)
		print line
	return EXIT_SUCCESS

def _validate_tokens(tokens):
	'''
	Compares list of tokens against a list of regexes.
	Raise exception to be caught if a mismatch
	'''
	_assert_not_empty(tokens)
	token_pairs = zip(regexes, tokens)
	for regex, token in token_pairs:
		if re.match(regex, token) == None:
			print "Error in token: " + token
			raise ValueError
	return EXIT_SUCCESS

def _tokenize_input(line):
	'''Tokenizes a line for processing'''
	tokens = re.split("\s", line)
	tokens = filter(None, tokens) #remove empty tokens
	return [token + ' ' for token in tokens] #end each token with whitespace

def _format_output(tokens):
	'''Form a line for printing without F13 with accurate capitalization'''
	_assert_not_empty(tokens)
	for index in xrange(1,4):
		if tokens[index] != "": #skip nickname if not present
			tokens[index] = _format_name(tokens[index])
	tokens.remove("F13 ")
	line = "".join([token[:-1] + ',' for token in tokens])
	return line[:-1]

def _format_name(name):
	'''correctly capitalizes various names'''
	_assert_not_empty(name)
	result = name[0]
	prefixes = re.compile("Mc\Z|O'\Z|De\Z|D'\Z|Mac\Z")
	for char in name[1:]:
		if prefixes.match(result) != None: #if case to cap is found
			result += char
		else:
			result += char.lower()
	return result 

def _assert_not_empty(item):
	if len(item) == 0:
		raise ValueError

if __name__ == '__main__':
	lines = stdin.xreadlines()
	main(lines)