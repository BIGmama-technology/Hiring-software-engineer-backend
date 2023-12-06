import unittest
import asyncio
from unittest.mock import MagicMock, patch

from clientserverpkg.client import send_messages


class TestClient(unittest.TestCase):
    @patch('builtins.input', side_effect=["Message1", "Message2", "Message3"])
    async def test_send_messages(self, mock_input):
        # Create a mock reader and writer (you can adapt this based on your actual implementation)
        reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        writer_transport = MagicMock()

        # Set up the send_messages coroutine
        coro = send_messages()

        # Mock the input function to provide predefined messages
        with patch('builtins.input', side_effect=["Message1", "Message2", "Message3"]):
            await coro

        # Verify the expected behavior based on the provided input
        expected_messages = ["Message1", "Message2", "Message3"]
        for expected_message in expected_messages:
            writer_transport.write.assert_called_with(expected_message.encode())
            await writer_transport.drain()

            # Add any additional verification based on your implementation

if __name__ == '__main__':
    unittest.main()
