from adaptive_padding.padding.adaptive_padding.level900 import Level900

from pytest import fixture


@fixture(scope="function")
def create_level900_padding():
    return Level900()
