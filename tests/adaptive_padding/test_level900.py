from pytest import mark


@mark.parametrize("length, expected", [(134, 900), (679, 900)])
def test_level900_when_less_than_900_then_return_900(create_level900_padding, length, expected):
    actual: int = create_level900_padding.pad(length)
    assert expected == actual


@mark.parametrize("length", [901, 998])
def test_level900_when_between_901_and_998_return_within_this_interval(create_level900_padding, length):
    actual: int = create_level900_padding.pad(length)
    assert 901 <= actual <= 1000


@mark.parametrize("length", [999, 1398])
def test_level900_when_between_999_and_1399_return_within_this_interval(create_level900_padding, length):
    actual: int = create_level900_padding.pad(length)
    assert 999 <= actual <= 1400


@mark.parametrize("length", [1400, 1499])
def test_level900_when_greater_or_equal_than_1400_return_1500(level900_padding, length):
    actual: int = level900_padding.pad(length)
    assert actual == 1500
