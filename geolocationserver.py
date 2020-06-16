#Apoorva Sharma
''' 
In this program I have written a simple server script which will listen for a connection from a remote client. To locate the remote client I need his IP Address. When the server accepts a connection request by .accept() call, it returns a new socket descriptor for connecting to the client and ADDRESS STRUCTURE which stores the IP ADDRESS AND PORT NUMBER of the client. From this address structure I have extracted the IP Address of the client. 

With the IP Address known, I query a free to use online database of global IP Addresses for the location of this particular IP Address. The API used by "https://ipinfo.io/" automatically returns the location of the IP Address as a simple JSON structure listing country name, city name, zip code etc. I have parsed the JSON by using python's default json library. The parsed information is displayed on the console.

I also learnt that if an IP Address which is local to a network is given, then client cannot be located. In this case,  such reserved IP's along with other IP ranges that haven’t yet been allocated and therefore also shouldn’t appear on the public internet are sometimes known as bogons. Thus, in such cases the API of ipinfo.io returns "bogon=true".
 
'''

import socket # For socket programming.
import urllib.request # For querying the url of ipinfo.io and receive a JSON response.
import json      # To parse JSON structures.

HOST='147.32.69.80' #dummy IP address for hosting a server.
PORT=65432          #port number for the server to listen on.

serversocket=socket.socket() #create a socket for the server. 
serversocket.bind((HOST,PORT)) #bind the socket to the specific port.
serversocket.listen(5)      # now the server is listening for requests to connect on the specified port.

while:
	client,addr=serversocket.accept()  #connect to the client and store its IP Address and port number in structure addr. addr[0]=IP Address, addr[1]=Port Number.
	url="https://ipinfo.io/"           #generate a url to send a query to for the geolocation of the client. 
	print ('Connected to client from' , addr[0]) #prints on the console the IP Address of the client.
	url+=addr[0]                      #append the IP Address of the client to generate full url on which we will send the query.
	result=urllib.request.urlopen(url).read() #request for JSON response from ipinfo.io 
	json.loads(result)                # parse the JSON structure obtained.
	print(result)                     # print the geolocation obtained.
	client.close()                    #close the communication channel.

serversocket.close()#close server when done.	
	
