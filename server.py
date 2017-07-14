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
print('Starting up on IP: %s and port: %s' % server_address)

#Listen for incoming connections.
sock.listen(1)

# Accepting the incoming traffic on server socket.
connection, client_address = sock.accept()
sock_open = True
print('Connection from IP:', client_address)
data = connection.recv(10240)

connection.sendall(str(server.pubKey))
server.genKey(int(data))
print("Secret key:", hexlify(server.getKey()))

AES_S = AES.AESCipher(server.getKey())

while True:
    msg = connection.recv(10240)
    if msg:
        msg = AES_S.decrypt(msg)
        print >>sys.stderr, 'Echo\'ing back to client'
        msg = echoString + msg
        connection.sendall(AES_S.encrypt(msg))
    else:
        break
print 'Closing socket.'
connection.close()