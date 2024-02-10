from typing import Dict

from adaptive_padding.padding.adaptive_padding.level100 import Level100
from adaptive_padding.padding.adaptive_padding.level500 import Level500
from adaptive_padding.padding.adaptive_padding.level700 import Level700
from adaptive_padding.padding.adaptive_padding.level900 import Level900
from adaptive_padding.padding.existing.exponential_padding import ExponentialPadding
from adaptive_padding.padding.existing.linear import LinearPadding
from adaptive_padding.padding.existing.mouse_elephant import MouseElephant
from adaptive_padding.padding.existing.mtu import Mtu
from adaptive_padding.padding.existing.random import RandomPadding
from adaptive_padding.padding.existing.random_255 import Random255
from adaptive_padding.padding.padding_strategy import PaddingStrategy


def create_existing_strategies_mapping() -> Dict[str, PaddingStrategy]:
    return {
        "exponential": ExponentialPadding(),
        "linear": LinearPadding(),
        "mouse_elephant": MouseElephant(),
        "mtu": Mtu(),
        "random": RandomPadding(),
        "random255": Random255()}


def create_proposal_strategies_mapping() -> Dict[str, PaddingStrategy]:
    return {
        "100": Level100(),
        "500": Level500(),
        "700": Level700(),
        "900": Level900()
    }

