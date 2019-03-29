"""
Async approach just to compare with multi=thread one that I use in bombard.py

Obsolete, is not used.
"""
from aiohttp import ClientSession, TCPConnector
import asyncio
from typing import Optional


async def post(semaphore: asyncio.Semaphore, session: ClientSession, url: str, data: Optional[str]):
    async with semaphore:
        try:
            async with session.post(url, data=data) as r:
                response_data = await r.read()

                class Response(object):
                    def __init__(self, status_code, text):
                        self.status_code = status_code
                        self.text = text

                return Response(r.status, response_data.decode('utf-8'))
        except Exception as e:
            print(e)
            return None

max_connections = 50
requests = [('https://localhost/api/users', None)]

async with ClientSession(connector=TCPConnector(limit=max_connections)) as session:
    semaphore = asyncio.Semaphore(256)
    coros = [post(semaphore, session, r[0], r[1]) for r in requests]
    requests = await asyncio.gather(*coros)

