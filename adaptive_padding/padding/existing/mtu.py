from dataclasses import dataclass, field

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class Mtu(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)

    def __post_init__(self):
        self.__extra_bytes: int = 0

    def pad(self, length: int) -> int:
        try:
            modification = length
            if int(length) < self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - int(length)
                modification = int(length) + self.__extra_bytes
            return modification

        except ValueError as e:
            raise e
