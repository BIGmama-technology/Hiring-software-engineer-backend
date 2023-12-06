import asyncio
import subprocess

async def run_server():
    server_process = await asyncio.create_subprocess_exec('python', 'test_server.py')
    await server_process.wait()

async def run_client():
    await asyncio.sleep(5)  # Adjust this depending on your server startup time
    client_process = await asyncio.create_subprocess_exec('python', 'test_client.py')
    await client_process.wait()

async def main():
    # Start the server and client tasks concurrently
    server_task = asyncio.create_task(run_server())
    client_task = asyncio.create_task(run_client())

    # Wait for both tasks to finish
    await asyncio.gather(server_task, client_task)

if __name__ == '__main__':
    asyncio.run(main())
