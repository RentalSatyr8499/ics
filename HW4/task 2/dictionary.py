#!/usr/bin/python3

import sys, hashlib
verbose = False

def dictionaryAttack(dictionary, passwordHashes, salt):
	passwords = {}
	for word in dictionary: 
		currHash = hashlib.sha256(str(word + salt).encode()).hexdigest()
		if currHash in passwordHashes:
			user = passwordHashes[currHash]
			passwords[user] = word
		if len(passwords) == len(passwordHashes):
			break
	return passwords


def main():
	global verbose
	input = ""
	dictionary = []
	passwordHashes = {}
	salt = ""
	duplicatePasswords = {}

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

					if j[1] in passwordHashes: # there is a duplicate password.
						if passwordHashes[j[1]] not in duplicatePasswords:
							duplicatePasswords[passwordHashes[j[1]]] = [j[0]]
						else:
							duplicatePasswords[passwordHashes[j[1]]].append(j[0])
					else:
						passwordHashes[j[1]] = j[0]
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


	result = dictionaryAttack(dictionary, passwordHashes, salt)
	for key in result:
		print(f"password for {key} is: {result[key]}")

	if verbose:
		print(f"result: {result}\nduplicatePasswords: {duplicatePasswords}")

	# account for duplicates
	if (len(duplicatePasswords) != 0) and (len(result) != 0):
		print(duplicatePasswords)
		for a in duplicatePasswords:
			for b in duplicatePasswords[a]:
				print(f"password for {b} is: {result[a]}")
		
if __name__ == '__main__':
	main()
