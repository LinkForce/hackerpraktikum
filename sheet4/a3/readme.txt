Flappy Hacks (Aufgabe 3)

Anti-Emulation:

1. Explain how the APK detects an emulator.

The app checks some predefined strings in the Model, Device, Product, Manufacturer and build fingerprint provided by the OS, trying to detect common emulator fingerprints in those strings. It also checks if there is a bluetooth adaptor available, probably expecting emulators to not 
have bluetooth adaptors. And it request permission to read some device infos like baterry status to check for real hardware.

2. Modify the APK to run inside emulators.

The APK FlappyHacksNoDetection.apk provided can run inside emulators without detecting it.

Reverse Engineering:

Describe this verification routine.

The cheats are verified comparing hashed strings (in md5 and sha1 hashes) on the code using a class hidden inside a png file, more specifically,
Flappy.png. The app decripts this file and use the methods inside it to check if the hashed string from the cheats input matches with some hash 
present in the code.

How many and which cheats exist?

There are 3 cheats found in the code. One of them just prints a success message to the user, but doesn't seen to affect the game. The second 
onde prints a hint: EwkaPB0GOyoVU1oWUDcXFzEMAghSVGAwWDZc and says to use this hint with the prior cheat to find the next one. The last cheat
makes the points stack in 1000 at each obstacle, instead of 1. I couldn't find the actual cheat codes (and I don't know if we are intented to
do so), because they were all hashed and I couldn't find the decription to any of them online. I also tried decrypting the cheat engine class 
but could not use any information from there to find the actual cheat codes as well. The hashed cheats present in the code are:

00f88d2a5ea817d15f6cb29184366840 (md5)

7e6fd9ca8c7e437208b5f91efb4a94c568586645345553a25f39c8ef19eae632 (SHA-256)

642385be53489dd39a9256a10a6627dd83e614dacf294de7b0719954a927aeb9 (SHA-256)