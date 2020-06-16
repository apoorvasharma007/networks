#Apoorva Sharma 510817044 

#The intuition for the program is fairly simple. An image is a 2 dimensional matrix and we can invert it by inverting the intensity of each pixel of the image.  For this program I have used a library openCV which makes the task of reading and writing images as a 2D matrix in a program simple. This program works for all image formats. Given a black and white image, the colors are inverted. Given a colored image, the colors are inverted. For the PGM format the library functions are not supported, however, the intuition remains exactly the same. I will try to implement my own structures for processing an image as a 2D matrix.  

import socket
import cv2
import matplotlib.pyplot as plot
import matplotlib.image as mpimg

HOST='127.0.0.1'
PORT=65432

serversocket=socket.socket()  #create a socket for running the server
serversocket.bind((HOST,PORT)) #bind the socket to a port 
serversocket.listen(5)  #activate listening on the socket
client,addr=serversocket.accept() #connect the server socket with client socket,once connection established, client and server can communicate with each other.

data=client.recv(1024).decode('utf-8') #print message received by the client, client sends a text asking for an image.
print(data)

f=open('original.png','rb') #send the requested image to the client. The image binary is read and sent over the channel.
image=f.read()
client.send(image)   #image sent.
f.close()

invertedimage=client.recv(40960000) #recieve the inverted image binary sent by the client. 
f=open('receivedimage.png','wb')    #save the recieved image to a file by writing the image binary to a new file.
f.write(invertedimage)
f.close()


img1=mpimg.imread('original.png')  #plot the original image in a new window .
plot.figure()
plot.imshow(img1)


img2=mpimg.imread('receivedimage.png') #plot the inverted image in a new window.
plot.figure()
plot.imshow(img2)

plot.show()  #display the 2 image windows.

client.close() #close the socket after communication
