from abc import ABC, abstractmethod


class PaddingStrategy(ABC):
    @abstractmethod
    def pad(self, length: int) -> int:
        ...

