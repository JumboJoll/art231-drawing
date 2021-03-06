import websockets
import time
import asyncio
import json
import serial

class DrawingController:
    def __init__(self):
        self.uri = "ws://34.82.37.10:6789"
        self.request = json.dumps({'action': 'request'})
        self.speed = 10000

        # Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
        self.s = serial.Serial('/dev/cu.usbserial-14110',115200) # GRBL operates at 115200 baud. Leave that part alone.

        # Wake up grbl
        self.s.write("\r\n\r\n")
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input

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
            cmd = f'G01 X{int(x)} Y{int(y)} F{int(self.speed)}\n'
            print('GRBL < ' + cmd)
            s.write(cmd)
            grbl_out = s.readline() # Wait for grbl response with carriage return
            print('GRBL > ' + grbl_out.strip())
        else:
            print(f'Incorrect packet type: {data}')
        

if __name__ == "__main__":
    dc = DrawingController()
    asyncio.get_event_loop().run_until_complete(dc.loop())
    dc.s.close()