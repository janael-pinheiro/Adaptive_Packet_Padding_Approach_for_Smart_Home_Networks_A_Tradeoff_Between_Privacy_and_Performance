from dataclasses import dataclass, field

from adaptive_padding.padding.padding_strategy import PaddingStrategy


@dataclass
class LinearPadding(PaddingStrategy):
    mtu_number_bytes: int = field(default=1500)
    threshold: int = 128

    def __post_init__(self):
        self.__extra_bytes: int = 0

    def pad(self, length: int) -> int:
        try:
            if length < 1408:
                for x in range(1, 12):
                    if length < x * self.threshold:
                        self.__extra_bytes = x * self.threshold - length
                        break

            elif length >= 1409 and int(length) < self.mtu_number_bytes:
                self.__extra_bytes = self.mtu_number_bytes - length

            return length + self.__extra_bytes

        except ValueError as e:
            raise e
