#!/usr/bin/env python

import base64
import sys

if __name__ == '__main__':
	try:
		base = "wUHhFdm5le/fLoF/G4U0u6FGSNVtkxFA3ZIEwYombzhGF2eYUCOutHTg0h16BtYlBd5FO/XlJkQ058Ev+8hTIA==" #base message
		plaintext = "TRANSFER AMOUNT $1000000 REASON Salary Jan. 2016 DEST #78384 END" #plaintext of this message
		enc = base64.b64decode(base)

		i=0

		enlist = list(enc)

		for c in "31337": #for each char of the account number
			prexor =  ord(plaintext[55 + i]) ^ ord(enlist[39 + i]) #xor the char in the plaintext with the cyphered char on the previous block

			final = prexor ^ ord(c) # xor the result of the last operation with the desired 
									# value to get the bits that should be in the cyphered text to obtain the result

			enlist[39 + i] = chr(final)

			i = i + 1
			
		print base64.b64encode("".join(enlist)) #returns the base64 encoded message

	except:
		print sys.exc_info()[0]