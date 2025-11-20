#!/usr/bin/env python3


with open("test1", "rb") as f:
    bin_data = bytearray(f.read())


# 1. find locations and offsets in main
call_marker = None # find 0xe8 f3 (unique instruction in main)
for i in range(len(bin_data) - 1):
    if bin_data[i] == 0xE8 and bin_data[i + 1] == 0xF3:
        call_marker = i
        break
push_loc = None # find 0xB8 00 00 00 00 after call marker
for j in range(call_marker + 2, len(bin_data)):
    if bin_data[j] == 0xB8 and bin_data[j+1:j+5] == bytes([0,0,0,0]):
        push_loc = j
        break
ret_loc = None # find ret (0xC3) after epilogue
for k in range(push_loc + 1, len(bin_data)):
    if bin_data[k] == 0xC3:
        ret_loc = k
        break

# 2. find NOP function
write_loc = None
for i in range(len(bin_data) - 1):
    if bin_data[i] == 0x90 and bin_data[i + 1] == 0x90: # first and only occurence of 0x90 90
        write_loc = i
        break


# 3. save instructions from main
inst_len = 9
savedInstructions = bytes(bin_data[ret_loc - inst_len: ret_loc])



# 4. build and write payload to nop function
payload = bytes([
    0xeb, 0x0c, 0x4e, 0x6f, 0x74, 0x20, 0x61, 0x20, 0x76, 0x69, 0x72, 0x75, 0x73, 0x0a, 0xb8, 0x01, 0x00, 0x00, 0x00, 0xbf, 0x01, 0x00, 0x00, 0x00, 0x48, 0x8d, 0x35, 0xe3, 0xff, 0xff, 0xff, 0xba, 0x0c, 0x00, 0x00, 0x00, 0x0f, 0x05
]) + savedInstructions + bytes([0xC3])

bin_data[write_loc:write_loc+len(payload)] = payload

# 5. write tricky jump to main function
target_addr = 0x401150
patch = [
    0x68,
    (target_addr >> 0) & 0xFF,
    (target_addr >> 8) & 0xFF,
    (target_addr >> 16) & 0xFF,
    (target_addr >> 24) & 0xFF,
]
patch += [0x90] * (inst_len - len(patch)) # nop padding
bin_data[ret_loc - inst_len: ret_loc] = bytes(patch)



with open("test1mod", "wb") as f:
    f.write(bin_data)
