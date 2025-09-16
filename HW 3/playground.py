p = 923699493540667
q = 1122226872909601
n=(p)*(q)
e=675033172008551
d=pow(e,-1,(p-1)*(q-1))
print(f"p: {p}\nq: {q}\ne: {e}\nd: {d}\nn: {p*q}")

print(f"de % (p-1)*(q-1): {pow(d*e,1,(p-1)*(q-1))}")

msg = 125603172303331364781624097781523865174527708194463373654352928497584181448475180952643281362009984649482635973601288674509730073840655603004170311118828451299488767278199114676043196822650042010316788694347890133112251078737651439146016899423496689704419539423961780044122572276985354
cipher = pow(msg, e, n)
decrypted = pow(cipher, d, n)

print(f"original: {msg}\nciphered: {cipher}\ndecrypted: {decrypted}")

def convertFromASCII(text):
	return int.from_bytes(bytes(text,'ascii'),"big")

def convertToASCII(block):
	h = hex(block)[2:]
	if len(h) % 2 == 1:
		h = '0' + h
	return bytes.fromhex(h).decode('ascii')

msg = "Two things are infinite: the universe and human stupidity;\nand I'm not sure about the the universe.\nby Albert Einstein"
msg2 = convertFromASCII(msg)
msg3 = convertToASCII(msg2)

print(f"convertToASCII call: {convertToASCII(msg)}")