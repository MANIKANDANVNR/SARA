from abc import ABC, abstractmethod


class AIProvider(ABC):

    name = "unknown"

    model = "unknown"

    @abstractmethod
    def health_check(self):
        pass

    @abstractmethod
    def generate(self, prompt, context=None):
        pass