# python3 part0.py horizontal.pcap

import pyshark
import sys

cap = pyshark.FileCapture(sys.argv[1])

# used to calculate frequency of sequence numbers
seq_nums = {}
for p in cap:
  if p.transport_layer == 'TCP':
    if p.tcp.seq_raw in seq_nums:
      seq_nums[p.tcp.seq_raw] = seq_nums[p.tcp.seq_raw] + 1
    else:
      seq_nums[p.tcp.seq_raw] = 1
print(seq_nums)



# check if machine responds with ICMP port unreachable
# check if the same machine does not respond with port unreachable for port 69 (meaning port is open)

# (p.tcp.seq_raw) # for sequence nums
# 132.222.172.2* (neither were called); has calls to destination port 69 (TFTP)
# 150.114.84.2
# 150.114.84.1
# 4.240.20.1* (neither were called); has calls to destination port 69 (TFTP)
# 188.136.176.1
# 188.136.176.2

# 188.136.176.3 (returned ICMP port unreachable for other ports but gave no response for port 69—likely an open port)

# raw sequence numbers frequency table
# {
#   "1036411689": 1022,
#   "3714604571": 1022,
#   "0": 30,
#   "1454605540": 1,
#   "1036411690": 4,
#   "356529039": 1,
#   "3351072361": 1,
#   "1115649182": 1,
#   "1036477224": 1001,
#   "1019634217": 1,
#   "2861603725": 770,
#   "2861669260": 730,
#   "2107423249": 1,
#   "3714604572": 3,
#   "2078295801": 1,
#   "1557562135": 1,
#   "3714670106": 1008,
#   "3697827611": 1,
#   "190739001": 770,
#   "190804536": 727
# }
