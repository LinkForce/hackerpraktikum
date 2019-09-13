Basic Exploitation (Aufgabe 2)

1. Crash both programs (seg fault) by overlong input data.

For the 32 bits version, any input with 266 characters or longer will crash the program.

For the 32 bits version, any input with 274 characters or longer will crash the program.

2. Explain why the program crashed on your input. Which is the vulnerable instruc-
tion in the program and what happens to the RIP (return instruction pointer)?
Draw the stack in ASCII art immediately before and after the crash.

The program crashed because the input given is bigger than the space reserved in the stack for a string,
so when we try to strcpy to that string, the RIP gets overwritten with the end of our input.

This is basically like

0x0000000
	SPACE RESERVED TO STRING
	.
	.
	.
	.
	.
0xNNNNNNN
0xNNNNNNN+1
	0x4543abc <-- this is the original RIP value

and after strcpy execution:

0x0000000
	0x41414141
	0x41414141
	0x41414141 <-- 'A's from the input string
	.
	.
	.
	0x41414141
0xNNNNNNN
0xNNNNNNN+1
	0x08048480 <-- injected RIP value


3. With your input data, manipulate the program flow of hack-me.32 in way that
function secret gets executed.

a) Determine the address of function secret in hack-me.32.

The address is 0x08048480, and I obtained it by just loading the binary on gdb and running 
	
	info address secret

b) Write a script that concatenates this address multiple times, such that the
RIP gets overwritten by it.

The script secret32.py contains a simple code that concatenates 268 x characters with the secret address 
at the end, on the exact size needed that the address ends up written into the return instruction pointer.

c) Inject the output of your script as input into hack-me.32, such that secret
gets executed.

You can run hack-me.32 with the script output with the following command:

	./hack-me.32 $(python secret32.py)


4. Repeat step 3 for hack-me.64.

a) Determine the address of function secret in hack-me.64.

The address is 0x4005e0, and I obtained it by just loading the binary on gdb and running 
	
	info address secret

b) Write a script that concatenates this address multiple times, such that the
RIP gets overwritten by it.

The script secret64.py contains a simple code that concatenates 280 x characters with the secret address 
at the end, on the exact size needed that the address ends up written into the return instruction pointer.

c) Inject the output of your script as input into hack-me.32, such that secret
gets executed.

You can run hack-me.32 with the script output with the following command:

	./hack-me.64 $(python secret64.py)