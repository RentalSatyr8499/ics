def convertFromASCII(text):
	return int.from_bytes(bytes(text,'ascii'),"big")

def convertToASCII(block):
	h = hex(block)[2:]
	if len(h) % 2 == 1:
		h = '0' + h
	return bytes.fromhex(h).decode('ascii')

msg = "Two things are infinite: the universe and human stupidity;\nand I'm not sure about the the universe.\nby Albert Einstein\n"
integerReprestation = convertFromASCII(msg)
integerReprestation2 = 125603172303331364781624097781523865174527708194463373654352928497584181448475180952643281362009984649482635973601288674509730073840655603004170311118828451299488767278199114676043196822650042010316788694347890133112251078737651439146016899423496689704419539423961780044122572276985354
c = 12560317230333136478162409778152386517452770819446337365435292849758418144847518095264328136200998464948263597360128867450973007384065560300417031111882845129948876727819911467604319682265004201031678869434789001331122510787376514391460168994234966897044195394239617800404122572276985354

print(f"A: {integerReprestation}\nB: {integerReprestation2}\nare they equal: {integerReprestation==integerReprestation2}\nC: {c}")
print(f"converting integerRepresentation: {convertToASCII(integerReprestation)}")
print(f"converting integerRepresentation2: {convertToASCII(integerReprestation2)}")

'''msg = "Two things are infinite: the universe and human stupidity;\nand I'm not sure about the the universe.\nby Albert Einstein\n"
msg2 = convertFromASCII(msg)
msg3 = convertToASCII(msg2)

print(f"original: {msg}\ninteger representation: {msg2}\nconverted back: {msg3}")'''