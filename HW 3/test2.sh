# test speech 1
./rsa.sh -key susan -keygen 500
./rsa.sh -key abe -keygen 500
./rsa.sh -key abe -input speech1.txt -output encrypted1.txt -encrypt
# ./rsa.sh -key abe -input encrypted1.txt -output speech1b.txt -decrypt
# diff speech1.txt speech1b.txt

# test speech 2
./rsa.sh -key susan -keygen 500
./rsa.sh -key abe -keygen 500
./rsa.sh -key abe -input speech2.txt -output encrypted2.txt -encrypt
./rsa.sh -key abe -input encrypted2.txt -output speech2b.txt -decrypt
diff speech2.txt speech2b.txt

# /bin/rm -f susan*.key abe*.key message*.sign message?b.txt encrypted?.txt message?.txt