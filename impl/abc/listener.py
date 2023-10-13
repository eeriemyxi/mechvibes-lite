from abc import ABC, abstractmethod


class AbstractListener(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def listen(self):
        pass
