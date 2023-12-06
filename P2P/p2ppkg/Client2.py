import socket
import threading
import time

clientNumber = 2  # client number of this client
serverAddressPort = ("127.0.0.1", 7070) 
bufferSize = 1024
messageAddressPort = None  
serverLock = threading.Event() 
timerLock = threading.Event()
connecting = False
connected = False
connectedClient = "" 
terminated = False
ackNum = 0
sequenceNum = 0
otherSequenceNum = 0
previousSequenceNum = 0 

def thread_func(socket):
    global messageAddressPort
    global connectedClient
    global connecting
    global connected
    global terminated
    global ackNum
    global sequenceNum
    global previousSequenceNum
    global otherSequenceNum
    while(True):
        receive = socket.recvfrom(bufferSize)
        message = receive[0].decode("ascii")
        
        if(message.startswith("Client address is: ")):
            messageAddressPort = (message.split(" ")[3], int(message.split(" ")[4]))
            connecting = True 
            print(message)
            serverLock.set()
        # Receive request from other client
        elif(message.startswith("Connection Request")):
            connectedClient = message.split(" ")[2]
            connecting = True
            messageAddressPort = receive[1]
            print(message)
        
        elif(message == "Client " + connectedClient + " inactive"):
            print("Client " + connectedClient + " does not exist")
            connecting = False
            print(message)
            serverLock.set()
        
        elif(message.startswith("Connection Accept")):
            connected = True
            connecting = False
            mesList = message.split()
            del mesList[-1]
            print(" ".join(mesList))
            timerLock.set()
        # Other client declines, stop repeat attempting to connect
        elif(message.startswith("Connection Reject")):
            connecting = False
            messList = message.split()
            del messList[-1]
            print(" ".join(messList))
            timerLock.set()
        # Receive ACK from server for disconnection
        elif(message == "Client " + str(clientNumber) + " disconnected from server"):
            print(message)
            socket.close()
            serverLock.set()
            break
        
        elif(message == "Connection Termination"):
            connected = False
            socket.sendto(bytes("Termination ACK", "ascii"), messageAddressPort)
            print(message)
            print("Client number to connect to: ")
            terminated = True
        # Client requesting termination receives ACK
        elif(message == "Termination ACK"):
            print(message)
            serverLock.set()
        
        elif(message.startswith("Sequence")):
            otherSequenceNum = message.split(" ")[1]
            socket.sendto(bytes("ACK " + otherSequenceNum, "ascii"), messageAddressPort)
            if(otherSequenceNum == previousSequenceNum):
                continue
            previousSequenceNum = otherSequenceNum
            messageList = message.split() 
            print(" ".join(messageList[2:-1]))
       
        elif(message.startswith("ACK")):
            ackNum = int(message.split(" ")[1])
            timerLock.set()

# Create client side UDP Socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Send UDP socket to server with client number
UDPClientSocket.sendto(bytes("newClient "+str(clientNumber), "ascii"), serverAddressPort)

# Create thread
thread = threading.Thread(target=thread_func, args=(UDPClientSocket,))
thread.start()
print("Client " + str(clientNumber) + " connected to server")

while True:
    serverLock.clear()
    timerLock.clear()
    if(not terminated):
        connectToClient = input("Client number to connect to: \n")
    else:
        terminated = False
    # Connection termination message to server
    if(connectToClient == "Client Leave"):
        UDPClientSocket.sendto(bytes(connectToClient + " " + str(clientNumber), "ascii"), serverAddressPort)
        serverLock.wait()
        serverLock.clear()
        break
    # Request client IP and Port from server
    if(not connecting and not connected):
        UDPClientSocket.sendto(bytes("messageReq "+connectToClient, "ascii"), serverAddressPort)
        connectedClient = connectToClient
        serverLock.wait()
        serverLock.clear()
        if(connecting): 
            while(connecting):
                UDPClientSocket.sendto(bytes("Connection Request " + str(clientNumber), "ascii"), messageAddressPort)
                timerLock.wait(10)
                timerLock.clear()
    if(connecting):
        # Send answer to client attempting to connect
        if(connectToClient == "Accept"):
            UDPClientSocket.sendto(bytes("Connection Accept " + str(clientNumber), "ascii"), messageAddressPort)
            connected = True
            connecting = False
        else:
            UDPClientSocket.sendto(bytes("Connection Reject " + str(clientNumber), "ascii"), messageAddressPort)
            connected = False
            connecting = False
    # Sending messages between clients
    if(connected):
        while(connected): 
            clientMessage = input()
            if(terminated):
                connectToClient = clientMessage
                break
            if(clientMessage == "Connection Termination"):
                UDPClientSocket.sendto(bytes("Connection Termination", "ascii"), messageAddressPort)
                serverLock.wait()  # wait for termination ACK
                serverLock.clear()
                connected = False
            else:
                sequenceNum += 1 
                while(ackNum < sequenceNum):
                    
                    UDPClientSocket.sendto(bytes("Sequence " + str(sequenceNum) + " " + clientMessage + " " + str(clientNumber), "ascii"), messageAddressPort)
                    timerLock.wait(10)
                    timerLock.clear()
