import socket
import DiffieHellman
import AES
import nacl.secret
import nacl.utils
from binascii import hexlify

# Initialize Diffie Hellman object so private and public keys are generated.
client = DiffieHellman.D_H()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5555)
sock.connect(server_address)
print("Connected to %s on port %s" % server_address)

# Send Client's public key to the server so the Diffie hellman key exchange can happen.
# And cast the key over to string so we can send it over the socket.
sock.sendall(str(client.pubKey))

# Receive servers public key so we can generate the final (secret) key.
data = sock.recv(10240)

# Generate the secret key and cast the incoming key to int from str.
client.genKey(int(data))
print("Secret key:", hexlify(client.getKey()))

# Initialize the AES object and pass in the secret key.
#AES_c = AES.AESCipher(client.getKey())
box = nacl.secret.SecretBox(client.getKey())

while True:
    print 'Enter a msg or "exit" to close the program'
    message = raw_input()
    if message != 'exit':
        #sock.sendall(AES_c.encrypt(message))
        sock.sendall(box.encrypt(message))
        data = sock.recv(10240)
        data = box.decrypt(data)
        #data = AES_c.decrypt(data)
        print 'Recived data: "%s"' % data
    else:
        print 'Closing socket.'
        sock.close()
        break

