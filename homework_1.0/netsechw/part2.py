# python3 part2.py sidechannel.pcap

import pyshark
import sys

cap = pyshark.FileCapture(sys.argv[1])

dst_ports = {}
src_ip_addrs = {}
src_ip_addrs_zombie = {}
src_ip_addrs_attacker = {}
for p in cap:
  # gets frequency of destination ports 
  # def add_to_dst_ports(dst_port):
  #   if dst_port in dst_ports:
  #     dst_ports[dst_port] = dst_ports[dst_port] + 1
  #   else:
  #     dst_ports[dst_port] = 1

  # if hasattr(p, 'tcp'):
  #   add_to_dst_ports(p.tcp.dstport)
  # if hasattr(p, 'udp'):
  #   add_to_dst_ports(p.udp.dstport)

  # gather source IPs who's destination is the pasty/zombie
  try:
    if p.ip.dst == "188.136.176.2":
      if p.ip.src in src_ip_addrs_zombie:
        src_ip_addrs_zombie[p.ip.src] = src_ip_addrs_zombie[p.ip.src] + 1
      else:
        src_ip_addrs_zombie[p.ip.src] = 1
  except:
    print("NO IP")

  # gather source IPs who's destination is the attacker
  try:
    if p.ip.dst == "169.125.5.2":
      if p.ip.src in src_ip_addrs_attacker:
        src_ip_addrs_attacker[p.ip.src] = src_ip_addrs_attacker[p.ip.src] + 1
      else:
        src_ip_addrs_attacker[p.ip.src] = 1
  except:
    print("NO IP")

  # gather frequency of all src IPs in pcap
  # try:
  #   if p.ip.src in src_ip_addrs:
  #     src_ip_addrs[p.ip.src] = src_ip_addrs[p.ip.src] + 1
  #   else:
  #     src_ip_addrs[p.ip.src] = 1
  # except:
  #   print("NO IP")

# print(dst_ports)
# print(src_ip_addrs)
print(src_ip_addrs_zombie)
print(src_ip_addrs_attacker)


# all source IPs from sidechannel.pcap
# {
#   "188.136.176.4": 420, // only SYN
#   "188.136.176.126": 420, // only SYN
#   "188.136.176.33": 420, // only SYN
#   "188.136.176.99": 420, // only SYN
#   "188.136.176.5": 420, // only SYN
#   "188.136.176.199": 420, // only SYN
#   "188.136.176.127": 742, // SYN and RST
#   "169.125.5.79": 4200,
#   "4.240.20.2": 533 // likely offline
#   // "188.136.176.2": 13266,
#   // "188.136.176.3": 786,
#   // "169.125.5.2": 6700,
# }

# all source IPs from horizontal.pcap
# {
#   "188.136.176.1": 12,
#   "169.125.5.127": 6,
#   "4.240.20.1": 591,
#   "150.114.84.1": 11,
#   "150.114.84.2": 13,
#   "132.222.172.2": 589
#   // "188.136.176.2": 11,
#   // "188.136.176.3": 10,
#   // "169.125.5.2": 10597,
# }
