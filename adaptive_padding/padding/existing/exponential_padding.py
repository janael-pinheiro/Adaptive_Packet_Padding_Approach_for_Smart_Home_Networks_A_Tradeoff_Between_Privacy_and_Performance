import math
from dataclasses import dataclass, field

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class ExponentialPadding(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__extra_bytes: int = 0

    def pad(self, length: int) -> int:
        try:
            if length < 1024:
                self.__extra_bytes = 2 ** (int(math.log(length, 2)) + 1) - length

            elif length >= 1024 and int(length) < self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - length

            return length + self.__extra_bytes

        except ValueError as exception:
            raise exception
