from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        pass


class DummyLogger(Logger):
    def log(self, msg):
        pass


class ConsoleLogger(Logger):
    def log(self, msg):
        print(msg)
