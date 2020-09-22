# pip3 install pyshark
# Then ...
# python3 streamy.py mypcap.pcap | python3 buildkey.py

import pyshark
import sys

# open the pcap file, filtered for a single TCP stream 
cap = pyshark.FileCapture(sys.argv[1])

tupledict = {}
datadict = {}
longeststreamlen = -1
skippy = -1

for p in cap:
    if p.transport_layer == 'TCP':
        stream = p.tcp.stream
        if (int(p.tcp.dstport) == 10047):
            try:
                thisstream = p.data.data.binary_value
                if (len(thisstream) > longeststreamlen):
                    longeststream = thisstream[256:]
                    longeststreamlen = len(thisstream)
                    skippy = stream
            except AttributeError:  # Skip the ACKs.
                pass
        #if (stream not in tupledict and
        if(int(p.tcp.dstport) == 10047):
            try:
                tupledict[stream] = (p.ip.dst, p.ip.ttl)
            except AttributeError:  # Skip the ACKs.
                pass
        #if (stream not in datadict and
        if(int(p.tcp.srcport) == 10047):
            try:
                #if (int(stream) == 190):
                #    print("PING")
                datadict[stream] = p.data.data.binary_value
                #if (int(stream) == 190):
                #    print("PONG")
            except AttributeError as error:  # Skip the ACKs.
                #if (int(stream) == 190):
                #    print(error)
                #val=p.all_fields
                datadict[stream] = b'hello'
                #print(val)
                pass

print(longeststream.hex())

for packettuple in tupledict:
    hinttuple = tupledict[packettuple]
    if (packettuple in datadict):
        if (packettuple != skippy):
            if (datadict[packettuple] != b"Couldn't decrypt!"):
                print(hinttuple[0][8:] + " " + hinttuple[1])
    else:
        #pass
        print("Something was in tupledict but not datadict")
        print("Stream is " + str(int(packettuple)))
        exit(1)


