CBC Malleability (Aufgabe 1)

1. Use the given information to transfer the amount of money to your account #31337
instead.

The script transfer1337.py provided generates the following base64 message:
	
	wUHhFdm5le/fLoF/G4U0u6FGSNVtkxFA3ZIEwYombzhGF2eYUCOusH3g2R56BtYlBd5FO/XlJkQ058Ev+8hTIA==

That when send to the provided server via telnet, transfers the $100000 amount to account #31337.

The message is manipulated by flipping the bits of the previous block that, when XORed with the bits of the last block that corresponds to the account, alters the
destination account to 31337. Flipping those bits destroy the previous block, but that block is just for the reason text, so it does not impact on the transfer.

Changing the message like this is possible because CBC Decryption XORs the previous ciphertext block with the result of the Block Cypher Decryption to generate the
next plaintext block, so you just have to make the inverse operations to find out what bits you should flip to change the transfer to the desired account.

2. Which basic cryptographic principle has been violated and why is AES-CBC not
suitable to guarantee authenticity? What would you use instead?

The concept of Integrity has been violated, as a message that is captured and modified is still acepted by the receiver end.
You could use a Propagating Cipher Block Chaining encryption, for example, so every block affects the blocks after, including the Initialization Vector, 
and with this you can't modify the messages as you do with CBC.