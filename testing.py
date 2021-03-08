
# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

async def counter(websocket, path):
    print(websocket)
    async for message in websocket:
        print(message)


start_server = websockets.serve(counter, "0.0.0.0", port = 80)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()