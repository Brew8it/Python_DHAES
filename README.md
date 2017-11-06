# Python_DHAES
Diffie Hellman "from scratch" and using PyNaCL as crypto library.

Basic Idea:
Create a simple Client -> Server echo program.
  * Make Key-Exchange with Diffie Hellman.
  * Encrypt and Decrypt using Secret_Box using Key from DH exchange.
  * Send message from Client -> Server and Server echos is back with "Echo" | message.
