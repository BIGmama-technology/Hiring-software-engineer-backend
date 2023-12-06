import unittest
import asyncio
from unittest.mock import MagicMock
 

from clientserverpkg.server import handle_client


class TestServer(unittest.TestCase):
    async def test_handle_client(self):
        asyncio.run(handle_client())
        

if __name__ == '__main__':
    unittest.main()
