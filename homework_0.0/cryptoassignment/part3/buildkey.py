# Read the top of streamy.py for usage, and see line 23 of this file
from aes import AESCipher
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
import textwrap
import fileinput

def wrap64(string):
    return '\n'.join(textwrap.wrap(string,64))

bitsknownint = 0

for line in fileinput.input():
    if len(line) > 10:
        firstline = line
        if (len(line) % 2 == 0):
            firstline = '0' + line
        continue
    x, y = map(int, line.split())
    hint = ((x - 1) << 7) | (y - 32) # AES key fully shifted left
    tryabit = hint & 1 # last bit popped off
    i = hint >> 1 # shift AES key to the right
# All you have to do is figure out what YYY and ZZZ should be...
    printStr = "HINT: " + str(hint) + " TRYABIT: " + str(tryabit) + " AT I: " + str(i)
    print(printStr)
    # print(str(x) + " " + str(y))
    # print(firstline)
    # print(tryabit)
    # print(i)
    # if (tryabit & 1 == ):
    # if (len(str(bitsknownint)) - 1 < 256):
    # if ()
        # bitsknownint = str(tryabit) + str(bitsknownint)
        # bitsknownint = ((tryabit << (len(str(bitsknownint)))) | bitsknownint) 
        # print(bitsknownint)
# 00100 >> 0010
# 0111 

# 510 => 111111110
# 508 => 111111100
# 509 => 111111101
# 506 => 111111010

#while (len(bitsknown) < 256):
#    i = 255 - len(bitsknown)
    #for tryabit in ['0', '1']:
        #hint = (i << 1) + int(tryabit)
                #bitsknown = str(tryabit) + bitsknown
bitsknownint = int(bitsknownint[:-1], 2)
print(bitsknownint)
AESkey = long_to_bytes(bitsknownint, 32)
aes = AESCipher(AESkey)
print(firstline)
print(len(firstline))
eavesdroppedaes = bytes.fromhex(firstline)
#('088d72fda25863ae81a27ddc286ee8ffef55bdcd0eeee4487fa42cb9c012155e6c38a32d741c68aaa86fda4c9878cbb4')
print('Recovered plaintext is: {}'.format(aes.decrypt(eavesdroppedaes)[:400]))
printme = "{0:b}".format(bitsknownint)
while len(printme) < 256:
    printme = '0' + printme
print(wrap64(printme))

