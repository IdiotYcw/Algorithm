import socket
import time
from datetime import datetime

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_name = '127.0.0.1'
server_address = (server_name, 8083)
print('starting up on %s port %s' % server_address)

# Listen for incoming connections
sock.bind(server_address)
sock.listen(5)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)
        count = 0
        # Receive the data in small chunks and retransmit it
        while count < 1000000:
            print('SEND COUNT %s' % count)
            connection.send(bytes(
                ('600093,牛逼,T111,13:54:07.110,43983364,633373968.00,14.690,14.000,15.500,13.580,13.650,0.000,13.650,1300,13.670,200,%s\n' % count).encode()))
            count += 1
            time.sleep(0.01)

    finally:
        # Clean up the connection
        print('close connection')
        connection.close()
        print('close socket')
        sock.close()
