#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -z "$1" ]
  then
    echo "No port to listen provided"
    exit
fi

nc -l -p $1 -vvv

