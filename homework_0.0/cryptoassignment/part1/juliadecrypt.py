import math

with open('juliaplaintext.txt.gz.enc', 'rb') as file:
  data = file.read()
  # print(data)

keybyte = 'hUftKOPlQDWp'
bitshift = 2
multiplier = math.ceil(len(data) / len(keybyte))

decrypted = ''
for ch0, ch1 in zip(data, keybyte * multiplier):
  decryptedByte = ord(chr(ch0)) ^ ord(ch1)
  decrypted += chr(decryptedByte)
# print(decrypted)

byteArr = []
for char in decrypted:
  intChar = ord(char)
  rotatedChar = (intChar >> bitshift) | ((intChar << (8 - bitshift)) & 0xff)
  byteArr.append(rotatedChar)
# print(byteArr)

with open('juliaplaintext.txt.gz', 'wb') as decrypted_file:
  decrypted_file.write(bytes(byteArr))
