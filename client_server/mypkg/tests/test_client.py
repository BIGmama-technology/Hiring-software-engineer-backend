import unittest
import asyncio
from unittest.mock import MagicMock, patch

from clientserverpkg.client import send_messages


class TestClient(unittest.TestCase):
    
    async def test_send_messages(self):
         
        asyncio.run(send_messages())
 
  
if __name__ == '__main__':
    unittest.main()
