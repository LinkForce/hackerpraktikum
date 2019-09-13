Basic Reverse Engineering (Aufgabe 1)

1. What is the password for challenge 1?

Using the command string on any of the executables gives a list of strings, with one of them being
very suspicious. This string is p4ssw0rd, and is the password for challenge 1.

2. What is the password for challenge 2?

Using a decopiler, we can see that the password for this challenge is formed by the sum of 4 variables
printed on a string. Those variables values are 1000, 300, 30, 7, and the sum is 1337, and this is the
password for challenge 2.

What is the password for challenge 3? 

Using gdb to look through the code in assembly mode, you can step into the function checkHard and after
the loop, you can check the 2 registers that are loaded to the strcmp function. One of them contains the
string that you input to the program, the other contains the string zyvgjqpc. This string is calculated
by checkHard and is the password for challenge 3.