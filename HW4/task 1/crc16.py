import crc, sys
assert len(sys.argv) == 2
with open(sys.argv[1]) as f:
    data = f.read()
bindata = bytes(data,"ascii")
calculator = crc.Calculator(crc.Crc16.MODBUS)
result = calculator.checksum(bindata)
print(sys.argv[0]+":",hex(result))