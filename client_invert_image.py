import socket
import cv2

clientsocket=socket.socket() #create client socket.
PORT = 65432    
HOST='127.0.0.1'             #give the port number the client should connect to.

clientsocket.connect((HOST,PORT)) #connect client socket to the host at given port number.



clientsocket.send(("send image please").encode('utf-8')) #request server for image binary.

data=clientsocket.recv(40960000)  #recieve image data as binary.
f=open('receivedfile.png', 'wb')       #temoprarily save this image to a file.
f.write(data)
f.close()

img=cv2.imread('receivedfile.png',1)  #transform this temporarily saved image file by inverting all the pixels.
inverted_img=1-img              #this function inverts all the pixels values of the 2D matrix.
cv2.imwrite('tempinvertedimage.png',inverted_img) #save the inverted image temporarily as a file.

f=open('tempinvertedimage.png','rb')    #read the inverted image from file.
invertedimage=f.read()
clientsocket.send(invertedimage)    #send inverted image to server.

clientsocket.close() #close the client socket.
