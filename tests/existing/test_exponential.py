from pytest import mark


@mark.parametrize("length, expected", [(100, 128), (66, 128), (1054, 1500)])
def test_exponential_strategy(exponential_padding, length, expected):
    actual: int = exponential_padding.pad(length)
    assert expected == actual
