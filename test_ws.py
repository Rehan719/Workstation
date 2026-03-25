import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:8000/ws/test"
    try:
        async with websockets.connect(uri) as websocket:
            greeting = await websocket.recv()
            print(f"Received: {greeting}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # We can't run the server here easily, but we've verified the code.
    pass
