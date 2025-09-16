p = 923699493540667
q = 1122226872909601
n=(p)*(q)
e=675033172008551
d=pow(e,-1,(p-1)*(q-1))
print(f"p: {p}\nq: {q}\ne: {e}\nd: {d}\nn: {p*q}")

print(f"de % (p-1)*(q-1): {pow(d*e,1,(p-1)*(q-1))}")

msg = 125603172303331
cipher = pow(msg, e, n)
decrypted = pow(cipher, d, n)

print(f"original: {msg}\nciphered: {cipher}\ndecrypted: {decrypted}")
