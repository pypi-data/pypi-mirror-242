from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type


class AppInterface(ABC):
    @property
    @staticmethod
    def id():
        pass

    def __init__(self, parser) -> None:
        self.parser = parser
        self.build()

    @abstractmethod
    def build(self) -> Type[AppInterface]:
        pass

    @abstractmethod
    def parse(self) -> Type[AppInterface]:
        pass

    @abstractmethod
    def exe(self) -> Type[AppInterface]:
        pass
