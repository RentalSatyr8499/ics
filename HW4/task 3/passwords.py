#!/usr/bin/python3

import sys, hashlib, string
verbose = False

def checkPassword(currPassHash, oldPassword, salt):
	for firstLetter in string.printable:
		for secondLetter in string.printable:
			invalidPassword = oldPassword + firstLetter + secondLetter + salt
			invalidPassHash = hashlib.sha256(str(invalidPassword).encode()).hexdigest()
			if currPassHash == invalidPassHash:
				return firstLetter + secondLetter
	return ""

def main():
	global verbose
	currPassHash = ""
	oldPassword = ""
	salt = ""
	
	i = 1
	while i < len(sys.argv):

		if i == 1:
			currPassHash = sys.argv[i]
		elif i == 2:
			oldPassword = sys.argv[i]
		elif i == 3:
			salt = sys.argv[i]
		else:
			print ("Extra parameter: '" + str(sys.argv[i]) + "', exiting.")
			exit()

		i += 1

	with open("output.txt", "w") as f:
		result = checkPassword(currPassHash, oldPassword, salt)
		if result == "": print("Not found")
		else: print(f"Found: {result}")


		
if __name__ == '__main__':
	main()
