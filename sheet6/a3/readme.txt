Game Labrys (Aufgabe 3)

1. Cracking: You don’t want to pay for this game, so you decide to crack it.

a) Serial : Determine at least one valid license key by hand, analyzing the license
check algorithm.

The serial is composed of 5 groups of 5 characters from A-Z or from 0-9, each group separated by a -.

The first block is verified by doing a xor of each of the 5 chars and this xor should be 65, or A in ascii.

the second block is verified by doing the xor of the 3 first characters, and this should be the value of
the last character of the block.

The third block is verified by doing the AND of the first 4 characters, and this should be value of the
last character.

The fourth block is verified by doing the OR of the 3 odd positioned characters MOD 16, an thos should be 
value of the XOR of the 2 even positioned character.

The fifth block is verified if the first character is  the second -1 , the third characteris the 
fourth + 1, and the last has to be X.

From this, we can get that a valid key is:

	AAAAA-AAAAA-AAAAA-AB0CA-ABBAX

b) Keygen: Write a tool that creates you an arbitrary number of valid serial numbers.

The script keygen.py generates proceduraly a new valid key for every execution of it.

You can run it like this:

	python keygen.py

c) Patch: Modify the binary of the game such that it starts without requiring a
license key at all.

The binary labrys.32.crack is modified to start the game without checking for a license key. To achieve
this I just swapped the first instruction that checks if the file exists to a jump to the end of the code, 
when the code already passed on the key verification.

2. Cheating: You want to be better than your friends, so you start cheating.

a) Wallhack : Modify the game such that you can go through wall horizontally
(but do not fall through grounds or roofs vertically).

The binary labrys.32.wallhack contains a modified binary that makes the player go through walls.
To achieve this I modified the code when the objects check for horizontal colisions, so the walls never
detects horizontal colisions and the player can go through them.

b) Flyhack : Modify the game such that you are able to fly through all levels.

The binary labrys.32.flyhack contains a modified binary that makes the player fly.
To achieve this I modified the code to make the fly spell always active, by changing a jump on the 
save_state function that verifies if the fly spell is active, making it always return that the skill is active.

c) Speedhack : Modify the game to run quicker.

The binary labrys.32.speedhack contains a modified binary that makes the player run faster.
To achieve this I modified the code to make the run spell (horse) always active, by changing a jump on the 
save_state function that verifies if the horse spell is active, making it always return that the skill is active.

3. Exploitation: Share your own levels with frieds to hack into their computers.

a) Shellcode Injection: Edit level 5 such that shellcode is executed on the stack.
Note that ASLR is enabled, but not NX. That is, you can run your shellcode
on the stack but stack addresses are randomized.

The labyrinth file provided is crafted to inject shell code when you play level 5.

But, as the address are randomized, you have to try the code injection potentialy several times before 
getting it working. 
To do this, you can run the script shellinjection.sh provided and keep starting level 5 to load the code.

This script creates an environment variable with some shell code in it and a huge block of nops, to make a 
technique called NOP-Sleding. This env variable is loaded on the stack upon the game execution, and from
this, the file labyrinth contains a precise amount of character to overflow the buffer that reads it and 
write a new return value to the Return Instruction Pointer reg, and this value can, potentially, be
somewhere inside the nop block, and if it is, the code will slide through the nops and execute a shell code
to run a bash.

b) Return Oriented Programming: We additionally assume that Labrys was com-
piled with NX enabled. That is, you have to start shellcode without executable
stack. Use return-oriented programming.

You can generate the labyrinth file for this exercise by running the generaterop.py script like this:

	python generaterop.py > level5/labyrinth

The file has some comments explaning how I achieved the code injection and made the shell open.

After generating the crafted labyrinth file, just boot the game and start level 5.


Every exploit in this exercise was made based on the original 32 bits executable. So, for example, each 
hack is in its own individual file and the serial is needed for the game to run for every exercise except
for the cracked binary itself. Both of the code injection exploits were tested on the original unmodified
binary.