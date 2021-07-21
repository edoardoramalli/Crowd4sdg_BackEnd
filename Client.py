import asyncio
import websockets
import json

# async def hello():
#     # uri = "ws://localhost:8765"
#     uri = "ws://127.0.0.1:8000/WS/some_url"
#     async with websockets.connect(uri) as websocket:
#         # name = input("What's your name? ")
#         #
#         # await websocket.send(name)
#         # print(f"> {name}")
#
#         greeting = await websocket.recv()
#         print(f"< {greeting}")


async def async_processing():
    uri = "ws://127.0.0.1:8000/WS/some_url"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = json.loads(await websocket.recv())
                await websocket.send(json.dumps({'message': 'ciao'}))
                print(message['message'])

            except websockets.exceptions.ConnectionClosed:
                print('ConnectionClosed')
                is_alive = False
                break


asyncio.get_event_loop().run_until_complete(async_processing())

# uri = "ws://127.0.0.1:8000/WS/some_url"
# hello()
#
# exit()
#
# loop = asyncio.get_event_loop()
# loop.create_task(hello())
# loop.run_forever()

# asyncio.get_event_loop().run_until_complete(hello())
# asyncio.get_event_loop().run_forever()