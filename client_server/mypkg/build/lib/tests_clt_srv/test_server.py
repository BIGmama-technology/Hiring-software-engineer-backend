import unittest
import asyncio
from unittest.mock import MagicMock

from clientserverpkg.server import handle_client, start_server

class TestServer(unittest.TestCase):
    async def test_handle_client(self):
        # Create a mock reader and writer
        reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        writer_transport = MagicMock()

        # Set up the handle_client coroutine
        coro = handle_client(reader, writer_transport)

        # Start the server
        server_task = asyncio.ensure_future(start_server())

        # Send data to the server (simulate client sending data)
        message = "Hello, Server!"
        writer_transport.get_extra_info.return_value = ('127.0.0.1', 12345)
        writer_transport.is_closing.return_value = False
        writer_transport.write.return_value = None
        writer_transport.drain.return_value = asyncio.Future()
        asyncio.ensure_future(coro)
        await asyncio.sleep(0.1)  # Let the coroutine execute

        # Verify that handle_client processed the data correctly
        received_data = await reader.read(100)
        received_message = received_data.decode()
        self.assertEqual(received_message, message)

        # Stop the server
        server_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await server_task

if __name__ == '__main__':
    unittest.main()
