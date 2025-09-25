#!/usr/bin/python3

import sys, crc
verbose = False

def dictionaryAttack(dictionary, passwordHashes, salt):
	return "Testing dictionary input: " + str(dictionary) + "\n" + str(passwordHashes) + "\n" + str(salt)

def main():
	global verbose
	input = ""
	dictionary = []
	passwordHashes = {}
	salt = ""

	i = 1
	while i < len(sys.argv):

		if i == 1: # dictionary word bank
			with open(sys.argv[i], 'r') as f:
				dictionary = f.read().strip().split("\n")
		elif i == 2: # passwords to crack
			with open(sys.argv[i], 'r') as f:
				input = f.read().strip().split("\n")
				for j in input:
					j = j.split(" ")
					passwordHashes[j[0]] = j[1]
		elif i == 3: # salt
			salt = sys.argv[i]
		elif i == 4:
			if sys.argv[i] == "-verbose": 
				verbose = True
			else: 
				print ("Extra parameter: '" + str(sys.argv[i]) + "', exiting.")
				exit()
		else:
			print ("Extra parameter: '" + str(sys.argv[i]) + "', exiting.")
			exit()

		i += 1

	with open("output.txt", "w") as f:
		result = dictionaryAttack(dictionary, passwordHashes, salt)
		print(result)
		
if __name__ == '__main__':
	main()
