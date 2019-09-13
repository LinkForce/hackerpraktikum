import sys
from ecdsa import VerifyingKey, BadSignatureError, NIST256p
import ecdsa.util
import ecdsa.numbertheory
import hashlib

def readsig(sig):
	sig = bytearray(open(sig,"rb").read())

	lr = sig[3] #get length of r
	r =  long(''.join('{:02x}'.format(x) for x in sig[4:(4+int(lr))]),16) # read as long

	ls = sig[(4+int(lr)+1)] #get length of s
	s =  long(''.join('{:02x}'.format(x) for x in sig[(4+int(lr)+2):(4+int(lr)+2+ls)]),16) # read as long

	return r,s

def readmsgint(msg):
	return long((hashlib.sha1(open(msg,"r").read()).hexdigest()),16) #get long from sha1 hash hex

n = NIST256p.order

r1,s1 = readsig(sys.argv[1])
r2,s2 = readsig(sys.argv[2])

msg1 = readmsgint(sys.argv[3])
msg2 = readmsgint(sys.argv[4])

k = (((msg1-msg2) % n) * ecdsa.numbertheory.inverse_mod((s1-s2), n)) % n #k = (z-z')/(s-s')

privatekey = (((s1*k - msg1) % n) * ecdsa.numbertheory.inverse_mod(r1, n)) % n #PK = (sk-z)/r

print ecdsa.SigningKey.from_secret_exponent(privatekey, NIST256p).to_pem() #print key in pem format to stdout

