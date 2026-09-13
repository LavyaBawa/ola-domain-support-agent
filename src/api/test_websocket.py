import asyncio
import websockets


async def test_websocket():
    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
        await websocket.send("Hello support agent")
        response = await websocket.recv()
        print("Server response:", response)


asyncio.run(test_websocket())
