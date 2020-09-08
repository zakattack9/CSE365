with open('ciphertext.txt', 'r') as file:
  ciphertext = file.read()

decryptStr = ''
for i in range(len(ciphertext)):
  dec = ord(ciphertext[i])
  decryptChar = ((dec - 65 - 7) % 26) + 65
  decryptStr += chr(decryptChar)

with open('caesarplaintext.txt', 'w') as out_file:
  out_file.write(decryptStr)
