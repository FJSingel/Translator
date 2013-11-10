"""
Created on Nov 8, 2013
@author: Frank Singel
FJS52@case.edu
This module translates a series of spaces strings into CSVs
"""

import re
import sys

#Regex Strings
regexes = ["\d\d\d\d\d\d\d", 
			"[A-Z]+",
			"[A-Z]+",
			"[A-Z]*",
			"[a-z]+",
			"F13",
			"S[0-9]{2}"]

def main():
	for line in sys.stdin:
		tokens = re.split("\s", line)
		#remove empty tokens
		tokens = filter(None, tokens)

		try:
			#Ensures entry has 7 values
			if len(tokens) == 6:
				tokens.insert(3, "")
			elif len(tokens) != 7:
				raise ValueError

			_validate_tokens(tokens)
		except ValueError:
			print "Data does not match."

	    #Form a line for printing
		line = "".join([token + ',' for token in tokens])
		print line[:-1]


def _validate_tokens(tokens):
	token_pairs = zip(regexes, tokens)
	for regex, token in token_pairs:
		if(re.match(regex, token) == None):
			raise ValueError

if __name__ == '__main__':
	main()

#Refactor this
# def check_tokens(self, tokens):
# 	if(len(tokens) != 6 or len(tokens) != 7):
# 		raise ValueError
# 	if(re.match(number, tokens[0]) == None):
# 		raise ValueError
# 	if(re.match(upper, tokens[1]) == None):
# 		raise ValueError
# 	if(re.match(upper, tokens[2]) == None):
# 		raise ValueError
# 	if(re.match(upper, tokens[3] == None)):
# 		has_middle = False
# 	else:
# 		has_middle = True
# 	if(has_middle):
# 		#Token should be the nickname
# 		pass
# 	else:
# 		#Token at 3 should be userID
# 		if(re.match(user, tokens[3] == None)):
# 			has_middle = False