# Read the top of streamy.py for usage, and see line 23 of this file
from aes import AESCipher
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
import textwrap
import fileinput

def wrap64(string):
    return '\n'.join(textwrap.wrap(string,64))

bitsknownint = ""
curr = 255

for line in fileinput.input():
    if len(line) > 10:
        firstline = line
        if (len(line) % 2 == 0):
            firstline = '0' + line
        continue
    x, y = map(int, line.split()) #
    hint = ((x - 1) << 7) | (y - 32) # AES key fully shifted left
    tryabit = hint & 1 # last bit popped off
    i = hint >> 1 # shift AES key to the right
# All you have to do is figure out what YYY and ZZZ should be...
    printStr = "HINT: " + str(hint) + " TRYABIT: " + str(tryabit) + " AT I: " + str(i)
    # print(printStr)
    print(str(i) + " " + str(tryabit))
    # print(str(x) + " " + str(y))
    # print(firstline)
    # if (tryabit & 1 == ):
    # if (len(str(bitsknownint)) - 1 < 256):
    if (i < curr or tryabit == 1):
        bitsknownint = str(tryabit) + str(bitsknownint)
        curr = curr - 1
        # bitsknownint = ((tryabit << (len(str(bitsknownint)))) | bitsknownint) 
        # print(bitsknownint)

#while (len(bitsknown) < 256):
#    i = 255 - len(bitsknown)
    #for tryabit in ['0', '1']:
        #hint = (i << 1) + int(tryabit)
                #bitsknown = str(tryabit) + bitsknown
bitsknownint = int(bitsknownint, 2)
print(bitsknownint)
# print(len(bitsknownint))
AESkey = long_to_bytes(bitsknownint, 32)
aes = AESCipher(AESkey)
print(firstline)
print(len(firstline))
eavesdroppedaes = bytes.fromhex(firstline)
#('088d72fda25863ae81a27ddc286ee8ffef55bdcd0eeee4487fa42cb9c012155e6c38a32d741c68aaa86fda4c9878cbb4')
print('Recovered plaintext is: {}'.format(aes.decrypt(eavesdroppedaes)[:400]))

with open('rsaplaintext.txt', 'wb') as out_file:
  out_file.write(aes.decrypt(eavesdroppedaes)[:400])

printme = "{0:b}".format(bitsknownint)
while len(printme) < 256:
    printme = '0' + printme
print(wrap64(printme))

