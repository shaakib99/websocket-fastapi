from abc import ABC, abstractmethod
from fastapi import WebSocket

class SubscriberABC(ABC):
    def __init__(self, socket:WebSocket):
        pass

    @abstractmethod
    async def notify(self, message: dict):
        pass

class WebsocketServiceABC(ABC):
    def __init__(self, channel, subscribers: list[SubscriberABC] = []):
        pass

    @abstractmethod
    def add_subscriber(self, subscriber: SubscriberABC) -> None:
        pass

    @abstractmethod
    def remove_subscriber(self, subscriber: SubscriberABC) -> None:
        pass

    @abstractmethod
    async def broadcast(self, message: dict, exclude: list[SubscriberABC]) -> None:
        pass

    @abstractmethod
    async def send_message(self, subscriber: SubscriberABC, message: dict) -> None:
        pass

    @abstractmethod
    def get_all_subscribers(self) -> list[SubscriberABC]:
        pass

    @staticmethod
    @abstractmethod
    def get_instance(channel) -> "WebsocketServiceABC":
        pass