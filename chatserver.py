#Apoorva Sharma
''''
In this program the fundamental approach was to create a thread for every client that connects to the server. This program works for 100 clients as the server waits for 100 clients in the queue. The clients are given a unique identification number (client ID). The server maintains a list of all client's socket and their unique ID's. The flow of the program is as follow-

1. Implement the server socket and bind it to a port.
2. Keep listening for a client and as soon as one connects, store it's socket (returned by .accept() call) and ask for an ID. 
3. Spawn a thread (Function Clientthread ) for this client which will indefinitely ask the client if it wants to send a message or not. If it does, it will receive   the message.
4. The message received will contain the message as well as the destination client's ID. Function Broadcast will deliver this message to the destination client.
5. A Remove function will remove a client from the list of clients stored on the server if that clients socket is closed.

'''


import socket #for socket and socket function calls
import _thread # for creating threads 
PORT= 65431 #assign port for server to run
IP=''       # the default IP of the local host

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #assign a number to this socket
server.bind((IP, PORT))  # bind this socket to the port 
server.listen(100)       # activate listening on the socket
list_of_clients = []     # stores communication socket for each client, and each client's ID 
  
def clientthread(conn, addr, sender_id): # this function is called in a new thread for every client.  
	conn.send(("Welcome to this chatroom! \nPlease type your message followed by COMMA and destination ID \n").encode()) #send welcome msg and format of texting to client 
	while True: 
		try:
			data = conn.recv(2048).decode()                #if client wants to send message, receive it .
			msg,receiver_id = data.split(',')              # the message is followed by ',' and destination. extract them by splitting the message on comma.
			receiver_id=receiver_id.replace(" ", "")       #this will be printed on the server side, just to see how this script is working
			print(msg+ " for " + receiver_id)
			if len(msg)>0:  
				message_to_send = "FROM " + sender_id + ": " +  msg  #each receiver must know who sent this message, so add sender's ID to the message being sent.
				broadcast(message_to_send, receiver_id)	     #call broadcast function which sends the message to the UNIQUE RECEIVER
		except: 
			continue
  
def broadcast(message, to_who):     #fucntion to send a given message to a UNIQUE DESTINATION client.
	for client in list_of_clients:  #find the communication socket of the DESTINATION client by comparing ID's. 
		if client[1]==to_who:
			try:
				client[0].send(message.encode()) #when found the destination client, send the message using it's communication socket
			except: 
				client[0].close() # if the link is broken, we remove the client
				remove(client) 
			
def remove(client): #function to remove a client whose connection is broken 
	if client in list_of_clients:
		print("removed "+client[1])
		list_of_clients.remove(connection) 
  
while True: 
	conn, addr = server.accept()   #accept a request to connect from a client
	number=conn.recv(4).decode()   #the client will send it's unique ID.
	list_of_clients.append([conn,number])   #store the communicaton socket and ID for this client. 
	_thread.start_new_thread(clientthread,(conn,addr,number))# creates and individual thread for every client that connects     
 
server.close() #close the server socket after completion.
