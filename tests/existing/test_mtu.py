from pytest import mark


@mark.parametrize("length", [100, 66, 1054])
def test_mtu_strategy(mtu_padding, length):
    expected: int = 1500
    actual: int = mtu_padding.pad(length)
    assert expected == actual
