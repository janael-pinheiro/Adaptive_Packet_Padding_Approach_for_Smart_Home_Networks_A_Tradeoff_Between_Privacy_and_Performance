from dataclasses import dataclass, field
from random import randint

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class Level100(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__threshold = 100
        self.__extra_bytes = 0

    def pad(self, length: int) -> int:
        try:
            if length < self.__threshold:
                self.__extra_bytes = self.__threshold - length

            elif length >= self.__threshold and length < 200:
                self.__extra_bytes = 200 - int(length)

            elif length >= 200 and length < 300:
                self.__extra_bytes = 300 - length

            elif length >= 300 and length < 999:
                upper_bound = 1000 - length
                self.__extra_bytes = randint(1, upper_bound)

            elif length >= 999 and length <= 1399:
                upper_bound = 1400 - length
                self.__extra_bytes = randint(1, upper_bound)

            elif length >= 1400 and length < self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - int(length)

            return length + self.__extra_bytes

        except ValueError as e:
            raise e
