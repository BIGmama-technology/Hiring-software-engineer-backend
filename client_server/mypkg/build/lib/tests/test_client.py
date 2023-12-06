import unittest
import asyncio
from unittest.mock import MagicMock, patch

from clientserverpkg.client import send_messages


class TestClient(unittest.TestCase):
    
    async def test_send_messages(self):
         
        asyncio.run(send_messages())
         
         

        # Set up the send_messages coroutine
         
        # Mock the input function to provide predefined messages
       
        # Verify the expected behavior based on the provided input
         

            # Add any additional verification based on your implementation
            
  
if __name__ == '__main__':
    unittest.main()
