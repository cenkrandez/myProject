import scapy.all as scapy 
import optparse
# 1) arp request
# 2) broadcast 
# 3) response


def get_user_input():
	parse_object = optparse.OptionParser()
	parse_object.add_option("-i", "--ipaddress",dest= "ip_address",help="Enter IP Address")

	(user_input,arguments) = parse_object.parse_args()

	if not user_input.ip_address:
		print("Enter IP Address")

	return user_input

def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combinede_packet = broadcast/arp_request
	(answered_list,unsanswered_list) = scapy.srp(combinede_packet,timeout=1)
	answered_list.summary()

user_ip_address = get_user_input()
scan(user_ip_address.ip_address)
#scapy.ls(scapy.ARP)
