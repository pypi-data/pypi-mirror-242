import pytest
from unittest.mock import patch
from lindvall_tools.geodesy.utils import (
    check_model,
    get_transverse_mercator_parameters,
    degr_to_radians,
    get_ellipsoidal_parameters,
)


def test_check_model_with_valid_model():
    implemented_models = ["GRS1980", "SWEREF99TM"]
    model = "GRS1980"
    result = check_model(model, implemented_models)
    assert result == "GRS1980"


@patch("builtins.input", side_effect=["y"])
def test_check_model_with_invalid_model_default_projection(mock_input):
    implemented_models = ["SWEREF99TM"]
    model = "InvalidModel"
    result = check_model(model, implemented_models)
    assert result == "SWEREF99TM"


@patch("builtins.input", side_effect=["n"])
def test_check_model_with_invalid_model_raise_error(mock_input):
    implemented_models = ["SWEREF99TM"]
    model = "InvalidModel"
    with pytest.raises(NameError):
        check_model(model, implemented_models)


@patch("builtins.input", side_effect=["invalid_input", "y"])
def test_check_model_with_invalid_input(mock_input):
    implemented_models = ["SWEREF99TM"]
    model = "InvalidModel"
    with pytest.raises(ValueError):
        check_model(model, implemented_models)


def test_degr_to_radians():
    degrees = 45.0
    result = degr_to_radians(degrees)
    expected_result = 0.785398163
    assert result == pytest.approx(expected_result, abs=1e-6)


def test_get_transverse_mercator_parameters_sweref99tm():
    projection = "SWEREF99TM"
    result = get_transverse_mercator_parameters(projection)
    expected_result = (degr_to_radians(15), 0.9996, 0, 500000)
    assert result == pytest.approx(expected_result, abs=1e-6)


def test_get_ellipsoidal_parameters():
    ellipsoid = "GRS1980"
    result = get_ellipsoidal_parameters(ellipsoid)
    expected_result = (6378137.0000, 1 / 298.257222101)
    assert result == pytest.approx(expected_result, abs=1e-6)
