import argparse
import os
import time
#import socket
import sys
import string
#from aes import AESCipher
#from Crypto.PublicKey import RSA

# Handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cipher",
                    help='cipher... caesar or julia',
                    required=True)
parser.add_argument("-d", "--decrypt",
                    help='Decrypt a file',
                    required=False)
parser.add_argument("-e", "--encrypt",
                    help='Encrypt a file',
                    required=False)
parser.add_argument("-o", "--outfile",
                    help='Output file',
                    required=False)

args = parser.parse_args()

encrypting = True

def lrot(n, d): return ((n << d)|(n >> (8 - d)))&0xff

try:
    ciphertext = open(args.decrypt, "rb").read()
    try:
        plaintext = open(args.encrypt, "rb").read()
        print("You can't specify both -e and -d")
        exit(1)
    except:
        encrypting = False
except:
    try:
        plaintext = open(args.encrypt, "rb").read()
    except:
        print("Input file error (did you specify -e or -d?)")
        exit(1)

try:
    whichcipher = args.cipher
    if (whichcipher == 'julia') or (whichcipher == 'caesar'):
        output = open(args.outfile, "wb")
    else:
        print('Available ciphers are julia and caesar, case sensitive')
        exit(1)
except:
    print("Output file error or you didn't specify cipher")
    exit(1)



if (encrypting):
    if whichcipher == 'julia':
        keybytes = bytes(os.urandom(13))
        keyshift = keybytes[0] % 7 + 1
        keyxor = [] 
        keyxorasstring = ""
        for i in range(1, 13):
            keyxor.append(ord(string.ascii_letters[keybytes[i] % len(string.ascii_letters)]))
            keyxorasstring = keyxorasstring + chr(keyxor[i-1])
        print('Key is shifting by ' + str(keyshift) + ' and XORing with ' + keyxorasstring)
        ciphertext = []
        for i in range(0, len(plaintext)):
            ciphertext.append(lrot(plaintext[i], keyshift) ^ keyxor[i % len(keyxor)])
        output.write(bytes(ciphertext))
        output.close
    elif whichcipher == 'caesar':
        keybytes = bytes(os.urandom(1))
        keyrotate = int(keybytes[0] % 25) + 1
        print('Key is ' + string.ascii_uppercase[keyrotate] + ' i.e. rotating by ' + str(keyrotate))
        skipped = 0
        ciphertext = ''
        for i in range(0, len(plaintext)):
            if chr(plaintext[i]) in string.ascii_uppercase:
                p = plaintext[i] - ord('A')
                c = chr(ord('A') + ((p + keyrotate) % 26))
                ciphertext = ciphertext + c
            else:
                skipped = skipped + 1
        output.write(ciphertext.encode('ascii'))
        output.close
        if skipped != 0:
            print('Skipped ' + str(skipped) + ' bytes for not being capital letters')
    else:
        print('Should not have gotten here')
        exit(1)

