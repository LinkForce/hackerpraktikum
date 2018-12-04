Before running the scripts, please run installDepencies.sh to install all dependencies needed by the tools.
All installDependencies.sh scripts are the same, so you just need to run one of them.

Sniffing (Aufgabe 2)

The vulnerability is the Heartbleed vunerability, a bug in the OpenSLL cryptography library.

The server private key can be obtained running the script heartbleed.py

Usage:
    python heartbleed.py target-server-ip
Example:
    python heartbleed.py 10.0.23.19

After obtaining the key and decrypting the captured traffic, we get the following credentials:

Login:    d4rkh4xx0r
Password: Y0uW1llN3v3rG3tM3

Log-in to the provided URL and you can find a single email send from the user to the user himself.

To prevent the traffic being decripted, assuming that the the key is still not known by the
interceptor, you can change the SSL certificate from the server, thus getting a new private key that
does not work for decrypting the already captured traffic, and change the encryption approach to a Perfect Forward Secrecy, that creates a unique key for each session.

Every script can be closed by the common interrupt signal Ctrl+C on the terminal


