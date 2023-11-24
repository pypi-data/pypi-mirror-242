import numpy as np
from typing import Any


def check_float(var: Any) -> float:
    """Transform inpurt argument var to type float.

    Args:
        var (Any): input argument.

    Raises:
        TypeError: if 'var' can not be transformed to type float raise error.

    Returns:
        float: 'var' as type float.
    """
    if not isinstance(var, float):
        try:
            var = float(var)
            return var
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid value for conversion to float: {e}")

    return var


def degr_min_sec_to_decimal_degr(data: tuple) -> float:
    """Transform an angle expressed in degrees, minutes and seconds to
    an angle expressed as decimal degrees.

    Args:
        data (tuple): angle in degrees, minutes and seconds

    Returns:
        float: angle in decimal degrees
    """
    decimal_degr = data[0] + data[1] / 60.0 + data[2] / 3600.0
    return decimal_degr


def degr_to_radians(degrees: float) -> float:
    """Transform angle expressed in degrees to angle expressed in radians.

    Args:
        degrees (float): angle in degrees

    Returns:
        float: angle in radians
    """
    radians = degrees * (np.pi / 180)
    return radians


def get_transverse_mercator_parameters(
    projection: str,
) -> tuple[float, float, float, float]:
    """Returns the transverse mercator parameters of a projection.

    Symbols and definitions:
        lam0    longitude of central meridian
        k0      scale factor along the central meridian
        FN      false northing
        FE      false easting

    Args:
        projection (str): name of projection

    Returns:
        tuple[float, float, float, float]: transverse mercator parameters
    """
    projection = check_model(
        model=projection, implemented_models=["test", "SWEREF99TM"]
    )

    if projection == "test":
        lam0 = (13, 35, 7.692000)
        k0 = 1.000002540000
        FN = -6226307.8640
        FE = 84182.8790

    if projection == "SWEREF99TM":
        lam0 = (15, 0, 0)
        k0 = 0.9996
        FN = 0
        FE = 500000

    if len(lam0) == 3:
        lam0 = degr_min_sec_to_decimal_degr(lam0)

    lam0 = degr_to_radians(lam0)

    return lam0, k0, FN, FE


def check_model(model: str, implemented_models: list) -> str:
    default_ellipsoid = "GRS1980"
    default_projection = "SWEREF99TM"

    if not model in implemented_models:
        print(f"Model '{model}' is not among implemented models: {implemented_models}.")

        if default_ellipsoid in implemented_models:
            proceed = input(
                f"Proceed with default ellipsoid '{default_ellipsoid}'? (y/n) "
            )
            if proceed == "y":
                model = default_ellipsoid
                return model

        elif default_projection in implemented_models:
            proceed = input(
                f"Proceed with default projection '{default_projection}'? (y/n) "
            )
            if proceed == "y":
                model = default_projection
                return model

        if proceed == "n":
            raise NameError("A known model is required.")
        elif proceed != "y":
            raise ValueError("Answer with either 'y' (yes) or 'n' (no).")

    return model


def get_ellipsoidal_parameters(ellipsoid: str) -> tuple[float, float]:
    """Return the ellipsoidal parameters associated with an ellips.

    Args:
        ellips (str): name of ellips

    Returns:
        tuple[float, float]: ellipsoidal parameters
    """
    ellipsoid = check_model(model=ellipsoid, implemented_models=["GRS1980"])
    if ellipsoid == "GRS1980":
        a = 6378137.0000
        f = 1 / 298.257222101
    return a, f


def from_ellipsoidal_parameters(a: float, f: float) -> tuple[float, float, float]:
    """Computes addtional parameters from ellipsoidal parameters.

    Args:
        a (float): semi-major axis of the ellipsoid
        f (float): flattening of the ellipsoid

    Returns:
        tuple[float, float, float]: additional parameters associated with ellipsoidal parameters
    """
    e_cubed = f * (2 - f)
    e = np.sqrt(e_cubed)
    n = f / (2 - f)
    a_hat = (a / (1 + n)) * (1 + (1 / 4) * n**2 + (1 / 64) * n**4)
    return e, n, a_hat
