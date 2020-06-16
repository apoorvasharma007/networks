#Apoorva Sharma
''' 
The idea here is to create a client socket and communicate with the server through this socket. The FUNDAMENTAL concept here is of thread syncronisation essentially. We know that each client socket is communicating wiht the server inside a thread. Now there are 2 scenarios. 
1. Server is trying to send a message to this client (which it essentially received from some other client).
2. Client is trying to send a message to the server (which is bound to some destination client)
To determine dynamically which one of these 2 condions exist for a particular client, I have used select system call. select() takes a list of file descriptors and returns 3 lists , readable file descriptors which can do read operation only, writable file descriptors which can write/send data, and error file descriptors which cannot do either. 
Thus, if the client socket is in readable list, it means there is some message being sent to it and it has to receive it. Otherwise it is free to send a message.

'''
import socket #for socket programming library of python.
import select #for python implementation of select() system call.
import sys    # for taking command line input of client ID .

#PLEASE GIVE A UNIQUE NUMBER AS ARGUEMENT FROM THE COMMAND LINE WHICH WILL BE USE AS ID NUMBER TO IDENTIFY THIS CLIENT ON SERVER'S END.

PORT=65431 #connect to this port where the server is listening. 
IP=''      #server is running on local host.

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #make a socket for TCP protocol communication. 
clientsocket.connect((IP, PORT)) #connect with the server. 
client_id=sys.argv[1]            # store the unique client ID given by user from command line.
clientsocket.send(client_id.encode())  #send this unique ID to the server.

while True:  
	io_streams = [sys.stdin, clientsocket]  # a list of input/output file descriptors, either the socket will send message via stdin or receive via clientsocket.
	read_sockets,write_sockets, error_sockets = select.select(io_streams,[],[]) #select system call will dynamically syncronise and see if a message is coming or not
	for s in read_sockets: 
		if s == clientsocket:  #if the clientsocket is being sent a message by the server, receive it and print it on console
			message = clientsocket.recv(2048).decode() 
			print(message)
			print() #to format output on console
			 
		else:                  #else the client can send a message to whoever he wants to. 
			message = input()  #Take message to be sent as input from console. 
			clientsocket.send(message.encode()) #send the message via the clientsocket.
			print()
			 		
clientsocket.close() #close the clientsocket when communication is done.

'''
IMPORTANT NOTE :  

It is advisable not to kill a client socket without properly shutting it down with .close() 

Excerpt from Python Documentation : 
"Probably the worst thing about using blocking sockets is what happens when the other side comes down hard (without doing a close). Your socket is likely to hang.    SOCKSTREAM is a reliable protocol, and it will wait a long, long time before giving up on a connection. If you’re using threads, the entire thread is essentially dead. There’s not much you can do about it. As long as you aren’t doing something dumb, like holding a lock while doing a blocking read, the thread isn’t really consuming much in the way of resources. Do not try to kill the thread - part of the reason that threads are more efficient than processes is that they avoid the overhead associated with the automatic recycling of resources. In other words, if you do manage to kill the thread, your whole process is likely to be screwed up."

Thus, I haven't been able to figure out a workaround for this problem. If a client is killed without doing a proper close , there is unexpected behaviour in the server side thread. In my program it results in not being removed from the server's side list of clients, Because of this if this client reconnects with his same ID which he used last time, there will be 2 clients in the list of clients on the server side with same ID. One old and one new. The old one's socket is closed but it hasn't  been removed from list of clients. Thus this new client with same ID might not receive some messages because they are misdirected by the server to a brocken socket.

'''
