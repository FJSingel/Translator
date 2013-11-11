"""
Created on Nov 8, 2013
@author: Frank Singel
FJS52@case.edu
This module translates a series of spaces strings into CSVs
"""

import re
from sys import stdin

#Regex Strings
regexes = ["\d{7} ", 
			"([A-Z]+')?[A-Z]+(-[A-Z]+)? ", #Allows [Letters]'[Letters]-[Letters] Like LA'FAWN-DAH
			"([A-Z]+')?[A-Z]+(-[A-Z]+)? ",
			"[A-Z]* ", #Middle name does not get fancy punctuation
			"[a-z]+ ",
			"F13 ",
			"S[0-9]{2} "]
#Exit Codes
EXIT_FAILURE = False
EXIT_SUCCESS = True

def main(lines):
	'''
	Takes a list of lines as input.
	'''
	for line in lines:
		try:
			tokens = _tokenize_input(line)
			#Ensures entry has 7 values by adding blank where nickname should be
			if len(tokens) == 6:
				tokens.insert(3, " ")
			else:
				_len_seven_or_valueerror(tokens) #can raise ValueError
			_validate_tokens(tokens) #can raise Valueerror
		except ValueError:
			print "Data is empty or does not match. Exiting."
			return EXIT_FAILURE
		line = _format_output(tokens)
		print line
	return EXIT_SUCCESS

def _validate_tokens(tokens):
	'''
	Compares list of 7 tokens against a list of 7 regexes.
	Raise exception to be caught if a mismatch occurs
	'''
	assert(len(tokens)==7)
	_len_seven_or_valueerror(regexes)
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
	'''Form a line for printing without F13 with accurate capitalization.'''
	assert(len(tokens) != 0)
	for index in xrange(1,4):
		if tokens[index] != "": #skip nickname if not present
			tokens[index] = _format_name(tokens[index])
	tokens.remove("F13 ") #This is required to be in the tokens because validate_tokens is called prior
	line = "".join([token[:-1] + ',' for token in tokens])
	return line[:-1]

def _format_name(name):
	'''correctly capitalizes various names'''
	assert(len(name) != 0)
	result = name[0]
	prefixes = re.compile("Mc\Z|O'\Z|De\Z|D'\Z|Mac\Z|L'\Z")
	for char in name[1:]:
		if prefixes.match(result) != None: #if case to cap is found
			result += char
		else:
			result += char.lower()
	return result 

def _len_seven_or_valueerror(item):
	if len(item) != 7:
		print "List not of appropriate length"
		raise ValueError

if __name__ == '__main__':
	lines = stdin.xreadlines()
	main(lines)	