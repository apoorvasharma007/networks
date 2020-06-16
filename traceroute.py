# Apoorva Sharma
''' 
traceroute tracks the route packets taken from an source to a given destination host. The fundamental concept used is to use the IP protocol's time to live (TTL) field and attempt to elicit an ICMP TIME_EXCEEDED response from each gateway along the path to the host. Given the name of the destination host , I start my probe with a ttl of one and increase it by one until we get an ICMP "port unreachable" (or TCP reset), which means we got to an intermediate host router or destination , or hit a max hop value, which I have set to 33 hops. 

'''
import socket # for socket programming.
import sys    #for taking command line input.
HOST = ''     # both sender and receiver socket are on local host.
PORT = 33434  # the ports generally used for tracing routes are in range (33434,33534). I tried using other port numbers but they mostly never lead to destination. Thus all packets end up being dropped mid way. 
def main(destination_name):
	destination_addr = socket.gethostbyname(destination_name) #resolve the IP address of the destinaiton from its name.
	print("The path from you to " + destination_name + "  IP: " + destination_addr + " is --")  #takes you on a journey ! 
	icmp = socket.getprotobyname('icmp')  #standard protocol name of ICMP.
	udp = socket.getprotobyname('udp')    #standard protocol name of UDP.
	timeout = 0.2                         #the receiving socket will wait for a response  for maximum 0.2 seconds, then it will timeout.
	for ttl in range(1,34):
		receive_socket = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp) # receiving socket is a raw socket as it captures the ICMP signal.
		receive_socket.settimeout(timeout) #set timeout for receiving socket.        
		send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,udp) # the sending socket will send an empty string as message using UDP protocol
		send_socket.setsockopt( socket.SOL_IP, socket.IP_TTL, ttl)     # this function lets us set some parameters for the socket. I have set the TTL for the socket. 
		receive_socket.bind((HOST,PORT))                               #bind the host to the specified port to accept response from gateway routers and hosts. 
		send_socket.sendto(("").encode(), (destination_addr,PORT))     # send an empty string to destination with UDP protocol and a specified TTL value.
	
		'''
		It's important to note that some administrators disable receiving ICMP ECHO requests, specifically to prevent the use of utilities like
		traceroute, since it can be used for denial-of-service attacks and the network layout might be very sensitive. Thus it's possible that we'll get a timeout 			when we try to receive a ICMP response which will result in an exception. So I have written the recvfrom() call in a try exception block.

		'''
		try:  
			data, host_addr = receive_socket.recvfrom(1026) #returns data and an address structure containg IP Address and Port Number. We need only the IP.
			host_ip_addr = host_addr[0]  
		except socket.error:
			host_ip_addr = "TIMEOUT-NO RESPONSE"	 #If no response is received from gateway or host, let the user know.						  
		finally:
			receive_socket.close()   #in next iteration we will make new sockets with a greater TTL. Thus, close both the sockets. 
			send_socket.close() 
	
		print ("TTL: %d\tIP ADDRESS: %s" % (ttl, host_ip_addr))	#print the IP Address of this intermediate gateway host / destination host.
		
		if host_ip_addr == destination_addr:
			break
				 
if __name__ == "__main__":
	target = sys.argv[1]  #take command line arguemnet of name of destination.
	main(target)		
