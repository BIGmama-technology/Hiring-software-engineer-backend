import asyncio
import subprocess

async def run_server():
    server_process = await asyncio.create_subprocess_exec('python', 'test_server.py')
    await server_process.wait()

async def run_client1():
    await asyncio.sleep(5)  # Adjust this depending on your server startup time
    client_process = await asyncio.create_subprocess_exec('python', 'test_client1.py')
    await client_process.wait()

async def run_client2():
    await asyncio.sleep(5)  # Adjust this depending on your server startup time
    client_process = await asyncio.create_subprocess_exec('python', 'test_client2.py')
    await client_process.wait()

async def main():
    # Start the server and client tasks concurrently
    server_task = asyncio.create_task(run_server())
    client2_task = asyncio.create_task(run_client2())
    client1_task = asyncio.create_task(run_client1())

    # Wait for both tasks to finish
    await asyncio.gather(server_task, client2_task,client1_task)

if __name__ == '__main__':
    asyncio.run(main())

    

 