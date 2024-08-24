from fastapi import FastAPI, WebSocket
from websocket_service.service import WebSocketService, Subscriber

app = FastAPI()

@app.websocket('/ws/{channel}')
async def socket(websocket: WebSocket, channel: str):
    await websocket.accept()

    client = Subscriber(websocket)
    websocket_service = WebSocketService.get_instance(channel)
    websocket_service.add_subscriber(client)

    while True:
        data = await websocket.receive_text()
        await websocket_service.broadcast({"message": "Hello World"}, [client])

