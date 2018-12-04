Before running the scripts, please run installDepencies.sh to install all dependencies needed by the tools.
All installDependencies.sh scripts are the same, so you just need to run one of them.

Denial of Service (Aufgabe 4)

To test a server for its maximum amount of open connections, you can run the script ddos.py

Usage:
    python ddos.py target-server-ip [number-of-threads]
Example
    python ddos.py target-server-ip 150

If the number of threads is not provided, the script will fall back to a default value of 300 threads

The script will print the number of active connections to the server periodically until it stabilizes in the maximum amount


Every script can be closed by the common interrupt signal Ctrl+C on the terminal


