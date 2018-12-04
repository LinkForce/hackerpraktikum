Sandbox (Aufgabe 2)

The sandbox works by replacing some libc functions with modified versions that checks the whitelist file before file opens and reads,
and based on the whitelist, returns the file if allowed, or null if not allowed.

To build the sandbox, just run the make command.

The whitelist is just a list of files, with one file per line. I left some examples inside the whitelist file.

To use the sandbox, you can pass the LD_PRELOAD enviromnent variable to the program like this:

    LD_PRELOAD=./sandbox.so ./my_program

There are some ways that a program can escape this kind of sandbox.

1) You can compile your program using static libraries, so the program will not look for
the functions inside the sandbox, and use the functions that are compiled with it.

2) You can call syscalls directly instead of using the libc wrappers. LD_PRELOAD cannot hook syscalls, so it will have no effect.

3) Some libraries are capable of removing the LD_PRELOAD env by using unsetenv("LD_PRELOAD"), so if the application has access to a library
that has this capability, it can escape the sandbox.
