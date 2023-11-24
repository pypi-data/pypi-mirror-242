from abc import ABC, abstractmethod


class SunProvider(ABC):
    @abstractmethod
    def calc_sun():
        pass
