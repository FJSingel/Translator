"""
Created on Nov 8, 2013
@author: Frank Singel
FJS52@case.edu
This module translates a series of spaces strings into CSVs
"""

import re
import sys

#Regex Strings
number = "\d\d\d\d\d\d\d"
upper = "[A-Z]+"
user = "[a-z]+"
F13 = "F13"
S13 = "S13"

has_middle = False

for line in sys.stdin:
	tokens = re.split("\s", line)
	#remove empty tokens
	tokens = filter(None, tokens)

	try:
		validate_tokens(tokens)
	except ValueError:
		print "Data does not match."
	else:
		print "Unexpected error:", sys.exc_info()[0]
    	raise

#Refactor this
def check_tokens(self, tokens):
	if(len(tokens) != 6 or len(tokens) != 7):
		raise ValueError
	if(re.match(number, tokens[0]) == None):
		raise ValueError
	if(re.match(upper, tokens[1]) == None):
		raise ValueError
	if(re.match(upper, tokens[2]) == None):
		raise ValueError
	if(re.match(upper, tokens[3] == None)):
		has_middle = False
	else:
		has_middle = True
	if(has_middle):
		#Token should be the nickname
		pass
	else:
		#Token at 3 should be userID
		if(re.match(user, tokens[3] == None)):
			has_middle = False