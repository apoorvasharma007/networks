#Apoorva Sharma 510817044
#The intuition for the program is fairly simple. Round trip time is the time taken to send a signal from the source to destination plus the time taken to receive the acknowledgement of that signal being received. Here my client will send a PING message to the server and server will send a PONG message back to the client. When the client receives the PONG message it will calculate the round trip time taken by the signal. The average round trip time on my machine was around 1.021-1.505 miliseconds.

import socket 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #Establishing a connectionless UDP channel for transmission.
serversocket.bind(('127.0.0.1', 65432))   #Binding the socket to a port.

for i in range(10):
	data,addr = serversocket.recvfrom(1024) #receive the message from client. 
	
	print(data.decode()) #print the message received.
	
	serversocket.sendto(("pong").encode(), addr) #send acknowledgement message to client.

