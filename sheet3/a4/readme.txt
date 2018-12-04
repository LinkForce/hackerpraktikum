Rootkit (Aufgabe 4)

The rootkit can be installed using the install.sh provided like this:

    sudo ./install.sh program_to_be_hidden
    please run as root

This will build the rootkit (so it's not needed to make it before), install,
configure it to run on boot with the provided program name that should be hidden
from applications and start it.
Have in mind that the rootkit hides itself from too, so it will not show on lsmod.

I would like to note that I had some problems with kernel versions while writing this
rootkit. It should run just fine in any ubuntu-based distro using a kernel < 4.17, but
sometimes I got a bug on dmesg while trying to read the syscalltable.

Anyway hope this works just fine on your tests.
