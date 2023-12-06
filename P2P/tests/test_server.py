import asyncio
import socket

localIP = "127.0.0.1"
localPort = 7070
bufferSize = 1024

currentConnections = {}  # Dictionary to hold active clients' IP and port

async def handle_datagrams():
    # Datagram socket is created
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # IP address and port number are bound to the server socket
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")

    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode("ascii")
        address = bytesAddressPair[1]

        if "newClient" in message:
            # Receive client and set address
            currentConnections[message.split(" ")[1]] = address
            print(currentConnections)

        elif "messageReq" in message:
            # Receive number of client and ACK client IP and port
            client = message.split(" ")[1]
            if client in currentConnections:
                clientAddress = "Client address is: " + str(currentConnections[client][0]) + " " + str(currentConnections[client][1])
                UDPServerSocket.sendto(bytes(clientAddress, "ascii"), address)
            else:
                UDPServerSocket.sendto(bytes("Client " + client + " inactive", "ascii"), address)

        elif "Client Leave" in message:
            # Handles client leave request
            del currentConnections[message.split(" ")[2]]  # Update dictionary
            UDPServerSocket.sendto(bytes("Client " + message.split(" ")[2] + " disconnected from server", "ascii"), address)
            print(currentConnections)

async def main():
    await handle_datagrams()

if __name__ == '__main__':
    asyncio.run(main())
