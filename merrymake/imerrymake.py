from abc import ABC, abstractmethod

class IMerrymake(ABC):
    @abstractmethod
    def handle(self):
        pass

    @abstractmethod
    def initialize(self):
        pass
