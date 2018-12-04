#!/usr/bin/python

import sys
import socket
import requests
import ftplib
import string
import re
from ftpfingerprints import *

ip = sys.argv[1]

#test open port for a HTTPd sending a get request and looking at response
def httpdtest(ip,port):
    try:
        response = requests.get("http://{}:{}".format(ip,port))
        print "Port {} is httpd. Server info: {}".format(port,
                response.headers["Server"])
    except Exception as e:
        raise e

#test open port for a FTPd sending a HELP command and comparing with known server fingerprints
def ftpdtest(socket,ip,port):
    ftp = ftplib.FTP()
    ftp.connect(ip,port)

    try:
        helpstr = ftp.sendcmd("HELP")
    except ftplib.error_perm as e:
        helpstr = str(e)
        pass

    for f, v in ftp_fingerprints.iteritems():
        base = re.sub('\s+',' ', f).strip() #formating HELP response and dictinary known HELP for easier comparisson
        recv = re.sub('\s+',' ', helpstr).strip()
        if base == recv:
            print "Port {} is ftpd {}.".format(port, v)
            return

    #if none of the known fingerprint matches, assume it is py-ftpd
    print "port {} is ftpd py-ftpd".format(port)

for port in range(23,65535): #starting from 23 to skip 22 ssh port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if s.connect_ex((ip,port)) == 0:
        print "Port {} is open, checking for httpd".format(port)
        try:
            httpdtest(ip,port)
        except Exception as error:
            print "http request failed, testing as ftp"
            ftpdtest(s,ip,port)

        s.close()
        print
