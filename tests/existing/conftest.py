from adaptive_padding.padding.existing.mtu import Mtu
from adaptive_padding.padding.existing.exponential_padding import ExponentialPadding


from pytest import fixture


@fixture(scope="function")
def mtu_padding():
    return Mtu()


@fixture(scope="function")
def exponential_padding():
    return ExponentialPadding()
