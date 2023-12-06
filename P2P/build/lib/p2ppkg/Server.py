import socket

localIP     = "127.0.0.1"
localPort   = 7070
bufferSize  = 1024

currentConnections = {}  # List to hold active clients' IP and port
# Datagram socket is made
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# IP address and port number are binded to server socket
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Continually listen for datagrams coming to the Server
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode("ascii")
    address = bytesAddressPair[1]
    if "newClient" in message:  # receive client and set address
        currentConnections[message.split(" ")[1]] = address
        print(currentConnections)
    if "messageReq" in message:  # receive number of client and ACK client IP and port
        client = message.split(" ")[1]
        if client in currentConnections:
            clientAddress = "Client address is: " + currentConnections[client][0] + " " + str(currentConnections[client][1])
            UDPServerSocket.sendto(bytes(clientAddress,"ascii"), address)
        else:
            UDPServerSocket.sendto(bytes("Client " + client + " inactive", "ascii"), address)
    if "Client Leave" in message:  # Handles client leave request
        del currentConnections[message.split(" ")[2]]  # update dict
        UDPServerSocket.sendto(bytes("Client " + message.split(" ")[2] + " disconnected from server", "ascii"), address)  # ACK to client
        print(currentConnections)
