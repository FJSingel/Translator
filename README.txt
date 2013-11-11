Frank Singel
README for translator.py

Testing Methodology
-------------------

Error Handling Strategy
-----------------------

Input will be read line by line using stdio.xreadline.
A try, except is opened to catch Value Errors from validation.
Input is then tokenized in the barrier, where errors
are checked for, and if found, a ValueError will be raised.
This ValueError will be caught, and error message will be written out,
and main() will return a failure value. In this barrier, we call several
helper methods that raise ValueErrors if the input isn't clean.
These ValueErrors are also caught in the barrier.
Everything after the _validate_tokens() call in main is past the barrier.
Now that we can assume input to be clean, we format the data for output.
The line is now output cleanly.
This loops for each line, and each line has to pass the barrier.

Checklist:
-This protects itself from bad user info
-Assertions exist to help document assumptions in each method
-Assert is used only for cases that should never happen
-This catches Valueerrors that this code throws
-This code favors error handling
-There is a barricade to handle errors
-Testify and Mock was used to debug this
-Testify doesn't bother code running
-Defensive code amount seems reasonable
-Code termination in error states have been checked
---
-Use exceptions to flag improper input before returning a failure code
-I've replaced what would be unhandled exceptions with assertions in helper methods
-Exceptions are handled within the same module
-No constructors or destructors to have exceptions in
-All Exceptions have appropriate output messages
-No empty catch/except blocks
---
-Uses xreadline for reading input
-All exceptions are caught
-Error messages aren't too detailed


/*
Submit a separate text file to document the error handling 
architecture that you will follow in your implementation.

The architecture document should describe your error
handling choices such as a strategy for handling
erroneous user input, decisions on local or
global error handling, error propagation through the code,
presence and location of a barricade, and the other factors
in the defensive programming checklist at the end of chapter 8.
*/
