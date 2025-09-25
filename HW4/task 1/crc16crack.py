#!/usr/bin/python3

import sys, crc
verbose = False

def crack(input, desiredHash):
	suffix = 0	
	calculator = crc.Calculator(crc.Crc16.MODBUS)
	currHash = calculator.checksum(bytes(input + hex(suffix)[2:], "ascii"))

	l = len(hex(suffix))
	while currHash != desiredHash:
		if verbose and (len(hex(suffix)) != l):
			print(f"currHash {currHash} is not equal to desiredHash {desiredHash}: {hex(suffix)}")
			l = len(hex(suffix))

		suffix += 1
		currHash = calculator.checksum(bytes(input + hex(suffix)[2:], "ascii"))

		if len(hex(suffix)[2:]) > 10: 
			print(f"The suffix length has exceeded 10: {hex(suffix)}")
			exit

	return input + hex(suffix)[2:]

def main():
	global verbose
	input = ""
	desiredHash = 0
	i = 1
	
	while i < len(sys.argv):

		if i == 1:
			with open(sys.argv[i], 'r') as f:
				input = f.read().strip()
		elif i == 2:
			desiredHash = int(sys.argv[i], 16)
		elif i == 3:
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
		result = crack(input, desiredHash)
		f.write(result)

		if verbose:
			print(f"result: {result}")
			calculator = crc.Calculator(crc.Crc16.MODBUS)
			print(f"hash of result: {hex(calculator.checksum(bytes(result, "ascii")))}")

		
if __name__ == '__main__':
	main()
