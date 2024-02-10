from dataclasses import dataclass, field
from random import randint

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class RandomPadding(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__extra_bytes: int = 0

    def pad(self, length: int) -> int:
        try:
            modification = length
            if int(length) < self.mtu_number_bytes:
                upper_bound = self.mtu_number_bytes - int(length)
                self.__extra_bytes = randint(1, upper_bound)
                modification = int(length) + self.__extra_bytes

            return modification

        except ValueError as e:
            raise e
