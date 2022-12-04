from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        pass

    @abstractmethod
    def important_log(self, msg: str) -> None:
        pass


class SilentLogger(Logger):
    def log(self, msg):
        pass

    def important_log(self, msg: str) -> None:
        print(f"{msg}")


class ConsoleLogger(Logger):
    def log(self, msg):
        print(msg)

    def important_log(self, msg: str) -> None:
        print(f"{msg}")
