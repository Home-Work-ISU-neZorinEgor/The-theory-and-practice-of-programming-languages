import pytest

from extended_dlc import ExtendedDLC, ploc, iloc

@pytest.fixture
def extended_dlc_instance():
    return ExtendedDLC()

def test_ploc_operators(extended_dlc_instance):
    ploc_instance = extended_dlc_instance.ploc

    assert ploc_instance.operators('=', 5, 5)
    assert not ploc_instance.operators('=', 5, 3)
    assert ploc_instance.operators('>', 5, 6)
    assert not ploc_instance.operators('>', 5, 4)
    assert ploc_instance.operators('<', 5, 4)
    assert not ploc_instance.operators('<', 5, 6)


def test_ploc_parse_keys(extended_dlc_instance):
    ploc_instance = extended_dlc_instance.ploc

    extended_dlc_instance["1,2"] = 3
    extended_dlc_instance["4,5"] = 6

    assert ploc_instance.parse_keys() == [[1.0, 2.0], [4.0, 5.0]]

def test_ploc_parse_item(extended_dlc_instance):
    ploc_instance = extended_dlc_instance.ploc

    assert ploc_instance.parse_item("> 5,= 3.14") == [['>', '5'], ['=', '3.14']]

    with pytest.raises(ValueError, match="Invalid key"):
        ploc_instance.parse_item("invalid key")

def test_iloc_getitem(extended_dlc_instance):
    extended_dlc_instance["b"] = 2
    extended_dlc_instance["a"] = 1

    iloc_instance = extended_dlc_instance.iloc
    assert iloc_instance[0] == 1
    assert iloc_instance[1] == 2
    with pytest.raises(ValueError, match="index out of range"):
        iloc_instance[2]

