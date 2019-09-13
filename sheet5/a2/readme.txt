HMAC Length Extension Attack (Aufgabe 2)

The HMAC for the new message:

	3a3a838b7615e68c2194d0551465b5d9de1b54aa5b65095b391a144f1e2e301f

the message is located at newmotd.txt.

This attack is possible by knowing the HASH Algorithm and that the HMAC is made in the format of 
HASH(k | m). Using this information, we can bruteforce the size of the key k and, by adding padding
to fill up the message to get it to the original size that it had when the HASH algorithm padded it,
along with the correct padding bytes. After that, as sha256 works by iterating over chunks and 
processing those chunks with the current processed previous chunk, by adding the padding, extending the
message beyond the padding and feeding the current known state of the hash to the algorithm, we can 
make it process the extended part as it was with the original text, because all the needed previous 
information, including the key, is already present in the current state of the hash.

The message always starts with H because of the padding. The padding of a SHA-256 hash is made by adding
a 1 followed by zero bytes and ends with a big endian hexadecimal that represents the size of the actual message in bits. The key used to hash the message is 20 characters long, and the original 
message is 373 characters long. That makes 393 characters. Each character is a byte, so 393 * 8 = 3144.
3144 in big endian hexadecial is 0x0c 0x48. But 0x48 is the same decimal code used to the char H on the 
ASCII table, so when the webpage prints the message, it recognizes this byte as a H character.