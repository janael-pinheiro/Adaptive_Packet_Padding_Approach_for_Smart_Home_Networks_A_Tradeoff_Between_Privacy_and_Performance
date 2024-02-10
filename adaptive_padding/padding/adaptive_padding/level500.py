from dataclasses import dataclass, field
from random import randint

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class Level500(PaddingStrategy):
    extra_bytes: int = field(default=0)
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__threshold = 500
        self.__extra_bytes = 0

    def pad(self, length: int) -> int:
        try:
            if length < self.__threshold:
                self.__extra_bytes = self.__threshold - length
            elif length >= self.__threshold and length < 999:
                le = 1000 - length
                self.__extra_bytes = randint(1, le)
            elif length >= 999 and length <= 1399:
                le = 1400 - length
                self.__extra_bytes = randint(1, le)
            elif length >= 1400 and length < self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - length
            return length + self.__extra_bytes
        except ValueError as e:
            raise e
