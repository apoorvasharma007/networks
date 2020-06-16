import socket 
import time

HOST = "127.0.0.1"
PORT = 65432
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Make a client socket for communication with server.
sum=0 #will calculate 10 RTT's and take their average.
for i in range(10):
	starttime = time.time() #start the clock.
	clientsocket.sendto(("ping").encode(),(HOST,PORT)) #send ping message to server.
	data,serveraddr = clientsocket.recvfrom(1024)      #receive pong message from the server.
	endtime = time.time()                              #calcuate the round trip time
	sum+=(endtime-starttime)*1000                      #and save it in miliseconds upto three decimal places.
	data = data.decode()                               #print pong message received by the server  
	print(data)
	
print("Average Round Trip Time is %.3f \n" % (sum/10) ) #print the average RTT of 10 signals sent back and forth .
