#Apoorva Sharma
'''
In this script I have created a raw socket to access incoming packets on the network layer. The flow of the program is as follows-
1. On receinving a packet extract the 14 byte Ethernet Header (6 for source mac address + 6 destination mac + 2 for Ethernet Type)
2. The ethernet_head function processes the source mac, destination mac and protocol by using functions to convert hex to readable data.
3. The ipv4_head function processes 20 bytes IP header which has the IP version , header length , time to live , protocol , 32 bit source IP , 32 bit destination IP
4. The tcp_head function processes the 14 byte TCP header which contains 16 bit source port, 16 bit destination port, 32 bit sequence number, 32 bit acknowledgment number , and additional flags. 

'''

import socket #for socket programming 
import struct #for deciphering hexadecimal values to readible data
import textwrap #for formatting output


def get_mac_addr(bytes_addr):  #for deciphering address from bytes
    bytes_str = map('{:02x}'.format, bytes_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr
    
def ethernet_head(raw_data): #for extraxting ethernet head data
	dest,src,prototype = struct.unpack('! 6s 6s H', raw_data[:14]);
	src_mac = get_mac_addr(src);
	dest_mac = get_mac_addr(dest);
	proto = socket.htons(prototype);
	data = raw_data[14:];
	return dest_mac, src_mac, proto, data; #returns remaing data after the ethernet header for further processing
	
def ipv4(addr): #for deciphering IP address from string
    return '.'.join(map(str, addr))	
    
def ipv4_head(raw_data): #for deciphering IP header data
	version_header_length = raw_data[0]
	version = version_header_length >> 4
	header_length = (version_header_length & 15) * 4
	ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
	data = raw_data[header_length:]
	src = ipv4(src)
	target = ipv4(target)
	return version, header_length, ttl, proto, src, target, data #returns remaining data after the IP header for further processing
	
def tcp_head( raw_data): #for deciphering TCP header data
	(src_port, dest_port, sequence, acknowledgment, offset_reserved_flags) = struct.unpack('! H H L L H',raw_data[:14])
	offset = (offset_reserved_flags >> 12) * 4
	flag_urg = (offset_reserved_flags & 32) >> 5
	flag_ack = (offset_reserved_flags & 16) >> 4
	flag_psh = (offset_reserved_flags & 8) >> 3
	flag_rst = (offset_reserved_flags & 4) >> 2
	flag_syn = (offset_reserved_flags & 2) >> 1
	flag_fin = offset_reserved_flags & 1
	data = raw_data[offset:]
	return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack,flag_psh, flag_rst, flag_syn, flag_fin, data #returns the data extracted from TCP header

def format_multi_line(prefix, string, size=80): #for formatting output
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size-= 1
            return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

#INSIDE THE MAIN FUNCTION I SNIFF ETHERNET HEADER AND SNIFF IP HEADER IF PROTOCOL IS IPV4 , AND SNIFF TCP HEADER ONLY IF PROTOCOL USED IT TCP           		

def main():
	s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) #create a raw socket
	while True:
		print()
		print("********packet received********")
		raw_data, addr = s.recvfrom(65535)   #recieve packet data
		eth = ethernet_head(raw_data)        #pass the packet data to process ethernet head
		print('\nEthernet Frame:')
		print('Destination: {}, Source: {}, Protocol: {}'.format(eth[0],eth[1],eth[2])) #prints data extracted from the ethernet head
		if eth[2] == 8:         #if the protocol used is IPV4 only then the IP header is sniffed        
			ipv4 = ipv4_head(eth[3])
			print( '\n' + 'IPv4 Packet:')
			print( 'Version: {}, Header Length: {}, TTL:{},'.format(ipv4[0], ipv4[1], ipv4[2])) #prints the data extracted from IP header
			print( 'Protocol: {}, Source: {}, Target:{}'.format(ipv4[3], ipv4[4], ipv4[5]))
			if ipv4[3] == 6:    #if the protocol used is TCP only then the TCP header is sniffed. 
				tcp = tcp_head(ipv4[6])
				print('\n' + 'TCP Segment:')
				print('Source Port: {}, Destination Port: {}'.format(tcp[0], tcp[1])) #prints data extracted from TCP header
				print('Sequence: {}, Acknowledgment: {}'.format(tcp[2], tcp[3]))
				print('Flags:')
				print( 'URG: {}, ACK: {}, PSH:{}'.format(tcp[4], tcp[5], tcp[6]))
				print( 'RST: {}, SYN: {}, FIN:{}'.format(tcp[7], tcp[8], tcp[9]))
				if len(tcp[10]) > 0:
					if tcp[0] == 80 or tcp[1] == 80:
						print('\n' + 'HTTP Data:')
						try:
							http = HTTP(tcp[10])
							http_info = str(http[10]).split('\n')
							for line in http_info:
								print(str(line))
						except:
							print(format_multi_line('', tcp[10]))
					else:
						print('' + 'TCP Data:')
						print(format_multi_line('', tcp[10]))	
main()
