import sys
from Crypto.PublicKey import RSA

#chinese remainder theorem
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
#modular multiplicative inverse 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

#finds integer component of n'th root of x, n being the public keys expoent
def invpow(x,n):
	high = 1
	while high ** n < x:
	    high *= 2
	low = high/2
	while low < high:
	    mid = (low + high) // 2
	    if low < mid and mid**n < x:
	        low = mid
	    elif high > mid and mid**n > x:
	        high = mid
	    else:
	        return mid
	return mid + 1

#read messages as bytes and converts it to long
def readMsg(msg):
	return long(''.join('{:02x}'.format(x) for x in bytearray(open(msg,"rb").read())),16)

#read public keys as base64 and converts it to long
def readPubKey(key):
	lines = open(key,"r").readlines()
	return long(RSA.importKey(''.join(lines).strip()).__getattr__('n'))

msg1 = readMsg(sys.argv[1])
msg2 = readMsg(sys.argv[2])
msg3 = readMsg(sys.argv[3])

key1 = readPubKey(sys.argv[4])
key2 = readPubKey(sys.argv[5])
key3 = readPubKey(sys.argv[6])

#execute the chinese remainder theorem to get the message
crt = chinese_remainder([key1,key2,key3],[msg1,msg2,msg3])

#finds the integer component, and decode final message
print str(hex(invpow(crt,3)))[2:-1].decode('hex')