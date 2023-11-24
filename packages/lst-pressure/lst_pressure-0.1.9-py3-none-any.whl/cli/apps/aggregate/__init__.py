from ..AppInterface import AppInterface
from typing import Self


class Aggregate(AppInterface):
    id = "aggregate"

    def build(self) -> Self:
        return self

    def parse(self) -> Self:
        return self

    def exe(self) -> Self:
        return self
