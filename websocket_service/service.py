from websocket_service.lib.websocket_service_abc import WebsocketServiceABC, SubscriberABC
from fastapi import WebSocket
import json

class Subscriber(SubscriberABC):
    def __init__(self, socket: WebSocket):
        self.socket = socket
    
    async def notify(self, message: dict):
        await self.socket.send_json(json.dumps(message))

class WebSocketService(WebsocketServiceABC):
    connection_manager = {}
    def __init__(self, channel: str, subscribers: list[SubscriberABC] = []):
        self.channel = channel
        self.subscribers = subscribers

    def add_subscriber(self, subscriber: SubscriberABC):
        self.subscribers.append(subscriber)
    
    def remove_subscriber(self, subscriber: SubscriberABC):
        self.subscribers.remove(subscriber)
    
    async def broadcast(self, message: dict, exclude: list[SubscriberABC] = []):
        for subscriber in self.subscribers:
            if subscriber in exclude: 
                continue
            await subscriber.notify(message)
    
    async def send_message(self, subscriber: SubscriberABC, message: dict):
        await subscriber.notify(message)
    
    def get_all_subscribers(self):
        return self.subscribers
    
    @staticmethod
    def get_instance(channel: str):
        if channel in WebSocketService.connection_manager:
            return WebSocketService.connection_manager[channel]
        ws = WebSocketService(channel)
        WebSocketService.connection_manager[channel] = ws
        return ws
