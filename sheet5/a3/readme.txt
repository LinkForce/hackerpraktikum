if there are unmet dependencies, just run pip install pycrypto

RSA Small Exponent (Aufgabe 3)

1. Use OpenSSL to examine the public keys and get the key parameters. What do
you see?

That the exponent of all keys are the same, 3. This allows us to execute a Hastad attack to decrypt
the message without the private key.

2. Use your findings to decrypt the message without knowing any private key.

The script hastad.py provided, when execute in the following manner:

	python hastad.py msg1.bin msg2.bin msg3.bin pk1.pem pk2.pem pk3.pem 

Uses the Hastad Broadcast Attack to decrypt the following message:

	The answer to life the universe and everything = 42

The Attack bases itself on the Chinese Remaider Theorem to compute the original message based on
modulus operations over the 3 encrypted messages. 