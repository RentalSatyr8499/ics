with open("test1","rb") as f:
    bin = list(f.read())

inst_len = 9
payload_len = 39

for i in range(0, len(bin)):
    if (bin[i] == 0xe8) and (bin[i+1] == 0xf3):
        push_loc = i
        break

for i in range(0, len(bin)):
    if (bin[i] == 0x90) and (bin[i+1] == 0x90):
        write_loc = i
        break

originalCode = bin[push_loc+5:push_loc+14]
bin[push_loc+5:push_loc+14] = [0x68, 0x50, 0x11, 0x00, 0x00, 0x90, 0x90, 0x90, 0x90]
bin[write_loc:write_loc+40] = [0xeb, 0x0c, 0x4e, 0x6f, 0x74, 0x20, 0x61, 0x20, 0x76, 0x69, 0x72, 0x75, 0x73, 0x0a, 0xb8, 0x01, 0x00, 0x00, 0x00, 0xbf, 0x01, 0x00, 0x00, 0x00, 0x8d, 0x34, 0x25, 0x22, 0x11, 0x40, 0x00, 0xba, 0x0c, 0x00, 0x00, 0x00, 0x0f, 0x05]
bin[write_loc+40:write_loc+51] = originalCode + [0xc3]

print([hex(w) for w in bin[4408+5:4408+14]])
print("push patch:", push_loc+5, push_loc+14)
print("payload patch:", write_loc, write_loc+51)
print("shdr table range:", 14960, 17264)

binout = b''
for i in bin:
    binout += bytes.fromhex("0x{:02x}".format(i).replace('0x',''))
with open("test1mod","wb") as f:
    f.write(binout)