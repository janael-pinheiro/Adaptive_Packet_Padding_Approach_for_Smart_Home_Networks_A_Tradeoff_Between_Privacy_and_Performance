from dataclasses import dataclass, field
from random import randint

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class Random255(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__extra_bytes: int = 0
        self.__LOWER_BOUND = 1
        self.__UPPER_BOUND = 255

    def pad(self, length: int) -> int:
        if length >= self.mtu_number_bytes:
            return length
        try:
            self.__extra_bytes = randint(self.__LOWER_BOUND, self.__UPPER_BOUND)
            if self.__extra_bytes + length >= self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - length
            return length + self.__extra_bytes
        except ValueError as e:
            raise e
