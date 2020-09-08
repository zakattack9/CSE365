import argparse
import os
import time
import socket
import sys
from aes import AESCipher
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
import textwrap

def wrap64(string):
    return '\n'.join(textwrap.wrap(string,64))

# Handle command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ipaddress",
                    help='ip address where the server is running',
                    default='127.0.0.1',  # Defaults to loopback
                    required=True)
parser.add_argument("-p", "--port",
                    help='port where the server is listening on',
                    required=True)
parser.add_argument("-f", "--publickey",
                    help='name of public key',
                    default='serverPublicKey',
                    required=False)
parser.add_argument("-v", "--verbose",
                    help="print out extra info to stdout",
                    default='True',
                    required=False)
parser.add_argument("-e", "--eavesdrop",
                    help="filename of eavesdrop",
                    default='True',
                    required=False)

args = parser.parse_args()
f = open(args.eavesdrop, "rb")
b = f.read()
f.close()

# load server's public key
serverPublicKeyFileName = args.publickey
key = ""
with open(serverPublicKeyFileName, 'r') as f:
    key = RSA.importKey(f.read())

MESSAGE_LENGTH = 2048

# 256 byte RSA-encrypted AES key from client-server Wireshark capture for default 'True' message
eavesdroppedrsa = b[0:256] #bytearray.fromhex('4a04ac1ffcc305c4c5f0daaeca07bca5be7cc795f812bd57d96933904ec4433d5033bae1729a6e0fae3d62cc081ed51111db6cfe96b2d84c633c827662bc076c83d401bbbb02a0d454b6fb6ab355be62e9dec8542741f2583b49d0794230ffdcdc6aebf444e139f69594cd4cfdc544178611027757cf534c725384a0e35b2eee66772261bc49de4666f9cb16b94e32335cce727664032058259a6ff6e31a110f4f8c03f1ec166a656269c1a126a587d4e472cc082bd08df6c50b2567e29798c84f7abd605aef66a46fdb471c5bad7c02071923a210bbfe236e5a5b32359d12040a37c9db2785f1d11faa2619b617b6deeb7da0011fbba82e44246aac99231d42')


bitsknown = ''
while (len(bitsknown) < 256):
    i = 255 - len(bitsknown)
    shifty = pow(2, i * key.e, key.n)
    sessionkey = (bytes_to_long(eavesdroppedrsa) * shifty) % key.n
    for tryabit in ['0', '1']:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hint = (i << 1) + int(tryabit)
        print(hint)
        #sock.setsockopt(socket.SOL_TCP, socket.TCP_MAXSEG, 500 + hint)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, hint % 128 + 32)
        differentipaddress = "127.0.0." + str((hint >> 7) + 1)
        print(differentipaddress)
        server_address = (differentipaddress, int(args.port))
        #server_address = (args.ipaddress, int(args.port))
        sock.connect(server_address)
        sock.settimeout(2)
        AESkeytry = long_to_bytes(int(tryabit + bitsknown + '0'*i, 2), 32)
        print('guessing...\n{}'.format(wrap64(tryabit + bitsknown + '0'*i)))
        aes = AESCipher(AESkeytry)
        answer = b''
        try:
            message = aes.encrypt('GoSeeCal') 
            msg = long_to_bytes(sessionkey, 256) + message
            sock.sendall(msg)
            amount_received = 0
            amount_expected = len(message)

            if amount_expected % 16 != 0:
                amount_expected += (16 - (len(message) % 16))

            if amount_expected > amount_received:
                while amount_received < amount_expected:
                    data = sock.recv(MESSAGE_LENGTH)
                    amount_received += len(data)
                    answer += data
        except Exception as e:
            print(e)
        else:
            #messageresult = (aes.decrypt(answer))
            if aes.decrypt(answer).strip() == b'GOSEECAL':
                bitsknown = str(tryabit) + bitsknown
                break
        finally:
            sock.close()

AESkey = long_to_bytes(int(bitsknown, 2), 32)
aes = AESCipher(AESkey)
eavesdroppedaes = b[256:] #bytes.fromhex('088d72fda25863ae81a27ddc286ee8ffef55bdcd0eeee4487fa42cb9c012155e6c38a32d741c68aaa86fda4c9878cbb4')
print('Recovered plaintext is: {}'.format(aes.decrypt(eavesdroppedaes)))
print('Sending to server...')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (args.ipaddress, int(args.port))
sock.connect(server_address)
sock.settimeout(2)
aes = AESCipher(AESkey)
answer = b''
sessionkey = bytes_to_long(eavesdroppedrsa)
try:
    message = eavesdroppedaes
    msg = long_to_bytes(sessionkey, 256) + message
    sock.sendall(msg)
    amount_received = 0
    amount_expected = len(message)

    if amount_expected % 16 != 0:
        amount_expected += (16 - (len(message) % 16))

    if amount_expected > amount_received:
        while amount_received < amount_expected:
            data = sock.recv(MESSAGE_LENGTH)
            amount_received += len(data)
            answer += data
except Exception as e:
    print(e)
else:
    print(aes.decrypt(answer).strip())
finally:
    sock.close()
