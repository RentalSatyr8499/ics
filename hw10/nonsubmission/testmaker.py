# make_testB.py
data = bytearray(0x2000)  # allocate 8KB of space

# 1. Entry point at 0x18–0x1b
data[0x18:0x1c] = bytes([0x40, 0x10, 0x40, 0x00])

# 2. Fake epilogue at 0x1120
epilogue = [
    0x90,              # nop
    0x58,              # pop eax
    0xB8, 0x01, 0x00, 0x00, 0x00,  # mov eax, 1
    0x48, 0x83, 0xC4, 0x04,  # add esp, 4
    0xC3               # ret
]
data[0x1120:0x1120+len(epilogue)] = bytes(epilogue)

# 3. Large NOP sled at 0x1500
data[0x1500:0x1500+100] = bytes([0x90] * 100)

# Write out to file
with open("testB", "wb") as f:
    f.write(data)

print("testB created.")
