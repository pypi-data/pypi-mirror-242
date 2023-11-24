from abc import ABC, abstractmethod
from typing import Self


class AppInterface(ABC):
    @property
    @staticmethod
    def id():
        pass

    def __init__(self, parser) -> None:
        self.parser = parser
        self.build()

    @abstractmethod
    def build(self) -> Self:
        pass

    @abstractmethod
    def parse(self) -> Self:
        pass

    @abstractmethod
    def exe(self) -> Self:
        pass
