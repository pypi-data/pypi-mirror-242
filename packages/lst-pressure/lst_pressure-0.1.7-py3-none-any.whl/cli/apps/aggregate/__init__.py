from __future__ import annotations  # Not required from 3.11 onwards
from ..AppInterface import AppInterface
from typing import Type


class Aggregate(AppInterface):
    id = "aggregate"

    def build(self) -> Type[Aggregate]:
        return self

    def parse(self) -> Type[Aggregate]:
        return self

    def exe(self) -> Type[Aggregate]:
        return self
