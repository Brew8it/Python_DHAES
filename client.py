import socket
import sys
import DiffieHellman
import AES
from binascii import hexlify


client = DiffieHellman.D_H()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5555)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
# test area for DH

data = client.pubKey
sock.sendall(str(data))

data = sock.recv(10240)

print("Key:", hexlify(data))
client.genKey(int(data))
print("Secret key:", hexlify(client.getKey()))
# end of test area

#init AES
AES_c = AES.AESCipher(client.getKey())



while True:
    print 'Enter a msg or "exit" to close the program'
    message = raw_input()
    if message != 'exit':
        sock.sendall(AES_c.encrypt(message))
        data = sock.recv(10240)
        data = AES_c.decrypt(data)
        print >>sys.stderr, 'Recived data: "%s"' % data
    else:
        sock.sendall(message)
        print >>sys.stderr, 'Closing socket.'
        sock.close()
        break

