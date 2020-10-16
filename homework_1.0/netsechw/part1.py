# python3 part1.py vertical.pcap

import pyshark
import sys

cap = pyshark.FileCapture(sys.argv[1])

# used to calculate frequency of sequence numbers
ip_addr = {}
ttl = {}
for p in cap:
  # gets number of unique ip addresses in pcap
  # try:
  #   if p.ip.src in ip_addr:
  #     ip_addr[p.ip.src] = ip_addr[p.ip.src] + 1
  #   else:
  #     ip_addr[p.ip.src] = 1
  # except:
  #   print("NO IP")

  # gets number of different TTLs in pcap
  try:
    if p.ip.ttl in ttl:
      ttl[p.ip.ttl] = ttl[p.ip.ttl] + 1
    else:
      ttl[p.ip.ttl] = 1
  except:
    print("NO TTL")

# print(ip_addr)
print(ttl)

# number of unique IP addresses in vertical.pcap
# {
#   "169.125.5.2": 3837,
#   "188.136.176.2": 1281,
#   "169.125.5.1": 3,
#   "4.240.20.1": 2,
#   "188.136.176.3": 1142,
#   "150.114.84.2": 1142,
#   "132.222.172.2": 1
# }

# number of unique TTLs in vertical.pcap
# {
#   "41": 156,
#   "37": 152,
#   "53": 152,
#   "54": 130,
#   "62": 3567,
#   "55": 147,
#   "38": 153,
#   "47": 152,
#   "45": 121,
#   "40": 137,
#   "52": 144,
#   "42": 144,
#   "51": 147,
#   "39": 148,
#   "43": 151,
#   "57": 158,
#   "46": 162,
#   "58": 150,
#   "59": 145,
#   "64": 470,
#   "56": 142,
#   "50": 126,
#   "49": 138,
#   "48": 135,
#   "44": 145,
#   "60": 1,
#   "3": 3,
#   "2": 3,
#   "1": 3,
#   "4": 3,
#   "5": 3,
#   "6": 3,
#   "7": 3,
#   "8": 3,
#   "63": 4,
#   "9": 3,
#   "10": 3,
#   "61": 1
# }
