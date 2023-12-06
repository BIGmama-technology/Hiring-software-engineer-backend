import asyncio
async def send_messages():

    # connection to the server
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    for _ in range(5):  # Send 5 messages, you can adjust as needed or keep it looping
        #get the input message
        message = input("Enter a message: ")
        print(f"Send: {message!r}")

        #encode the message and send to the server
        writer.write(message.encode())

        #wait until the data is sent to the server
        await writer.drain()


        #read the response from server
        #up to 100 bytes
        data = await reader.read(100)
        print(f"Received: {data.decode()!r}")

    print("Closing the connection")

    #close the connection
    writer.close()



# Run the asynchronous function
asyncio.run(send_messages())
