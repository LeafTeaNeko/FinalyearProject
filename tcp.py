# Echo server program
import socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
# s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

conn, addr = s.accept()
print ('Connected by', addr)
while 1:
    data = conn.recv(1024)
    if not data: break
    info_package = '88888'
    conn.sendall(info_package.encode('utf-8'))
conn.close()

# # Setup Socket for data transfer
# TransferSocket = socket.socket(sock..et.AF_INET,socket.SOCK_STREAM)
# host = 'localhost'
# port = '7777'
# TransferSocket.connect((host,port))

# # Get data to send (this case a text file)
# f = open("file.txt","rb")

# # send message
# chunk = f.read(1024)
# while (chunk):
#     TransferSocket.send(chunk)  # Send data
#     Rmsg = TransferSocket.recv(1024) # wait for handshake before sending more
#     if Rmsg.decode() == "ACK":
#         chunk = f.read(1024)
#     else:
#         pass