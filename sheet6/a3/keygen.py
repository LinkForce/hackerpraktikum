#!/usr/bin/env python

import random

chars = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def checkinrange(val):
	if (val >= 48 and val <= 57 ) or (val >= 65 and val <= 90):
		return True
	return False

#first set of chars from the serial key
#the xor of all the characters must be 65, or the char 'A'
def firstblock():
	binaries = [0x00,0x00,0x00,0x00,0x00] #placeholder for creating the block

	vtx = random.choice([1,3,5]) #choose a odd number of values to flip the desired bits that should be 1 at the end

	#flip the bit
	for x in xrange(0,vtx):
		binaries[x] = binaries[x] ^ 0x41

	#flip the remaining values to number range	
	for x in xrange(vtx,5):
		binaries[x] = binaries[x] ^ 0x30

	random.shuffle(binaries)

	init = 0x10

	#randonly flip bits in pairs while keeping the values in the serial key chars range
	for x in range(4,-1,-1):
		vtx = random.choice([0,2,4])

		for z in range(0,vtx,2):
			newvalue = binaries[z] ^ init
			newvalue2 = binaries[z+1] ^ init

			if (not checkinrange(newvalue)) or (not checkinrange(newvalue2)):
				continue

			binaries[z] = newvalue
			binaries[z+1] = newvalue2

		init = init >> 1
		random.shuffle(binaries)

	xor=0

	for x in binaries:
		xor = xor ^ x

	#print xor

	return ''.join(chr(x) for x in binaries)

#second set of chars from the serial key
#the xor of the first 3 characters must be value of the last character
def secondblock():
	binaries = [0x00,0x00,0x00,0x00,0x00] #placeholder for creating the block

	if random.choice([ True, False ]): #randonly decides if the values will be numbers or letters
		#case letter
		for x in xrange(0,3):
			binaries[x] = binaries[x] ^ 0x41

		if random.choice([ True, False ]): #now randomly decides if value is P or higher
			for x in xrange(0,3):
				binaries[x] = binaries[x] ^ 0x10
	else:
		for x in xrange(0,3):
			binaries[x] = binaries[x] ^ 0x30


	#for each of the 3 values
	for x in xrange(0,3):
		init = 0x10
		#randonly flips bits in the value
		for z in range(4,-1,-1):
			if random.choice([ True, False ]) and checkinrange(binaries[z] ^ init):
				binaries[z] = binaries[z] ^ init
			init = init >> 1

	binaries[3] = ord(random.choice(chars)) # pick any random value for the 4th char
	binaries[4] = binaries[0] ^ binaries[1] ^ binaries[2] #combine the 3 first into the last one
	
	#print binaries

	return ''.join(chr(x) for x in binaries)

#third set of chars from the serial key
#the AND of the first 4 characters must be value of the last character
def thirdblock():
	binaries = [0x00,0x00,0x00,0x00,0x00] #placeholder for creating the block

	if random.choice([ True, False ]): #randonly decides if the values will be numbers or letters
		#case letter
		for x in xrange(0,4):
			binaries[x] = binaries[x] ^ 0x41
			if random.choice([ True, False ]): #now randomly decides if value is P or higher
				binaries[x] = binaries[x] ^ 0x10		
	else:
		for x in xrange(0,4):
			binaries[x] = binaries[x] ^ 0x30

	#print binaries

	#randonly flips bits in the value
	init = 0x1

	for z in range(0,5):
		#for each of the 4 values
		for x in xrange(0,4):
			if random.choice([ True, False ]) and checkinrange(binaries[x] ^ init):
				binaries[x] = binaries[x] ^ init
			
		init = init << 1

	binaries[4] = binaries[0] & binaries[1] & binaries[2] & binaries[3]

	#this checks for a edge case when this and can make all the bits 0 after the 7th bit,
	#and this makes the result of the and be a @. This is probably not the best way to fix
	#this problem, but it works

	#print binaries

	if not checkinrange(binaries[4]):
		for x in xrange(0,4):
			if checkinrange(binaries[x] | 0x1):
				binaries[x] = binaries[x] | 0x1
			else:
				binaries[x] = binaries[x] ^ 0x2
				binaries[x] = binaries[x] | 0x1
		
	binaries[4] = binaries[0] & binaries[1] & binaries[2] & binaries[3]	

	#print binaries

	return ''.join(chr(x) for x in binaries)

#fourth set of chars from the serial key
#the OR of the 3 odd positioned characters MOD 16 must be value of the XOR of the 2 even positioned character
def fourthblock():
	binaries = [0x00,0x00,0x00,0x00,0x00] #placeholder for creating the block

	#randomly picks the first 3 chars
	for x in range(0,5,2):
		binaries[x] = ord(random.choice(chars))

	#get the or from it

	or3 = binaries[0] | binaries[2] | binaries[4]

	#get the 2 last values in a separated array so I can shuffle them
	last = [0x00,0x00]

	#randomly build the 2 last values based on those

	if random.choice([ True, False ]): #randonly decides if the values will be numbers or letters
		#case letter
		for x in xrange(0,2):
			last[x] = last[x] ^ 0x41
	else: #case number
		for x in xrange(0,2):
			last[x] = last[x] ^ 0x30

	#randonly flips bits in the values
	init = 0x8
	#for each of the 4 flippable bits
	for z in range(0,4):

		#if this bit is a 1, only one value gets a 1
		if or3 & init == init:
			if checkinrange(last[0] ^ init): #if bit can be flipped from this char
				last[0] = last[0] ^ init
			elif checkinrange(last[1] ^ init):#else try to flip from the other one
				last[1] = last[1] ^ init
			else: #if it cant flip any bit, just try it again, its easier than caring for edge cases
				return fourthblock()

		else: # if it is not, both values can be either 1 or 0, so pick randomly
			if random.choice([ True, False ]):#case both 1
				if checkinrange(last[0] ^ init) and checkinrange(last[1] ^ init):
					last[0] = last[0] ^ init
					last[1] = last[1] ^ init

		random.shuffle(last)
		init = init >> 1

	binaries[1] = last[0]
	binaries[3] = last[1]

	#print (binaries[0] | binaries[2] | binaries[4]) % 16 == last[0] ^ last[1]
	#print binaries

	return ''.join(chr(x) for x in binaries)

#fifth set of chars from the serial key
#the first character should be the second -1 , the third character should be the fourth + 1, and the
#last has to be X
def fifthblock():
	binaries = [0x00,0x00,0x00,0x00,0x58] #placeholder for creating the block

	#picking the first
	binaries[0] = ord(random.choice(chars))

	#check if first+1 is valid
	while not checkinrange(binaries[0]+1):
		binaries[0] = ord(random.choice(chars))

	binaries[1] = binaries[0]+1

	#picking the third
	binaries[2] = ord(random.choice(chars))

	#check if third-1 is valid
	while not checkinrange(binaries[2]-1):
		binaries[2] = ord(random.choice(chars))

	binaries[3] = binaries[2]-1

	return ''.join(chr(x) for x in binaries)

print firstblock() + "-" + secondblock() + "-" + thirdblock() + "-" + fourthblock() + "-" + fifthblock()