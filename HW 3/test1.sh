#!/bin/bash
# setup: create the message1.txt and message2.txt files
/bin/rm -f message[12].txt
echo "Two things are infinite: the universe and human stupidity;" > message1.txt
echo "and I'm not sure about the the universe." >> message1.txt
echo "by Albert Einstein" >> message1.txt
echo "The quick brown fox jumped over the lazy dog." > message2.txt
# 1: create keys alice-public.key and alice-private.key
./rsa.sh -key alice -keygen 200
# 2: create keys bob-public.key and bob-private.key
./rsa.sh -key bob -keygen 200
# 3: alice is going to encrypt a message for bob
./rsa.sh -key bob -input message1.txt -output encrypted1.txt -encrypt