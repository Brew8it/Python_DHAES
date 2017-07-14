import socket
import sys
from binascii import hexlify
import DiffieHellman
import AES

# Initialize Diffie Hellman object so private and public keys are generated.
server = DiffieHellman.D_H()

echoString = "I have received | "



#create a TCP/IP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to a port
server_address = ('localhost',5555)
sock.bind(server_address)
print('Starting up socket on IP: %s and port %s' % server_address)

#Listen for incoming connections.
sock.listen(1)

# Accepting the incoming traffic on server socket.
connection, client_address = sock.accept()
print('Connection from IP:', client_address)
data = connection.recv(10240)
idata = int(data)
print("Key:", hexlify(data))
connection.sendall(str(server.pubKey))
server.genKey(idata)
print("Secret key:", hexlify(server.getKey()))

AES_S = AES.AESCipher(server.getKey())


# ennd test area

while True:
    #wait for connection
    #print >>sys.stderr, 'Waiting for a connection.'
    #connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'Connection from', client_address
        ##Revice the data
        while True:
            data = connection.recv(10240)
            data = AES_S.decrypt(data)
            if data != 'exit':
                #print >>sys.stderr, 'Recived "%s"' % data
                print >>sys.stderr, 'sending data back to the client'
                data = echoString + data
                connection.sendall(AES_S.encrypt(data))
            else:
                break
    finally:
        print >>sys.stderr, 'Closing socket.'
        connection.close()