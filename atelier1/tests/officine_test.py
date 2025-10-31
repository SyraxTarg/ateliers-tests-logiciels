from unittest.mock import patch, MagicMock
import pytest
from main import Officine

@pytest.fixture
def mock_ingredients():
    return [
        "œil/yeux de grenouille",
        "larme de brume funèbre",
        "radicelle de racine hurlante",
        "pincée de poudre de lune",
        "croc de troll",
        "fragment d'écaille de dragonnet",
        "goutte de sang de citrouille"
    ]

@pytest.fixture
def mock_recettes():
    return {
        "fiole de glaires purulentes"   : [ "2 larmes de brume funèbre",  "1 goutte de sang de citrouille" ],
        "bille d'âme évanescente"       : [ "3 pincées de poudre de lune", "1 œil de grenouille" ],
        "soupçon de sels suffocants"    : [ "2 crocs de troll", "1 fragment d'écaille de dragonnet", "1 radicelle de racine hurlante" ],
        "baton de pâte sépulcrale"      : [ "3 radicelles de racine hurlante", "1 fiole de glaires purulentes" ],
        "bouffée d'essence de cauchemar": [ "2 pincées de poudre de lune", "2 larmes de brume funèbre" ]
    }



def test_rentrer_normal(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    # Act
    officine.rentrer("3 yeux de grenouille")

    #Assert
    print(officine.quantite("yeux de grenouille"))
    assert officine.quantite("yeux de grenouille") == 3


def test_rentrer_string_invalid_format(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    # Act
    with pytest.raises(ValueError) as result:
        officine.rentrer("yeux de grenouille")

    #Assert
    assert str(result.value) == "Format invalide. Exemple attendu : '3 yeux de grenouille'"
    assert officine.quantite("yeux de grenouille") == 0


def test_rentrer_invalid_argument_int(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    # Act
    with pytest.raises(AttributeError) as result:
        officine.rentrer(12)

    #Assert
    assert str(result.value) == "'int' object has no attribute 'strip'"


def test_rentrer_invalid_argument_bool(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    # Act
    with pytest.raises(AttributeError) as result:
        officine.rentrer(True)

    #Assert
    assert str(result.value) == "'bool' object has no attribute 'strip'"


def test_quantite_normal_empty(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    #Act
    result = officine.quantite("yeux de grenouille")

    #Assert
    assert result == 0


def test_quantite_normal_loaded(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    #Act
    officine.rentrer("15 yeux de grenouille")
    result = officine.quantite("yeux de grenouille")

    #Assert
    assert result == 15


def test_quantite_inexistent_name(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    #Act
    result = officine.quantite("yeux de grand-mère")

    #Assert
    assert result == 0


def test_quantite_invalid_argument_bool(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    #Act
    with pytest.raises(AttributeError) as result:
        officine.quantite(True)

    #Assert
    assert str(result.value) == "'bool' object has no attribute 'strip'"


def test_quantite_invalid_argument_int(mock_ingredients, mock_recettes):
    #Arrange
    officine = Officine(mock_ingredients, mock_recettes)

    #Act
    with pytest.raises(AttributeError) as result:
        officine.quantite(56)

    #Assert
    assert str(result.value) == "'int' object has no attribute 'strip'"
