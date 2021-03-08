import websockets
import time
import asyncio
import json

class DrawingController:
    def __init__(self):
        self.uri = "ws://34.82.37.10:6789"
        self.request = json.dumps({'action': 'request'})
        self.speed = 10000

    async def fetchPacket(self):
        await self.ws.send(self.request)
        print(f'Sent request...')
        packet = await self.ws.recv()
        self.sendGRBL(packet)

    async def loop(self):
        num_fails = 0
        while True:
            try:
                async with websockets.connect(self.uri) as self.ws:
                    num_fails = 0
                    state = await self.ws.recv()
                    print(f'Startup State: {state}')
                    while True:
                        input('Press any button to fetch next packet...')
                        await self.fetchPacket()
            except Exception as e:
                print(f'Error: {e}')
                num_fails += 1
                if num_fails < 10:
                    print('Connection Error! Reestablishing connection...')
                else:
                    print(f'Connection failed {num_fails} times. Exiting.')
                    break

    def sendGRBL(self, packet):
        data = json.loads(packet)
        if data['type'] == 'state':
            x = data['x']
            y = data['y']
            cmd = f'G01 X{int(x)} Y{int(y)} F{int(self.speed)}'
            print(cmd)
        else:
            print(f'Incorrect packet type: {data}')
        


   
