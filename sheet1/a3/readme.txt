Before running the scripts, please run installDepencies.sh to install all dependencies needed by the tools.
All installDependencies.sh scripts are the same, so you just need to run one of them.

Spoofing (Aufgabe 3)

To spoof any incoming NTP packets of a target machine, changing the packet date to 2035,  you can run the script ntpspoof.py

Usage:
    sudo python ntpspoof.py target-machine-ip [gateway-ip]
Example:
    sudo python ntpspoof.py 192.168.1.164 192.168.1.1

If the gateway ip is not provided, the script will assume the gateway ip by changing the last octet of the ip to a one

Root is required for running this script because it uses iptables

Every script can be closed by the common interrupt signal Ctrl+C on the terminal


