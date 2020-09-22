import math
import string

with open('secretfile.txt.gz.enc', 'rb') as file:
  data = file.read()
  # print(data)

alphanumeric = string.ascii_letters + string.digits
keybyte = "DAhVXqVTiDRx"
bitshift = 2
multiplier = math.ceil(len(data) / len(keybyte))

# ALGORITHM TO FIGURE OUT KEY
# for letter in alphanumeric:
#   # key = "DAhV" + letter
#   # key = (keybyte + letter + "placeholder") * 1000 # placeholder should contain a random string that is the length remaining of the unsolved 12 length key minus 1 (i.e. current key = "KEY" + letter + "12345678")
#   key = keybyte * 1000 # after finding first four chars of key
#   print("\nLETTER: " + letter)
#   for ch0, ch1 in zip(data, key):
#     xor = (ch0 ^ ord(ch1))
#     rotated = (xor >> bitshift) | ((xor << (8 - bitshift)) & 0xff)
#     # print(hex(rotated))
#     # print(chr(rotated), end="")

decrypted = ''
for ch0, ch1 in zip(data, keybyte * multiplier):
  decryptedByte = ord(chr(ch0)) ^ ord(ch1)
  print(hex(decryptedByte))
  decrypted += chr(decryptedByte)
# print(decrypted)

byteArr = []
for char in decrypted:
  intChar = ord(char)
  rotatedChar = (intChar >> bitshift) | ((intChar << (8 - bitshift)) & 0xff)
  byteArr.append(rotatedChar)
# print(byteArr)

with open('secretfile.txt.gz', 'wb') as decrypted_file:
  decrypted_file.write(bytes(byteArr))

# .gz.enc
# (first 4 bytes)
# 0x38 => 0011 1000
# 0x6F => 0110 1111
# 0x48 => 0100 1000
# 0x76 => 0111 0110
#
# .gz
# (first 4 bytes)
# 0x1F => 0001 1111
# 0x8B => 1000 1011
# 0x08 => 0000 1000
# 0x08 => 0000 1000
#
# XOR
# (first 4 bytes)
# 0001 1111 XOR 0010 0111 = 0011 1000
# 1000 1011 XOR 1110 0100 = 0110 1111
# 0000 1000 XOR 0100 0000 = 0100 1000
# 0111 0110 XOR 0111 1110 = 0000 1000
#
# .gz.enc
# (filename bytes)
# 0x9F => 1001 1111
# 0xED => 1110 1101
# 0xC9 => 1100 1001
# 0x88 => 1000 1000
# 0xFD => 1111 1101
# 0x87 => 1000 0111
# 0xC1 => 1100 0001
# 0xD4 => 1101 0100
# 0xE7 => 1110 0111
# 0xC1 => 1100 0001
# 0xD1 => 1101 0001
# 0x95 => 1001 0101
# 0xB3 => 1011 0011
# 0xA9 => 1010 1001
#
# .gz
# (filename bytes)
# 0x73 => 0111 0011
# 0x65 => 0110 0101
# 0x63 => 0110 0011
# 0x72 => 0111 0010
# 0x65 => 0110 0101
# 0x74 => 0111 0100
# 0x66 => 0110 0110
# 0x69 => 0110 1001
# 0x6C => 0110 1100
# 0x65 => 0110 0101
# 0x2E => 0010 1110
# 0x74 => 0111 0100
# 0x78 => 0111 1000
# 0x74 => 0111 0100
#
# XOR
# (filename bytes)
# 0111 0011 XOR 1110 1100 = 1001 1111
# 0110 0101 XOR 1000 1000 = 1110 1101
# 0110 0011 XOR 1010 1010 = 1100 1001
# 0111 0010 XOR 1111 1010 = 1000 1000
# 0110 0101 XOR 1001 1000 = 1111 1101
# 0111 0100 XOR 1111 0011 = 1000 0111
# 0110 0110 XOR 1010 0111 = 1100 0001
# 0110 1001 XOR 1011 1101 = 1101 0100
# 0110 1100 XOR 1000 1011 = 1110 0111
# 0110 0101 XOR 1010 0100 = 1100 0001
# 0010 1110 XOR 1111 1111 = 1101 0001
# 0111 0100 XOR 1110 0001 = 1001 0101
# 0111 1000 XOR 1100 1011 = 1011 0011
# 0111 0100 XOR 1101 1101 = 1010 1001
#
# (first 4 bytes)
# 0001 1111 XOR 0010 0111 = 0011 1000
# 1000 1011 XOR 1110 0100 = 0110 1111
# 0000 1000 XOR 0100 0000 = 0100 1000
# 0111 0110 XOR 0111 1110 = 0000 1000