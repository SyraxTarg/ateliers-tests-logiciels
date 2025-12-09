import pytest
from main import Laboratory

def test_init_labo():
    #Arrange
    substances = []

    # Act
    with pytest.raises(Exception) as result:
        Laboratory(substances)

    # Assert
    assert str(result.value) == "List can't be empty"


def test_get_quantity():
    #Arrange
    substances = ["toto", "tata"]
    l = Laboratory(substances)

    # Act
    result = l.getQuantity("toto")
    # Assert
    assert result == 0
