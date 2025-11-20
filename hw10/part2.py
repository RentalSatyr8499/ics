#!/usr/bin/env python3


with open("test1", "rb") as f:
    bin_data = bytearray(f.read())


# --- Find call marker (unique 'e8 f3') ---
call_marker = None
for i in range(len(bin_data) - 1):
    if bin_data[i] == 0xE8 and bin_data[i + 1] == 0xF3:
        call_marker = i
        break
if call_marker is None:
    raise RuntimeError("Could not find 'e8 f3' marker")


# --- Find mov eax,0 (0xB8 00 00 00 00) after call marker ---
push_loc = None
for j in range(call_marker + 2, len(bin_data)):
    if bin_data[j] == 0xB8 and bin_data[j+1:j+5] == bytes([0,0,0,0]):
        push_loc = j
        break
if push_loc is None:
    raise RuntimeError("Could not find 'mov eax,0'")


# --- Find ret (0xC3) after epilogue ---
ret_loc = None
for k in range(push_loc + 1, len(bin_data)):
    if bin_data[k] == 0xC3:
        ret_loc = k
        break
if ret_loc is None:
    raise RuntimeError("Could not find 'ret'")


# --- Grab original 9 bytes before ret ---
orig_len = 9
originalCode = bytes(bin_data[ret_loc - orig_len: ret_loc])


# --- Find NOP island (first 0x90 0x90) ---
write_loc = None
for i in range(len(bin_data) - 1):
    if bin_data[i] == 0x90 and bin_data[i + 1] == 0x90:
        write_loc = i
        break
if write_loc is None:
    raise RuntimeError("Could not find NOP island")


# --- Build payload ---
payload = bytes([
    0xeb, 0x0c, 0x4e, 0x6f, 0x74, 0x20, 0x61, 0x20, 0x76, 0x69, 0x72, 0x75, 0x73, 0x0a, 0xb8, 0x01, 0x00, 0x00, 0x00, 0xbf, 0x01, 0x00, 0x00, 0x00, 0x48, 0x8d, 0x35, 0xe3, 0xff, 0xff, 0xff, 0xba, 0x0c, 0x00, 0x00, 0x00, 0x0f, 0x05
]) + originalCode + bytes([0xC3])


bin_data[write_loc:write_loc+len(payload)] = payload


# --- Overwrite 9 bytes in main with push imm32 + NOPs ---
# push imm32: 0x68 <imm32 little-endian>
target_addr = 0x401150
patch = [
    0x68,
    (target_addr >> 0) & 0xFF,
    (target_addr >> 8) & 0xFF,
    (target_addr >> 16) & 0xFF,
    (target_addr >> 24) & 0xFF,
]
# Fill remaining 4 bytes with NOPs
patch += [0x90] * (orig_len - len(patch))


bin_data[ret_loc - orig_len: ret_loc] = bytes(patch)


# --- Write out modified binary ---
with open("test1mod", "wb") as f:
    f.write(bin_data)


print(f"Patched main epilogue at offset {ret_loc-orig_len:#x} with push {target_addr:#x} + NOPs")
print(f"Wrote payload ({len(payload)} bytes) into NOP island at offset {write_loc:#x}")
