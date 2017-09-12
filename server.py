import socket
import sys
from binascii import hexlify
import DiffieHellman
import AES
import nacl.secret
import nacl.utils


# Initialize Diffie Hellman object so private and public keys are generated.
server = DiffieHellman.D_H()

# This string we use to cat with the incoming msg and send to cat'd string back.
echoString = "I have received | "

# Create a TCP/IP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_address = ('localhost',5555)
sock.bind(server_address)
print('Starting up on IP: %s and port: %s' % server_address)

# Listen for incoming connections.
sock.listen(1)

# Accepting the incoming traffic on server socket.
connection, client_address = sock.accept()
print('Connection from IP:', client_address)

# Receive clients public key so we can generate the final (secret) key.
client_Pubkey = connection.recv(10240)

# Send our (server) public key.
connection.sendall(str(server.pubKey))

# Generate the secret key and cast the incoming key to int from str.
server.genKey(int(client_Pubkey))
print("Secret key:", hexlify(server.getKey()))

# Initialize the AES object and pass in the secret key.
#AES_S = AES.AESCipher(server.getKey())
box = nacl.secret.SecretBox(server.getKey())

# Enter the loop to keep the socket alive and echo back every msg we get from the client.
while True:
    msg = connection.recv(10240)
    if msg:
        #msg = AES_S.decrypt(msg)
        msg = box.decrypt(msg)
        print >>sys.stderr, 'Echo\'ing back to client'
        msg = echoString + msg
        connection.sendall(box.encrypt(msg))
        #connection.sendall(AES_S.encrypt(msg))
    else:
        break
print 'Closing socket.'
connection.close()