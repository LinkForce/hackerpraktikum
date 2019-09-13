ECDSA Fixed K (Aufgabe 4)

1. Use OpenSSL to read out the curve parameters. What are they?

The curve used is NIST256p (prime256v1 on OpenSSL parameters)

2. Compare the two signatures with a HEX-Editor. Which components are identical
and what follows from this?

The first 4 + 33 bytes hex values are the same, this means that the "r" part of the signatures are
the same, meaning that the same K value was used to sign both messages, and with this allowing us to
compute the private key by reverting some operations of the message signing.

3. Use the two signatures and the information from the public key to calculate the
private ECDSA key which has been used to create those signatures. Save the
calculated private key in PEM format and use exhaustive documentation.

The private keys is:

-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIN3Kex8uJS7CrU+6WH30YS03et8nHNMys0u0mvX+dbZAoAoGCCqGSM49
AwEHoUQDQgAEHTGYikaCJAYeT9d7rZEIO2Ak3FRwf2wNeKpL7lpJsSny/BKtZFEd
V/Rynkqi9MVTREGsAijvqUCuST6UCosrGw==
-----END EC PRIVATE KEY-----

To obtain the private key, you can run the calckey.py as follows:

	python calckey.py msg1.sig msg2.sig msg1.txt msg2.txt

The calculation uses the "s" part of the signatures to obtain the private key.
Because of the same K being used in both keys, that results on the same "r", we can calculate the K
using s - s' = k^-1 (z - z'), with z and z' being the SHA1 hash integer representation of the 2 messages
and s and s' the "s" part of the messages' signatures, respectively.

Reorganizing, we can find out that k = (z-z')/(s-s'), so we calculate K and apply modulus operation in 
every step with the curve order value.

After obtaining k, we can get from the signature generation algorithm that PK = (sk-z)/r. 
We already have s from the signature, the r part is the same from both signatures, z is the integer 
representation of the message, and we just calculated k, so with those infos we make this operation, 
apply the modulus with the curve order again and end up with the Private Key used to sign those messages.

4. Use the just calculated private key to sign a message of your choice. You should
now be able to verify this signature using the given public key (vk.pem)

And for this one, this readme file is signed with the private key and can be verified with vk.pem 
with the followin command:

	openssl dgst -sha1 -verify vk.pem -signature readme.sig readme.txt

(Maybe worth noticing that I could not run the commands like in the bash script provided, so I changed 
the -ecdsa-with-SHA1 part to -sha1)