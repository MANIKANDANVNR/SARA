from typing import Callable


class EventManager:

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name: str, callback: Callable):

        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)

    def emit(self, event_name: str, data=None):

        callbacks = self.listeners.get(event_name, [])

        for callback in callbacks:
            callback(data)

    def clear(self):

        self.listeners.clear()