import argparse
import os
import time
import socket
import sys
from aes import AESCipher
from Crypto.PublicKey import RSA

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
parser.add_argument("-m", "--messagefile",
                    help='what file the message should come from',
                    default='',
                    required=True)
parser.add_argument("-e", "--eavesdrop",
                    help='where to put eavesdropped stuff',
                    default='',
                    required=True)

args = parser.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (args.ipaddress, int(args.port))
sock.connect(server_address)
sock.settimeout(2)

AESKey = bytes(os.urandom(32))
while AESKey[0] == 0:  # Make sure there aren't leading 0s
    AESKey = bytes(os.urandom(32))

if args.verbose is True:
    binKey = bin(int.from_bytes(AESKey, byteorder='big'))
    print("Using AES key : {}".format(binKey))

# load server's public key
serverPublicKeyFileName = args.publickey
key = ""
with open(serverPublicKeyFileName, 'r') as f:
    key = RSA.importKey(f.read())

MESSAGE_LENGTH = 2048

encryptedKey = key.encrypt(AESKey, 32)[0]
while len(encryptedKey) != 2048>>3:
    #Python is weird about leading 0's, fix it up
    encryptedKey = b'\x00' + encryptedKey
aes = AESCipher(AESKey)
try:
    # Send data
    try:
        filetosend = open(args.messagefile, "r")
        plaintext = filetosend.read()
        filetosend.close()
        print(plaintext)
        message = aes.encrypt(plaintext)
    except ValueError:
        print("Client with port {} failed.".format(args.port),
              file=sys.stderr)
        exit(1)
    fileforeavesdrop = open(args.eavesdrop, "wb")
    msg = bytearray(encryptedKey + message)
    # msg: AES key encrypted by the public key of RSA
    #      + message encrypted by the AES key

    print('Sending: {}'.format(message.hex()))
    sock.sendall(msg)
    fileforeavesdrop.write(msg)
    fileforeavesdrop.close()

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

#    if amount_expected % 16 != 0:
#       amount_expected += (16 - (len(message) % 16))

    answer = b''
    if amount_expected > amount_received:
        while amount_received < amount_expected:
            try:
                data = sock.recv(MESSAGE_LENGTH)
                print(data)
            except socket.timeout as e:
                err = e.args[0]

                if err == 'timed out':
                    print('Connection timed out, waiting for retry',
                          file=sys.stderr)
                    time.sleep(1)
                    continue
                else:
                    print('Another issue: {}'.format(e),
                          file=sys.stderr)
                    break
            except socket.error as e:
                print('Socket error: {}'.format(e),
                      file=sys.stderr)
                break
            amount_received += len(data)
            answer += data

    print('Received: {}'.format(aes.decrypt(answer)))
    print('Succeeded for ' + args.messagefile)

finally:
    sock.close()
